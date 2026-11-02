#!/usr/bin/env node
/**
 * 🤖 Antigravity Asymmetric Subagent Runner (2026)
 * 
 * Purpose: Enables the Chief Orchestrator model to delegate token-heavy tasks 
 * (codebase surveys, multi-file scans, code generation, adversarial reviews, and log compression)
 * to fast, free submodels (Groq LPU, Mistral Codestral, Google Gemini, OpenRouter) 
 * without bloating the primary conversation context window (<600 tokens active state).
 * 
 * Features:
 *   - Groq LPU Neural Router (<150ms dynamic model arbitration)
 *   - Dynamic OpenRouter Free Model Discovery & Intelligence/Capability Scoring
 *   - Strict Zero-Cost Enforcement (Guaranteed 100% free models only)
 *   - Automatic Resilient Cascade Fallbacks (HTTP 429 rate limit tolerance)
 * 
 * Usage:
 *   node ./scripts/subagent.js --task research --query "How does auth work?" --files "src/auth.ts,src/server.ts"
 *   node ./scripts/subagent.js --task code --file "src/utils.ts" --prompt "Add UUID generator"
 *   node ./scripts/subagent.js --task review [--diff | --file "src/main.ts"]
 *   node ./scripts/subagent.js --task compress --file "build.log"
 *   node ./scripts/subagent.js --task ask --prompt "..." --tier [fast|code|reasoning|cheap]
 *   node ./scripts/subagent.js --list-models [--sort intelligence|latest|code|reasoning]
 *   node ./scripts/subagent.js --refresh-models
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Cache directory setup
const CACHE_DIR = path.join(process.env.USERPROFILE || process.env.HOME || '.', '.gemini', 'config', 'cache');
const OPENROUTER_CACHE_FILE = path.join(CACHE_DIR, 'openrouter_free_models.json');

// Path Traversal Security Guard: restricts file access strictly within current working directory
function isSafePath(filePath) {
  if (!filePath || typeof filePath !== 'string') return false;
  if (filePath.indexOf('\0') !== -1) return false;
  const cwd = path.resolve(process.cwd());
  const resolved = path.resolve(cwd, filePath);
  const relative = path.relative(cwd, resolved);
  return !relative.startsWith('..') && !path.isAbsolute(relative);
}

function readSafeFile(filePath) {
  if (!isSafePath(filePath)) {
    console.warn(`⚠️ [Security Warning] Path traversal blocked: '${filePath}' is outside workspace.`);
    return null;
  }
  const resolved = path.resolve(process.cwd(), filePath);
  try {
    if (fs.existsSync(resolved) && fs.statSync(resolved).isFile()) {
      return fs.readFileSync(resolved, 'utf-8');
    }
  } catch (e) {
    return null;
  }
  return null;
}

// Parse CLI arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const params = {
    help: false,
    task: 'ask',
    query: '',
    prompt: '',
    files: [],
    file: '',
    diff: false,
    tier: 'fast', // fast | code | reasoning | cheap
    model: '',
    provider: '',
    maxTokens: 1024,
    json: false,
    sort: 'intelligence', // intelligence | latest | code | reasoning | context
    router: 'auto', // auto | groq | direct
    listModels: false,
    refreshModels: false
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--help' || arg === '-h') params.help = true;
    else if (arg === '--task' || arg === '-t') params.task = args[++i];
    else if (arg === '--query' || arg === '-q') params.query = args[++i];
    else if (arg === '--prompt' || arg === '-p') params.prompt = args[++i];
    else if (arg === '--files') params.files = (args[++i] || '').split(',').map(s => s.trim()).filter(Boolean);
    else if (arg === '--file' || arg === '-f') params.file = args[++i];
    else if (arg === '--diff' || arg === '-d') params.diff = true;
    else if (arg === '--tier') params.tier = args[++i];
    else if (arg === '--model' || arg === '-m') params.model = args[++i];
    else if (arg === '--provider') params.provider = args[++i];
    else if (arg === '--max-tokens') params.maxTokens = parseInt(args[++i], 10);
    else if (arg === '--json') params.json = true;
    else if (arg === '--sort' || arg === '-s') params.sort = args[++i];
    else if (arg === '--router' || arg === '-r') params.router = args[++i];
    else if (arg === '--list-models' || arg === '-l') params.listModels = true;
    else if (arg === '--refresh-models') params.refreshModels = true;
    else if (!arg.startsWith('-') && !params.prompt) params.prompt = arg;
  }

  return params;
}

function printHelp() {
  console.log(`
🤖 Antigravity Asymmetric Subagent Runner (2026)

Purpose:
  Delegates token-heavy tasks (research, code drafting, adversarial reviews,
  and log compression) to ultra-fast submodels without bloating the primary
  Orchestrator context window (<600 tokens active state).

Usage:
  node ./scripts/subagent.js [options]
  node ./scripts/subagent.js --task <task> [options]

Tasks:
  research, explore   Inspect code files/context and extract concise findings (<250 tokens).
  code, patch         Surgical code generation / patch drafting following Ponytail rules.
  review, adversarial Independent adversarial review on git diff or specific files.
  compress, logs      Compress verbose terminal or test runner logs down to root causes & 1-line fix.
  ask (default)       General fast queries or lightweight assistant responses.

Options:
  -t, --task <type>       Task mode: research | code | review | compress | ask (default: ask)
  -q, --query <string>    Research query or search question
  -p, --prompt <string>   Prompt instructions for code, ask, or compress
  -f, --file <path>       Target file path to inspect, modify, or review
      --files <list>      Comma-separated list of file paths for multi-file research
  -d, --diff              Use git diff (HEAD / staged) as context for review task
      --tier <tier>       Model routing tier: fast | code | reasoning | cheap (default: fast)
  -m, --model <name>      Explicit model override (e.g. openai/gpt-oss-120b, codestral-latest)
      --provider <name>   Explicit provider name override (groq | mistral | gemini | openrouter)
  -r, --router <name>     Router engine: groq | auto | direct (default: auto)
  -s, --sort <criteria>   Sort OpenRouter models: intelligence | latest | code | reasoning | context
  -l, --list-models       Display discovered and ranked zero-cost models table
      --refresh-models    Force refresh of OpenRouter free models cache
      --max-tokens <int>  Maximum output tokens (default: 1024)
      --json              Output response as structured JSON ({ provider, model, output })
  -h, --help              Show this help menu and exit

Examples:
  node ./scripts/subagent.js --list-models --sort intelligence
  node ./scripts/subagent.js --task research --query "How does auth work?" --files "src/auth.ts,src/server.ts"
  node ./scripts/subagent.js --task code --file "src/utils.ts" --prompt "Add UUID generator"
  node ./scripts/subagent.js --task review --diff
  node ./scripts/subagent.js --task compress --file "build.log"
  node ./scripts/subagent.js --task ask --prompt "Explain the Karpathy ladder" --tier fast
`);
}

// Environment Keys
const KEYS = {
  gemini: process.env.GEMINI_API_KEY,
  groq: process.env.GROQ_API_KEY,
  mistral: process.env.MISTRAL_API_KEY,
  openrouter: process.env.OPENROUTER_API_KEY,
  // [PAID TIERS - REMOVED FROM ROTATION. Uncomment when keys are available]
  // deepseek: process.env.DEEPSEEK_API_KEY,
  // xai: process.env.XAI_API_KEY || process.env.GROK_API_KEY
};

// -------------------------------------------------------------
// Dynamic OpenRouter Free Model Discovery & Intelligence Engine
// -------------------------------------------------------------

async function getOpenRouterFreeModels(forceRefresh = false) {
  if (!forceRefresh && fs.existsSync(OPENROUTER_CACHE_FILE)) {
    try {
      const stats = fs.statSync(OPENROUTER_CACHE_FILE);
      const ageMs = Date.now() - stats.mtimeMs;
      if (ageMs < 45 * 60 * 1000) { // 45 minutes cache TTL
        const cached = JSON.parse(fs.readFileSync(OPENROUTER_CACHE_FILE, 'utf8'));
        if (cached && Array.isArray(cached.models) && cached.models.length > 0) {
          return cached;
        }
      }
    } catch (e) {}
  }

  try { fs.mkdirSync(CACHE_DIR, { recursive: true }); } catch (e) {}

  let freeModels = [];
  try {
    const res = await fetch('https://openrouter.ai/api/v1/models');
    if (res.ok) {
      const json = await res.json();
      if (json && Array.isArray(json.data)) {
        freeModels = json.data.filter(m => {
          // Hard rejection if pricing is non-zero
          const promptPrice = m.pricing ? parseFloat(m.pricing.prompt || '0') : 0;
          const completionPrice = m.pricing ? parseFloat(m.pricing.completion || '0') : 0;
          if (promptPrice > 0 || completionPrice > 0) return false;

          // Must either end in :free or have verified $0.00 pricing
          const isExplicitFree = m.id.endsWith(':free');
          const isExplicitZeroPrice = m.pricing && promptPrice === 0 && completionPrice === 0;
          return isExplicitFree || isExplicitZeroPrice;
        });
      }
    }
  } catch (e) {
    if (fs.existsSync(OPENROUTER_CACHE_FILE)) {
      try { return JSON.parse(fs.readFileSync(OPENROUTER_CACHE_FILE, 'utf8')); } catch (err) {}
    }
  }

  function scoreModel(m) {
    let base = 0;
    let codeScore = 0;
    let reasoningScore = 0;
    const text = ((m.description || '') + ' ' + (m.name || '') + ' ' + m.id).toLowerCase();

    // Scale Estimation
    if (text.includes('550b') || text.includes('ultra')) base += 100;
    else if (text.includes('120b') || text.includes('super')) base += 70;
    else if (text.includes('70b')) base += 50;
    else if (text.includes('32b') || text.includes('31b') || text.includes('30b') || text.includes('27b') || text.includes('26b')) base += 35;
    else if (text.includes('14b') || text.includes('12b') || text.includes('8b') || text.includes('7b')) base += 20;
    else base += 10;

    // Reasoning capabilities
    if (m.reasoning && (m.reasoning.default_enabled || m.reasoning.mandatory)) {
      base += 30;
      reasoningScore += 40;
    }
    if (text.includes('reasoning') || text.includes('thinking') || text.includes('deepseek-r1') || text.includes('r1')) {
      base += 25;
      reasoningScore += 30;
    }

    // Code specialization
    if (text.includes('code') || text.includes('coder') || text.includes('programming')) {
      base += 30;
      codeScore += 50;
    }

    // Context length bonus
    if (m.context_length >= 1000000) base += 25;
    else if (m.context_length >= 256000) base += 15;
    else if (m.context_length >= 128000) base += 10;

    // Recency bonus: Models released in 2026 get priority boost
    if (m.created && m.created > 1767225600) {
      base += 20;
    }

    return {
      intelligenceScore: base,
      codeScore: base + codeScore,
      reasoningScore: base + reasoningScore
    };
  }

  const enriched = freeModels.map(m => {
    const s = scoreModel(m);
    return {
      id: m.id,
      name: m.name,
      created: m.created || 0,
      context_length: m.context_length || 0,
      intelligenceScore: s.intelligenceScore,
      codeScore: s.codeScore,
      reasoningScore: s.reasoningScore,
      hasReasoning: !!(m.reasoning && (m.reasoning.default_enabled || m.reasoning.mandatory)),
      description: (m.description || '').slice(0, 140)
    };
  });

  const payload = {
    updatedAt: Date.now(),
    count: enriched.length,
    models: enriched
  };

  try {
    fs.writeFileSync(OPENROUTER_CACHE_FILE, JSON.stringify(payload, null, 2), 'utf8');
  } catch (e) {}

  return payload;
}

function getSortedModels(models, sortKey = 'intelligence') {
  const list = [...models];
  switch (sortKey.toLowerCase()) {
    case 'latest':
    case 'recency':
      return list.sort((a, b) => (b.created || 0) - (a.created || 0));
    case 'code':
    case 'coding':
      return list.sort((a, b) => b.codeScore - a.codeScore);
    case 'reasoning':
    case 'review':
      return list.sort((a, b) => b.reasoningScore - a.reasoningScore);
    case 'context':
      return list.sort((a, b) => b.context_length - a.context_length);
    case 'intelligence':
    default:
      return list.sort((a, b) => b.intelligenceScore - a.intelligenceScore);
  }
}

async function printModelList(sortKey = 'intelligence') {
  console.log(`🔍 Querying latest OpenRouter Zero-Cost models (Sorted by: ${sortKey})...\n`);
  const data = await getOpenRouterFreeModels(false);
  const sorted = getSortedModels(data.models, sortKey);

  console.log(`Found ${data.count} verified 100% Free models (Updated: ${new Date(data.updatedAt).toLocaleTimeString()}):\n`);
  console.log(
    'Rank'.padEnd(5) +
    'Score'.padEnd(7) +
    'Context'.padEnd(9) +
    'Release'.padEnd(12) +
    'Model ID'.padEnd(46) +
    'Capabilities'
  );
  console.log('='.repeat(100));

  sorted.forEach((m, idx) => {
    const rank = `#${idx + 1}`.padEnd(5);
    const score = `${m.intelligenceScore}`.padEnd(7);
    const ctx = `${Math.round(m.context_length / 1000)}k`.padEnd(9);
    const rel = (m.created ? new Date(m.created * 1000).toISOString().split('T')[0] : 'Unknown').padEnd(12);
    const id = m.id.padEnd(46);
    const caps = (m.hasReasoning ? '[Reasoning] ' : '') + (m.codeScore > m.intelligenceScore ? '[Code] ' : '');
    console.log(`${rank}${score}${ctx}${rel}${id}${caps}`);
  });
  console.log('\n💡 Note: All listed models have $0.00 prompt and $0.00 completion cost.');
}

// -------------------------------------------------------------
// Groq LPU Neural Router Engine (<150ms dynamic model decision)
// -------------------------------------------------------------

async function selectModelWithGroqRouter(task, prompt, candidateModels) {
  if (!KEYS.groq) return null;
  try {
    const systemPrompt = `You are the Groq LPU Neural Model Router.
Your job is to select the absolute best model id for the incoming task.
Output ONLY the chosen model id from the candidate list, nothing else.`;

    const userPrompt = `Task Type: ${task}\nInstructions: ${prompt ? prompt.slice(0, 400) : '(empty)'}\n\nCandidate Models:\n` +
      candidateModels.map(c => `- ${c.id}: ${c.desc}`).join('\n');

    // Use fast sub-second inference model on Groq LPU
    const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${KEYS.groq}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'qwen/qwen3.8-27b',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userPrompt }
        ],
        max_tokens: 50,
        temperature: 0.1
      })
    });

    if (res.ok) {
      const data = await res.json();
      const choice = data.choices?.[0]?.message?.content?.trim();
      if (choice && candidateModels.some(c => c.id === choice)) {
        return choice;
      }
    }
  } catch (e) {
    // Router fallback
  }
  return null;
}

// -------------------------------------------------------------
// Model Provider Implementations
// -------------------------------------------------------------

async function callGroq(prompt, systemPrompt, model = 'openai/gpt-oss-120b', maxTokens = 1024) {
  if (!KEYS.groq) throw new Error('GROQ_API_KEY not set');
  const res = await fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${KEYS.groq}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: model || 'openai/gpt-oss-120b',
      messages: [
        ...(systemPrompt ? [{ role: 'system', content: systemPrompt }] : []),
        { role: 'user', content: prompt }
      ],
      max_tokens: maxTokens,
      temperature: 0.2
    })
  });
  if (res.status === 429) {
    throw new Error('Groq free-tier rate limit reached (HTTP 429). Cascading to next free provider.');
  }
  const data = await res.json();
  if (data.error) throw new Error(data.error.message || JSON.stringify(data.error));
  return data.choices?.[0]?.message?.content?.trim() || '';
}

async function callMistral(prompt, systemPrompt, model = 'codestral-latest', maxTokens = 1024) {
  if (!KEYS.mistral) throw new Error('MISTRAL_API_KEY not set');
  const res = await fetch('https://api.mistral.ai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${KEYS.mistral}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: model || 'codestral-latest',
      messages: [
        ...(systemPrompt ? [{ role: 'system', content: systemPrompt }] : []),
        { role: 'user', content: prompt }
      ],
      max_tokens: maxTokens,
      temperature: 0.2
    })
  });
  if (res.status === 429) {
    throw new Error('Mistral free-tier rate limit reached (HTTP 429). Cascading to next free provider.');
  }
  if (res.status === 402 || res.status === 403) {
    throw new Error('Mistral free usage limit reached / payment required (HTTP ' + res.status + '). Blocked to guarantee zero charges.');
  }
  const data = await res.json();
  if (data.error) {
    const errMsg = (data.error.message || JSON.stringify(data.error)).toLowerCase();
    if (errMsg.includes('credit') || errMsg.includes('balance') || errMsg.includes('quota') || errMsg.includes('payment')) {
      throw new Error('Mistral free quota exhausted: ' + (data.error.message || 'Payment required') + '. Cascading to zero-cost fallback.');
    }
    throw new Error(data.error.message || JSON.stringify(data.error));
  }
  return data.choices?.[0]?.message?.content?.trim() || '';
}

async function callGemini(prompt, systemPrompt, model = 'gemini-3.8-flash', maxTokens = 1024) {
  if (!KEYS.gemini) throw new Error('GEMINI_API_KEY not set');
  const modelName = model.includes('/') ? model.split('/')[1] : (model || 'gemini-3.8-flash');
  const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-goog-api-key': KEYS.gemini
    },
    body: JSON.stringify({
      systemInstruction: systemPrompt ? { parts: [{ text: systemPrompt }] } : undefined,
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { maxOutputTokens: maxTokens, temperature: 0.2 }
    })
  });
  if (res.status === 429) {
    throw new Error('Gemini free-tier rate limit reached (HTTP 429). Cascading to next free provider.');
  }
  const data = await res.json();
  if (data.error) throw new Error(data.error.message || JSON.stringify(data.error));
  return data.candidates?.[0]?.content?.parts?.[0]?.text?.trim() || '';
}

/*
// [PAID TIER - REMOVED FROM ACTIVE ROTATION. Uncomment when keys are available]
async function callXAI(prompt, systemPrompt, model = 'grok-2-latest', maxTokens = 1024) {
  if (!KEYS.xai) throw new Error('XAI_API_KEY not set');
  const res = await fetch('https://api.x.ai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${KEYS.xai}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: model || 'grok-2-latest',
      messages: [
        ...(systemPrompt ? [{ role: 'system', content: systemPrompt }] : []),
        { role: 'user', content: prompt }
      ],
      max_tokens: maxTokens,
      temperature: 0.2
    })
  });
  if (res.status === 429) {
    throw new Error('xAI Grok rate limit reached (HTTP 429). Cascading to next free provider.');
  }
  if (res.status === 402 || res.status === 403) {
    throw new Error('xAI Grok trial credits exhausted or forbidden (HTTP ' + res.status + '). Blocked to guarantee zero charges.');
  }
  const data = await res.json();
  if (data.error) {
    const errMsg = (data.error.message || JSON.stringify(data.error)).toLowerCase();
    if (errMsg.includes('credit') || errMsg.includes('balance') || errMsg.includes('quota') || errMsg.includes('payment')) {
      throw new Error('xAI Grok credits exhausted: ' + (data.error.message || 'Payment required') + '. Cascading to zero-cost fallback.');
    }
    throw new Error(data.error.message || JSON.stringify(data.error));
  }
  return data.choices?.[0]?.message?.content?.trim() || '';
}
*/

