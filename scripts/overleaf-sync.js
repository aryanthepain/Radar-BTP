#!/usr/bin/env node
/**
 * scripts/overleaf-sync.js — Universal Overleaf Sync Engine
 *
 * Provides real-time bidirectional synchronization between local LaTeX documents
 * and Overleaf projects via Socket.IO and Operational Transforms (OT).
 *
 * Usage:
 *   node ./scripts/overleaf-sync.js --push
 *   node ./scripts/overleaf-sync.js --pull
 *   node ./scripts/overleaf-sync.js --status
 *   node ./scripts/overleaf-sync.js --project <id> --file <filename> --no-commit
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const DEFAULT_PROJECT_ID = '6af97ae4e99d9136ba9ad729'; // BTP_Report_Template_Overleaf
const ROOT_DIR = process.cwd();

// Locate Overleaf Workshop extension
function findOverleafExtension() {
  const baseDirs = [
    path.join(process.env.USERPROFILE, '.antigravity-ide', 'extensions'),
    path.join(process.env.USERPROFILE, '.vscode', 'extensions'),
    path.join(process.env.USERPROFILE, '.vscode-insiders', 'extensions')
  ];

  for (const base of baseDirs) {
    if (!fs.existsSync(base)) continue;
    const entries = fs.readdirSync(base);
    const match = entries.find(e => e.startsWith('iamhyc.overleaf-workshop'));
    if (match) {
      const fullPath = path.join(base, match);
      if (fs.existsSync(path.join(fullPath, 'node_modules', 'socket.io-client'))) {
        return fullPath;
      }
    }
  }
  return null;
}

const extDir = findOverleafExtension();
if (!extDir) {
  console.error('❌ Overleaf Workshop extension not found in Antigravity IDE or VS Code extensions directories.');
  process.exit(1);
}

const io = require(path.join(extDir, 'node_modules', 'socket.io-client'));
const DiffMatchPatch = require(path.join(extDir, 'node_modules', 'diff-match-patch'));

// Locate SQLite state.vscdb
function findStateVscdb() {
  const candidates = [
    path.join(process.env.APPDATA, 'Antigravity IDE', 'User', 'globalStorage', 'state.vscdb'),
    path.join(process.env.APPDATA, 'Code', 'User', 'globalStorage', 'state.vscdb'),
    path.join(process.env.APPDATA, 'Code - Insiders', 'User', 'globalStorage', 'state.vscdb')
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

function getOverleafIdentity() {
  const vscdb = findStateVscdb();
  if (!vscdb) {
    throw new Error('Could not find VS Code / Antigravity IDE globalStorage state.vscdb');
  }

  const pyScript = `import sqlite3, json, sys
conn = sqlite3.connect(r'${vscdb.replace(/\\/g, '\\\\')}')
c = conn.cursor()
c.execute("SELECT value FROM ItemTable WHERE key = 'iamhyc.overleaf-workshop'")
row = c.fetchone()
print(row[0] if row else '{}')
`;
  const res = spawnSync('python', ['-c', pyScript], { encoding: 'utf-8' });
  if (res.error || res.status !== 0) {
    throw new Error(`Failed to read state.vscdb via python: ${res.stderr || res.error}`);
  }
  const state = JSON.parse(res.stdout.trim() || '{}');
  const server = state?.['overleaf-servers']?.['www.overleaf.com'];
  if (!server?.login?.identity) {
    throw new Error('Overleaf credentials not found in globalStorage. Please log in via Overleaf Workshop extension.');
  }
  return server.login.identity;
}

function decodePackedUtf8(text) {
  return Buffer.from(text, 'latin1').toString('utf-8');
}

async function connectToOverleaf(projectId) {
  const identity = getOverleafIdentity();
  const query = `?projectId=${projectId}&t=${Date.now()}`;

  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      reject(new Error('Connection to Overleaf timed out after 10s'));
    }, 10000);

    const socket = io.connect(`https://www.overleaf.com${query}`, {
      reconnect: false,
      'force new connection': true,
      extraHeaders: {
        'Origin': 'https://www.overleaf.com',
        'Cookie': identity.cookies,
      }
    });

    socket.on('joinProjectResponse', (res) => {
      clearTimeout(timeout);
      const project = res.project || res;
      const rootFolder = Array.isArray(project?.rootFolder) ? project.rootFolder[0] : project?.rootFolder;
      const docs = rootFolder?.docs || [];
      const folders = rootFolder?.folders || [];
      resolve({ socket, project, rootFolder, docs, folders });
    });

    socket.on('connectionRejected', (err) => {
      clearTimeout(timeout);
      socket.disconnect();
      reject(new Error(`Overleaf connection rejected: ${err?.message || err}`));
    });

    socket.on('error', (err) => {
      clearTimeout(timeout);
      socket.disconnect();
      reject(new Error(`Socket error: ${err?.message || err}`));
    });
  });
}

async function getDocContent(socket, docId) {
  return new Promise((resolve, reject) => {
    socket.emit('joinDoc', docId, { encodeRanges: true }, (err, docLinesAscii, version) => {
      if (err) return reject(new Error(`joinDoc failed: ${err}`));
      const lines = (docLinesAscii || []).map(l => decodePackedUtf8(l));
      resolve({ content: lines.join('\n'), version });
    });
  });
}

async function applyDocUpdate(socket, docId, version, oldContent, newContent) {
  const dmp = new DiffMatchPatch();
  let currentPos = 0;
  const diffs = dmp.diff_main(oldContent, newContent);
  const op = diffs.map((part) => {
    const incCount = part[0] === -1 ? 0 : part[1].length;
    currentPos += incCount;
    if (part[0] !== 0) {
      return {
        p: currentPos - incCount,
        i: part[0] === 1 ? part[1] : undefined,
        d: part[0] === -1 ? part[1] : undefined,
      };
    }
  }).filter(Boolean);

  if (op.length === 0) {
    return { noChanges: true, version };
  }

  const update = {
    doc: docId,
    v: version,
    hash: crypto.createHash('sha1').update("blob " + newContent.length + "\x00" + newContent).digest('hex'),
    op: op
  };

  return new Promise((resolve, reject) => {
    socket.emit('applyOtUpdate', docId, update, (err) => {
      if (err) return reject(new Error(`applyOtUpdate failed: ${err}`));
      resolve({ opCount: op.length, version: version + 1 });
    });
  });
}

// Map remote documents to local candidates
function resolveLocalPath(remoteDocName) {
  const searchCandidates = [
    path.join(ROOT_DIR, remoteDocName),
    path.join(ROOT_DIR, 'templates', 'BTP_Report_Template_Overleaf', remoteDocName),
    path.join(ROOT_DIR, 'chapters', remoteDocName)
  ];

  // Specific alias mappings
  if (remoteDocName === 'General_Report_Template.tex') {
    searchCandidates.unshift(path.join(ROOT_DIR, 'report.tex'));
  }
  if (remoteDocName === 'btp_sample_references.bib') {
    searchCandidates.unshift(path.join(ROOT_DIR, 'references.bib'));
  }

  for (const c of searchCandidates) {
    if (fs.existsSync(c)) return c;
  }

  // Fallback to preferred default location
  if (remoteDocName.endsWith('.tex') && remoteDocName !== 'report.tex' && remoteDocName !== 'General_Report_Template.tex') {
    return path.join(ROOT_DIR, 'chapters', remoteDocName);
  }
  return path.join(ROOT_DIR, remoteDocName);
}

async function main() {
  const args = process.argv.slice(2);
  const action = args.includes('--pull') ? 'pull' : (args.includes('--status') ? 'status' : 'push');
  const projectIdx = args.indexOf('--project');
  const projectId = projectIdx !== -1 ? args[projectIdx + 1] : (process.env.OVERLEAF_PROJECT_ID || DEFAULT_PROJECT_ID);
  const fileIdx = args.indexOf('--file');
  const targetFileFilter = fileIdx !== -1 ? args[fileIdx + 1] : null;
  const noCommit = args.includes('--no-commit');

  console.log(`\n🚀 [OVERLEAF SYNC] Mode: ${action.toUpperCase()} | Project ID: ${projectId}`);

  const { socket, project, docs, folders } = await connectToOverleaf(projectId);
  console.log(`  [OK] Connected to Overleaf project: "${project.name}"`);

  // Collect all syncable remote docs
  const remoteDocsToSync = [];
  for (const d of docs) {
    if (!targetFileFilter || d.name === targetFileFilter) {
      remoteDocsToSync.push({ docId: d._id, remoteName: d.name, localPath: resolveLocalPath(d.name) });
    }
  }

  // Also check subfolders (e.g. chapters/)
  for (const f of folders) {
    for (const d of (f.docs || [])) {
      const relName = `${f.name}/${d.name}`;
      if (!targetFileFilter || relName === targetFileFilter || d.name === targetFileFilter) {
        remoteDocsToSync.push({ docId: d._id, remoteName: relName, localPath: path.join(ROOT_DIR, f.name, d.name) });
      }
    }
  }

  if (remoteDocsToSync.length === 0) {
    console.warn(`  [WARN] No matching documents found to sync in Overleaf project.`);
    socket.disconnect();
    process.exit(0);
  }

  let anyChanged = false;
  const changedFiles = [];

  for (const item of remoteDocsToSync) {
    const { content: remoteContent, version } = await getDocContent(socket, item.docId);
    const localExists = fs.existsSync(item.localPath);
    const localContent = localExists ? fs.readFileSync(item.localPath, 'utf-8') : '';
    const localNorm = localContent.replace(/\r\n/g, '\n');
    const remoteNorm = remoteContent.replace(/\r\n/g, '\n');

    if (action === 'status') {
      if (!localExists) {
        console.log(`  [MISSING] Remote "${item.remoteName}" (v${version}) exists on Overleaf but not locally (${path.relative(ROOT_DIR, item.localPath)}).`);
        anyChanged = true;
      } else if (localNorm === remoteNorm) {
        console.log(`  [SYNC] ${item.remoteName} and local ${path.relative(ROOT_DIR, item.localPath)} are in PERFECT SYNC (v${version}).`);
      } else {
        console.log(`  [DRIFT] ${item.remoteName} differs between local and Overleaf (Overleaf v${version}).`);
        anyChanged = true;
      }
    } else if (action === 'pull') {
      if (localNorm === remoteNorm) {
        console.log(`  [OK] ${item.remoteName} is already up to date with Overleaf (v${version}).`);
      } else {
        const dir = path.dirname(item.localPath);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(item.localPath, remoteContent, 'utf-8');
        console.log(`  [OK] Pulled Overleaf "${item.remoteName}" (v${version}) -> ${path.relative(ROOT_DIR, item.localPath)}`);
        anyChanged = true;
        changedFiles.push(item.localPath);
      }
    } else if (action === 'push') {
      if (!localExists) {
        console.warn(`  [WARN] Local file ${item.localPath} does not exist, skipping push for "${item.remoteName}".`);
        continue;
      }
      if (localNorm === remoteNorm) {
        console.log(`  [OK] Overleaf "${item.remoteName}" is already up to date with local (v${version}).`);
      } else {
        console.log(`  [SYNC] Pushing local changes for ${path.relative(ROOT_DIR, item.localPath)} -> Overleaf "${item.remoteName}"...`);
        const res = await applyDocUpdate(socket, item.docId, version, remoteNorm, localNorm);
        console.log(`  [OK] Applied ${res.opCount} diff operations -> Overleaf "${item.remoteName}" updated to v${res.version}!`);
        anyChanged = true;
        changedFiles.push(item.localPath);
      }
    }
  }

  socket.disconnect();

  if (anyChanged && !noCommit && action !== 'status') {
    console.log(`  [NOTE] Changes detected on ${changedFiles.length} files. Git auto-commit skipped (run git commit manually or via wrapper).`);
  }

  console.log(`\n✅ [OVERLEAF SYNC] Operation ${action.toUpperCase()} complete.`);
  process.exit(0);
}

main().catch(err => {
  console.error(`❌ Overleaf sync error: ${err.message}`);
  process.exit(1);
});