async function isModelVerifiedFree(modelId) {
  if (!modelId || typeof modelId !== 'string') return false;
  if (modelId === 'openrouter/free') return true;

  // Immediate defensive blacklist against common paid frontier models
  const lower = modelId.toLowerCase();
  const paidKeywords = [
    'gpt-4', 'gpt-3.5', 'o1-preview', 'o1-mini', 'o3-mini',
    'claude-3', 'claude-2', 'claude-instant',
    'gemini-1.5-pro', 'gemini-1.0-pro',
    'mistral-large', 'mistral-medium',
    'command-r-plus', 'dall-e'
  ];
  for (const keyword of paidKeywords) {
    if (lower.includes(keyword) && !lower.endsWith(':free')) {
      return false;
    }
  }

  // Check verified free catalog (which guarantees prompt: 0 and completion: 0)
  const freeData = await getOpenRouterFreeModels(false);
  const found = freeData.models.find(m => m.id === modelId);
  return !!found;
}

async function callOpenRouter(prompt, systemPrompt, model = 'openrouter/free', maxTokens = 1024) {
  if (!KEYS.openrouter) throw new Error('OPENROUTER_API_KEY not set');

  const targetModel = model || 'openrouter/free';

  // Hardcoded safety barrier: strictly 100% zero-cost models allowed
  const isVerified = await isModelVerifiedFree(targetModel);
  if (!isVerified) {
    throw new Error(`[OpenRouter Safety Guard] Blocked paid/unverified model call '${targetModel}'. Only verified zero-cost free models are permitted. Zero paid tokens allowed.`);
  }

  const res = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${KEYS.openrouter}`,
      'Content-Type': 'application/json',
      'HTTP-Referer': 'https://github.com/aryanthepain/antigravity_setup',
      'X-Title': 'Antigravity Free Subagent'
    },
    body: JSON.stringify({
      model: targetModel,
      messages: [
        ...(systemPrompt ? [{ role: 'system', content: systemPrompt }] : []),
        { role: 'user', content: prompt }
      ],
      max_tokens: maxTokens,
      temperature: 0.2
    })
  });

  if (res.status === 429) {
    throw new Error(`OpenRouter rate limit on ${targetModel} (HTTP 429). Cascading to next free candidate.`);
  }

  const data = await res.json();
  if (data.error) throw new Error(data.error.message || JSON.stringify(data.error));
  return data.choices?.[0]?.message?.content?.trim() || '';
}

// OmniRoute / Local gateway check
async function callOmniRoute(prompt, systemPrompt, model, maxTokens = 1024) {
  const res = await fetch('http://127.0.0.1:20128/v1/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: model || 'auto',
      messages: [
        ...(systemPrompt ? [{ role: 'system', content: systemPrompt }] : []),
        { role: 'user', content: prompt }
      ],
      max_tokens: maxTokens
    })
  });
  const data = await res.json();
  if (data.error) throw new Error(data.error.message || JSON.stringify(data.error));
  return data.choices?.[0]?.message?.content?.trim() || '';
}

// -------------------------------------------------------------
// Router Dispatcher with Groq LPU Neural Router & Dynamic Cascades
// -------------------------------------------------------------

async function dispatchToSubagent(prompt, systemPrompt, tier = 'fast', preferredModel = '', maxTokens = 1024, preferredProvider = '', options = {}) {
  const tryCall = async (fn, name, modelName = '') => {
    try {
      const output = await fn();
      return { success: true, provider: name, model: modelName, output };
    } catch (err) {
      return { success: false, provider: name, model: modelName, error: err.message };
    }
  };

  // 1. Try OmniRoute local proxy first if active
  if (!preferredProvider || preferredProvider.toLowerCase() === 'omniroute') {
    try {
      const omniResult = await callOmniRoute(prompt, systemPrompt, preferredModel, maxTokens);
      if (omniResult) return { provider: 'OmniRoute Gateway', model: preferredModel || 'auto', output: omniResult };
    } catch (e) {
      // OmniRoute not active, proceed to direct APIs
    }
  }

  // 1b. Upfront Paid Model Barrier: Verify zero-cost compliance if user explicitly passed a model
  if (preferredModel) {
    const isDirectProvider = ['groq', 'mistral', 'gemini', 'xai'].includes(preferredProvider.toLowerCase());
    if (!isDirectProvider || preferredProvider.toLowerCase() === 'openrouter') {
      const isKnownDirectFree = preferredModel.startsWith('openai/gpt-oss-') || preferredModel.startsWith('qwen/qwen3.8-') || preferredModel === 'codestral-latest' || preferredModel === 'gemini-3.8-flash';
      if (!isKnownDirectFree) {
        const isVerified = await isModelVerifiedFree(preferredModel);
        if (!isVerified) {
          throw new Error(`[OpenRouter Safety Guard] Blocked paid/unverified model call '${preferredModel}'. Only verified zero-cost free models are permitted. Zero paid tokens allowed.`);
        }
      }
    }
  }

  // 2. Query dynamic OpenRouter free models cache
  const freeData = await getOpenRouterFreeModels(false);
  const sortCriteria = options.sort || 'intelligence';
  const sortedFreeModels = getSortedModels(freeData.models, sortCriteria);

  // 3. Dynamic candidate assembly
  let candidateList = [];
  if (KEYS.mistral) candidateList.push({ id: 'codestral-latest', provider: 'Mistral', desc: 'Surgical code intelligence & patch synthesis' });
  if (KEYS.gemini) candidateList.push({ id: 'gemini-3.8-flash', provider: 'Google Gemini', desc: '1M-context multimodal reasoning' });
  if (KEYS.groq) candidateList.push({ id: 'openai/gpt-oss-120b', provider: 'Groq LPU', desc: 'Ultra-fast 120B model (800 tokens/s)' });
  // [PAID TIER - REMOVED FROM ROTATION]
  // if (KEYS.xai) candidateList.push({ id: 'grok-2-latest', provider: 'xAI', desc: 'xAI Grok 2 frontier model' });

  // Add top OpenRouter free models
  sortedFreeModels.slice(0, 5).forEach(m => {
    candidateList.push({
      id: m.id,
      provider: 'OpenRouter',
      desc: `${m.name} (${Math.round(m.context_length / 1000)}k ctx, Score: ${m.intelligenceScore})`
    });
  });

  // 4. Groq LPU Neural Router Arbitration
  let groqChosenModel = null;
  const routerMode = options.router || 'auto';
  if ((routerMode === 'groq' || routerMode === 'auto') && !preferredModel && !preferredProvider && KEYS.groq) {
    groqChosenModel = await selectModelWithGroqRouter(options.task || tier, prompt, candidateList);
  }

  // 5. Build multi-tier attempt cascade
  let attempts = [];

  // If Groq LPU router picked a specific model, prioritize it first!
  if (groqChosenModel) {
    const candidate = candidateList.find(c => c.id === groqChosenModel);
    if (candidate) {
      if (candidate.provider === 'OpenRouter' && KEYS.openrouter) {
        attempts.push(() => callOpenRouter(prompt, systemPrompt, candidate.id, maxTokens), `OpenRouter (${candidate.id})`, candidate.id);
      } else if (candidate.id === 'codestral-latest' && KEYS.mistral) {
        attempts.push(() => callMistral(prompt, systemPrompt, 'codestral-latest', maxTokens), 'Mistral Codestral', 'codestral-latest');
      } else if (candidate.id === 'gemini-3.8-flash' && KEYS.gemini) {
        attempts.push(() => callGemini(prompt, systemPrompt, 'gemini-3.8-flash', maxTokens), 'Google Gemini Flash', 'gemini-3.8-flash');
      } else if (candidate.id === 'openai/gpt-oss-120b' && KEYS.groq) {
        attempts.push(() => callGroq(prompt, systemPrompt, 'openai/gpt-oss-120b', maxTokens), 'Groq LPU (GPT-OSS 120B)', 'openai/gpt-oss-120b');
      // [PAID TIER - REMOVED FROM ROTATION]
      // } else if (candidate.id === 'grok-2-latest' && KEYS.xai) {
      //   attempts.push(() => callXAI(prompt, systemPrompt, 'grok-2-latest', maxTokens), 'xAI Grok', 'grok-2-latest');
      }
    }
  }

  // If user requested a specific provider
  if (preferredProvider) {
    const prov = preferredProvider.toLowerCase();
    if (prov === 'openrouter') {
      const topModel = preferredModel || (sortedFreeModels[0]?.id || 'openrouter/free');
      if (KEYS.openrouter) {
        attempts.push(() => callOpenRouter(prompt, systemPrompt, topModel, maxTokens), `OpenRouter (${topModel})`, topModel);
        // Cascade to next 2 best OpenRouter free models
        sortedFreeModels.slice(1, 3).forEach(m => {
          attempts.push(() => callOpenRouter(prompt, systemPrompt, m.id, maxTokens), `OpenRouter (${m.id})`, m.id);
        });
      }
      if (KEYS.groq) attempts.push(() => callGroq(prompt, systemPrompt, 'openai/gpt-oss-120b', maxTokens), 'Groq LPU (OpenRouter fallback)', 'openai/gpt-oss-120b');
    } else if (prov === 'groq') {
      if (KEYS.groq) attempts.push(() => callGroq(prompt, systemPrompt, preferredModel || 'openai/gpt-oss-120b', maxTokens), 'Groq LPU', preferredModel || 'openai/gpt-oss-120b');
      if (KEYS.mistral) attempts.push(() => callMistral(prompt, systemPrompt, 'codestral-latest', maxTokens), 'Mistral Codestral (Groq fallback)', 'codestral-latest');
      if (KEYS.gemini) attempts.push(() => callGemini(prompt, systemPrompt, 'gemini-3.8-flash', maxTokens), 'Google Gemini Flash (Groq fallback)', 'gemini-3.8-flash');
    } else if (prov === 'mistral') {
      if (KEYS.mistral) attempts.push(() => callMistral(prompt, systemPrompt, preferredModel || 'codestral-latest', maxTokens), 'Mistral Codestral', preferredModel || 'codestral-latest');
      if (KEYS.groq) attempts.push(() => callGroq(prompt, systemPrompt, 'openai/gpt-oss-120b', maxTokens), 'Groq LPU (Mistral fallback)', 'openai/gpt-oss-120b');
    } else if (prov === 'gemini') {
      if (KEYS.gemini) attempts.push(() => callGemini(prompt, systemPrompt, preferredModel || 'gemini-3.8-flash', maxTokens), 'Google Gemini Flash', preferredModel || 'gemini-3.8-flash');
      if (KEYS.groq) attempts.push(() => callGroq(prompt, systemPrompt, 'openai/gpt-oss-120b', maxTokens), 'Groq LPU (Gemini fallback)', 'openai/gpt-oss-120b');
    // [PAID TIER - REMOVED FROM ROTATION]
    // } else if (prov === 'xai' || prov === 'grok') {
    //   if (KEYS.xai) attempts.push(() => callXAI(prompt, systemPrompt, preferredModel || 'grok-2-latest', maxTokens), 'xAI Grok', preferredModel || 'grok-2-latest');
    //   if (KEYS.groq) attempts.push(() => callGroq(prompt, systemPrompt, 'openai/gpt-oss-120b', maxTokens), 'Groq LPU (xAI fallback)', 'openai/gpt-oss-120b');
    }
  }

  // Tier-based defaults (if not already handled or during cascade)
  if (tier === 'code' || tier === 'precision_coding') {
    // Coding hierarchy: Codestral -> Top OpenRouter Code Model -> Gemini 3.8 Flash -> Groq LPU
    const topCodeModel = sortedFreeModels.find(m => m.codeScore > m.intelligenceScore)?.id || sortedFreeModels[0]?.id;
    if (KEYS.mistral) attempts.push(() => callMistral(prompt, systemPrompt, preferredModel || 'codestral-latest', maxTokens), 'Mistral Codestral', 'codestral-latest');
    if (KEYS.openrouter && topCodeModel) attempts.push(() => callOpenRouter(prompt, systemPrompt, topCodeModel, maxTokens), `OpenRouter (${topCodeModel})`, topCodeModel);
    if (KEYS.gemini) attempts.push(() => callGemini(prompt, systemPrompt, 'gemini-3.8-flash', maxTokens), 'Google Gemini Flash', 'gemini-3.8-flash');
    if (KEYS.groq) attempts.push(() => callGroq(prompt, systemPrompt, 'openai/gpt-oss-120b', maxTokens), 'Groq LPU (GPT-OSS 120B)', 'openai/gpt-oss-120b');
  } else if (tier === 'reasoning' || tier === 'review') {
    // Reasoning / Review hierarchy: Top OpenRouter Reasoning Model -> Gemini 3.8 Flash -> Mistral -> Groq LPU
    const topReasoningModel = sortedFreeModels.find(m => m.hasReasoning)?.id || sortedFreeModels[0]?.id;
    if (KEYS.openrouter && topReasoningModel) attempts.push(() => callOpenRouter(prompt, systemPrompt, topReasoningModel, maxTokens), `OpenRouter (${topReasoningModel})`, topReasoningModel);
    if (KEYS.gemini) attempts.push(() => callGemini(prompt, systemPrompt, 'gemini-3.8-flash', maxTokens), 'Google Gemini Flash', 'gemini-3.8-flash');
    if (KEYS.mistral) attempts.push(() => callMistral(prompt, systemPrompt, 'codestral-latest', maxTokens), 'Mistral Codestral', 'codestral-latest');
    if (KEYS.groq) attempts.push(() => callGroq(prompt, systemPrompt, 'openai/gpt-oss-120b', maxTokens), 'Groq LPU (GPT-OSS 120B)', 'openai/gpt-oss-120b');
  } else {
    // Fast / Research default: Groq LPU (sub-second) -> Gemini 3.8 Flash -> Top OpenRouter Free -> Mistral
    const topFree = sortedFreeModels[0]?.id;
    if (KEYS.groq) attempts.push(() => callGroq(prompt, systemPrompt, preferredModel || 'openai/gpt-oss-120b', maxTokens), 'Groq LPU (GPT-OSS 120B)', preferredModel || 'openai/gpt-oss-120b');
    if (KEYS.gemini) attempts.push(() => callGemini(prompt, systemPrompt, 'gemini-3.8-flash', maxTokens), 'Google Gemini Flash', 'gemini-3.8-flash');
    if (KEYS.openrouter && topFree) attempts.push(() => callOpenRouter(prompt, systemPrompt, topFree, maxTokens), `OpenRouter (${topFree})`, topFree);
    if (KEYS.mistral) attempts.push(() => callMistral(prompt, systemPrompt, 'codestral-latest', maxTokens), 'Mistral Codestral', 'codestral-latest');
  }

  // Execute attempts in priority order
  for (let i = 0; i < attempts.length; i += 3) {
    const fn = attempts[i];
    const name = attempts[i + 1];
    const modelName = attempts[i + 2];
    const res = await tryCall(fn, name, modelName);
    if (res.success && res.output) {
      return { provider: res.provider, model: res.model, output: res.output };
    }
  }

  throw new Error('All model providers failed or keys not configured. Please check GEMINI_API_KEY, GROQ_API_KEY, MISTRAL_API_KEY, or OPENROUTER_API_KEY.');
}

// -------------------------------------------------------------
// Task Implementations
// -------------------------------------------------------------

// 1. RESEARCH & CODE EXPLORATION TASK
async function handleResearch(params) {
  const query = params.query || params.prompt;
  if (!query) {
    console.error('Error: --query or --prompt is required for research task');
    process.exit(1);
  }

  let fileContents = '';
  const fileList = params.files.length > 0 ? params.files : (params.file ? [params.file] : []);

  for (const f of fileList) {
    const content = readSafeFile(f);
    if (content !== null) {
      fileContents += `\n--- FILE: ${f} ---\n${content}\n`;
    }
  }

  const systemPrompt = `You are an ultra-concise Codebase Research Subagent.
Your goal is to inspect the provided code files or context and extract ONLY the exact answers, data structures, signatures, and invariants requested.
DO NOT return entire re-written files or verbose fluff.
Keep your response dense, structured, and under 250 tokens so the Chief Orchestrator stays lean.`;

  const userPrompt = `Research Question: ${query}\n\nFiles Context:\n${fileContents || '(No specific files attached, answer conceptually based on query)'}\n\nDeliverables:\n1. Key Findings & Invariants\n2. Relevant Signatures / Types\n3. Potential Edge Cases or Gotchas`;

  const result = await dispatchToSubagent(userPrompt, systemPrompt, 'fast', params.model, params.maxTokens, params.provider, {
    router: params.router,
    sort: params.sort,
    task: 'research'
  });

  if (params.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`[🤖 Worker Subagent: ${result.provider} | Task: Research]`);
    console.log(result.output);
  }
}

// 2. SURGICAL CODE GENERATION TASK
async function handleCode(params) {
  const instructions = params.prompt || params.query;
  const targetFile = params.file;

  let existingCode = '';
  if (targetFile) {
    const content = readSafeFile(targetFile);
    if (content !== null) {
      existingCode = content;
    }
  }

  const systemPrompt = `You are an expert Surgical Code Generator Subagent.
Follow the Ponytail Laziness Ladder (prefer stdlib, minimal code, zero bloat, no unused classes).
Return ONLY the surgical patch, function, or code block required to satisfy the instructions.
If modifying an existing file, specify the exact lines or function to replace.`;

  const userPrompt = `Target File: ${targetFile || 'Net new code'}\nInstructions: ${instructions}\n\nExisting Code:\n${existingCode || '(None)'}`;

  const result = await dispatchToSubagent(userPrompt, systemPrompt, 'code', params.model, params.maxTokens, params.provider, {
    router: params.router,
    sort: params.sort,
    task: 'code'
  });

  if (params.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`[🤖 Worker Subagent: ${result.provider} | Task: Code Generation]`);
    console.log(result.output);
  }
}

// 3. INDEPENDENT ADVERSARIAL REVIEW TASK
async function handleReview(params) {
  let diffContent = '';

  if (params.diff) {
    try {
      diffContent = execSync('git diff HEAD', { encoding: 'utf-8' });
      if (!diffContent.trim()) {
        diffContent = execSync('git diff --staged', { encoding: 'utf-8' });
      }
    } catch (e) {
      diffContent = '(Unable to get git diff, reviewing target file)';
    }
  }

  if (!diffContent.trim() && params.file) {
    const content = readSafeFile(params.file);
    if (content !== null) {
      diffContent = `File: ${params.file}\n` + content;
    }
  }

  if (!diffContent.trim()) {
    diffContent = params.prompt || 'No diff or code provided for review.';
  }

  const systemPrompt = `You are an Adversarial Code Reviewer Subagent.
Review the provided diff or code against:
1. Logic bugs & unhandled edge cases
2. Security issues or memory leaks
3. Ponytail anti-bloat violations (unnecessary dependencies, premature abstractions)
4. Type safety and invariant violations

Format output as a compact markdown table or bullet points:
- Status: [PASS | CAUTION | REJECT]
- Key Findings (max 3 bullet points)
- Actionable Recommendations`;

  const userPrompt = `Code / Diff for Review:\n${diffContent}`;

  const result = await dispatchToSubagent(userPrompt, systemPrompt, 'review', params.model, params.maxTokens, params.provider, {
    router: params.router,
    sort: params.sort,
    task: 'review'
  });

  if (params.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`[🤖 Worker Subagent: ${result.provider} | Task: Adversarial Review]`);
    console.log(result.output);
  }
}

// 4. LOG / TRACE COMPRESSION TASK
async function handleCompress(params) {
  let logContent = '';
  if (params.file) {
    const content = readSafeFile(params.file);
    if (content !== null) {
      logContent = content;
    } else {
      logContent = params.prompt || params.query;
    }
  } else {
    logContent = params.prompt || params.query;
  }

  const lines = logContent.split('\n');
  if (lines.length > 4000) {
    logContent = lines.slice(-4000).join('\n');
  }

  const systemPrompt = `You are a Log & Stacktrace Compression Subagent.
Analyze the raw terminal/test output and output ONLY:
1. Root Cause / Core Error Message
2. Failing Test Case / File and Line Number
3. Recommended 1-line Fix
Keep output under 100 tokens.`;

  const userPrompt = `Raw Logs:\n${logContent}`;

  const result = await dispatchToSubagent(userPrompt, systemPrompt, 'fast', params.model, 300, params.provider, {
    router: params.router,
    sort: params.sort,
    task: 'compress'
  });

  if (params.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`[🤖 Worker Subagent: ${result.provider} | Task: Log Compression]`);
    console.log(result.output);
  }
}

// 5. GENERAL FAST SUBAGENT ASK
async function handleAsk(params) {
  const prompt = params.prompt || params.query;
  if (!prompt) {
    console.error('Error: --prompt or query text is required');
    process.exit(1);
  }

  const result = await dispatchToSubagent(
    prompt,
    'You are an ultra-fast worker subagent. Give direct, accurate, concise answers.',
    params.tier,
    params.model,
    params.maxTokens,
    params.provider,
    {
      router: params.router,
      sort: params.sort,
      task: 'ask'
    }
  );

  if (params.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`[🤖 Worker Subagent: ${result.provider} | Tier: ${params.tier}]`);
    console.log(result.output);
  }
}

// Main CLI dispatch
async function main() {
  const params = parseArgs();

  if (params.help) {
    printHelp();
    process.exit(0);
  }

  if (params.refreshModels) {
    console.log('🔄 Refreshing OpenRouter free models cache...');
    const data = await getOpenRouterFreeModels(true);
    console.log(`✅ Discovered and cached ${data.count} free models successfully.`);
    process.exit(0);
  }

  if (params.listModels) {
    await printModelList(params.sort);
    process.exit(0);
  }

  try {
    switch (params.task.toLowerCase()) {
      case 'research':
      case 'explore':
        await handleResearch(params);
        break;
      case 'code':
      case 'patch':
        await handleCode(params);
        break;
      case 'review':
      case 'adversarial':
        await handleReview(params);
        break;
      case 'compress':
      case 'logs':
        await handleCompress(params);
        break;
      case 'ask':
      default:
        await handleAsk(params);
        break;
    }
  } catch (err) {
    console.error(`❌ Subagent Execution Error: ${err.message}`);
    process.exit(1);
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    parseArgs,
    isSafePath,
    getOpenRouterFreeModels,
    getSortedModels,
    selectModelWithGroqRouter,
    callGroq,
    callMistral,
    callGemini,
    // callXAI, // [PAID TIER - REMOVED FROM ROTATION]
    callOpenRouter,
    callOmniRoute,
    dispatchToSubagent,
    isModelVerifiedFree,
    KEYS
  };
}

if (require.main === module) {
  main();
}
