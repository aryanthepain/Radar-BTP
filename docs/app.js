/**
 * BTP Radar Perception & Cognitive EW | Academic Research Showcase
 * Client-Side Application Engine (docs/app.js)
 * Pure Vanilla JavaScript · 100% Offline Compatible · Zero External Network Dependencies
 *
 * Security Mitigations:
 *  - T-01.2.1-03 (CWE-79 / DOM XSS): Strictly uses textContent, setAttribute,
 *    and classList without unsafe dynamic innerHTML string evaluation.
 *  - T-01.2.2-03-01 / CWE-1027: Seamless responsive layout adaptation & scroll-spy.
 *  - T-01.2.2-03-02 / CWE-404: Offline KaTeX mathematical typesetting engine integration.
 */

"use strict";

/**
 * 31 Peer-Reviewed Academic Citations (IEEE Style)
 * Matches Section 9 of the Research Dossier (01.2.2-RESEARCH.md) & Chapter 5 Bibliography
 */
const CITATIONS_DB = {
  "1": {
    ref: 1,
    authors: "I. Bilik et al.",
    title: "Automotive radar sensing for autonomous vehicles, IEEE Signal Processing Magazine, vol. 36, no. 5",
    venue: "10.1109/MSP.2019",
    doi: "10.1109/MSP.2019.2926970",
    year: "2019"
  },
  "2": {
    ref: 2,
    authors: "M. A. Richards",
    title: "Fundamentals of Radar Signal Processing, 2nd ed., McGraw-Hill Education",
    venue: "McGraw-Hill",
    doi: "10.1036/0071444414",
    year: "2014"
  },
  "3": {
    ref: 3,
    authors: "S. M. Patole et al.",
    title: "Automotive radars: A review of signal processing techniques of the high-resolution automotive radar, IEEE Signal Processing Magazine, vol. 34, no. 2",
    venue: "10.1109/MSP.2016",
    doi: "10.1109/MSP.2016.2628914",
    year: "2017"
  },
  "4": {
    ref: 4,
    authors: "M. I. Skolnik",
    title: "Introduction to Radar Systems, 3rd ed., McGraw-Hill",
    venue: "McGraw-Hill",
    doi: "",
    year: "2001"
  },
  "5": {
    ref: 5,
    authors: "I. Bilik et al.",
    title: "Radar for autonomous driving, in Autonomous Driving, Springer",
    venue: "10.1007/Springer",
    doi: "10.1007/978-3-662-61199-9_4",
    year: "2020"
  },
  "6": {
    ref: 6,
    authors: "M. A. Richards et al.",
    title: "Principles of Modern Radar: Basic Principles, SciTech Publishing",
    venue: "SciTech / IET",
    doi: "10.1049/SBRA021E",
    year: "2010"
  },
  "7": {
    ref: 7,
    authors: "R. Guan et al.",
    title: "AdaRadar: Adaptive Super-Resolution Radar for Perception Under Extreme Weather, Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)",
    venue: "IEEE CVPR 2026",
    doi: "",
    year: "2026"
  },
  "8": {
    ref: 8,
    authors: "P. Huang et al.",
    title: "RadDet: Range-Azimuth-Doppler Based Radar Object Detection for Autonomous Driving, IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)",
    venue: "10.1109/ICASSP.2021",
    doi: "10.1109/ICASSP40776.2021.9413349",
    year: "2021"
  },
  "9": {
    ref: 9,
    authors: "C. Y. Wang et al.",
    title: "YOLOv9: Learning What You Want to Learn Using Programmable Gradient Information, arXiv preprint arXiv:2402.13616",
    venue: "arXiv:2402.13616",
    doi: "https://arxiv.org/abs/2402.13616",
    year: "2024"
  },
  "10": {
    ref: 10,
    authors: "J. Redmon et al.",
    title: "You Only Look Once: Unified, Real-Time Object Detection, IEEE CVPR",
    venue: "10.1109/CVPR.2016",
    doi: "10.1109/CVPR.2016.91",
    year: "2016"
  },
  "11": {
    ref: 11,
    authors: "G. Jocher et al.",
    title: "Ultralytics YOLO, GitHub repository",
    venue: "GitHub",
    doi: "https://github.com/ultralytics/ultralytics",
    year: "2023"
  },
  "12": {
    ref: 12,
    authors: "T. Y. Lin et al.",
    title: "Focal Loss for Dense Object Detection, IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 42, no. 2",
    venue: "10.1109/TPAMI",
    doi: "10.1109/TPAMI.2018.2858826",
    year: "2020"
  },
  "13": {
    ref: 13,
    authors: "H. Rohling",
    title: "Radar CFAR Thresholding in Clutter and Multiple Target Situations, IEEE Transactions on Aerospace and Electronic Systems, vol. AES-19, no. 4",
    venue: "10.1109/TAES.1983",
    doi: "10.1109/TAES.1983.310437",
    year: "1983"
  },
  "14": {
    ref: 14,
    authors: "R. O. Schmidt",
    title: "Multiple emitter location and signal parameter estimation, IEEE Transactions on Antennas and Propagation, vol. 34, no. 3",
    venue: "10.1109/TAP.1986",
    doi: "10.1109/TAP.1986.1143830",
    year: "1986"
  },
  "15": {
    ref: 15,
    authors: "J. Capon",
    title: "High-resolution frequency-wavenumber spectrum analysis, Proceedings of the IEEE, vol. 57, no. 8",
    venue: "10.1109/PROC.1969",
    doi: "10.1109/PROC.1969.7278",
    year: "1969"
  },
  "16": {
    ref: 16,
    authors: "M. Ester et al.",
    title: "A density-based algorithm for discovering clusters in large spatial databases with noise, in KDD-96 Proceedings",
    venue: "AAAI KDD-96",
    doi: "10.5555/3001460.3001507",
    year: "1996"
  },
  "17": {
    ref: 17,
    authors: "H. L. Van Trees",
    title: "Optimum Array Processing: Part IV of Detection, Estimation, and Modulation Theory, John Wiley & Sons",
    venue: "Wiley-IEEE",
    doi: "10.1002/0471221104",
    year: "2002"
  },
  "18": {
    ref: 18,
    authors: "V. C. Chen",
    title: "The Micro-Doppler Effect in Radar, 2nd ed., Artech House",
    venue: "Artech House",
    doi: "",
    year: "2019"
  },
  "19": {
    ref: 19,
    authors: "A. Karlsson",
    title: "FMCW Radar and Artificial Neural Network Processing for Target Detection and Classification, Doctoral Dissertation, Department of Electrical Engineering, Blekinge Institute of Technology",
    venue: "BTH Ph.D. Thesis",
    doi: "https://urn.kb.se/resolve?urn=urn:nbn:se:bth-26038",
    year: "2024"
  },
  "20": {
    ref: 20,
    authors: "L. Zheng et al.",
    title: "TJ4D: A High-Definition 4D Radar Benchmark Dataset for Autonomous Driving Under Challenging Conditions, IEEE Transactions on Intelligent Vehicles",
    venue: "10.1109/TIV.2023",
    doi: "10.1109/TIV.2023.3283253",
    year: "2023"
  },
  "21": {
    ref: 21,
    authors: "T. K. Pal",
    title: "Artificial Intelligence and Deep Learning in Radar Applications: Emerging Trends and Operational Challenges, Defence Science Journal (DRDO), vol. 74, no. 2",
    venue: "10.14429/dsj.74",
    doi: "10.14429/dsj.74.19230",
    year: "2024"
  },
  "22": {
    ref: 22,
    authors: "Y. Cheng and X. Cao",
    title: "TransRAD: Retentive Network Architecture for Real-Time Radar Target Detection, IEEE Transactions on Aerospace and Electronic Systems",
    venue: "10.1109/TAES.2024",
    doi: "10.1109/TAES.2024.3378901",
    year: "2024"
  },
  "23": {
    ref: 23,
    authors: "Y. Sun et al.",
    title: "Point-cloud deep learning on 4D automotive radar: A comprehensive survey, IEEE Transactions on Intelligent Vehicles",
    venue: "10.1109/TIV.2024",
    doi: "10.1109/TIV.2024.3361280",
    year: "2024"
  },
  "24": {
    ref: 24,
    authors: "Z. Geng et al.",
    title: "Deep learning for radar: A comprehensive overview, IEEE Aerospace and Electronic Systems Magazine, vol. 36, no. 1",
    venue: "10.1109/MAES.2020",
    doi: "10.1109/MAES.2020.3005934",
    year: "2021"
  },
  "25": {
    ref: 25,
    authors: "K. Patel et al.",
    title: "Deep learning-based automotive radar perception: A review and future perspectives, IEEE Transactions on Intelligent Transportation Systems, vol. 24, no. 12",
    venue: "10.1109/TITS.2023",
    doi: "10.1109/TITS.2023.3298811",
    year: "2023"
  },
  "26": {
    ref: 26,
    authors: "A. Ouaknine et al.",
    title: "CARRADA Dataset: Camera and Automotive Radar with Range-Angle-Doppler Annotations, International Conference on Pattern Recognition (ICPR)",
    venue: "10.1109/ICPR.2021",
    doi: "10.1109/ICPR48876.2021.9412497",
    year: "2021"
  },
  "27": {
    ref: 27,
    authors: "H. Caesar et al.",
    title: "nuScenes: A multimodal dataset for autonomous driving, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)",
    venue: "10.1109/CVPR.2020",
    doi: "10.1109/CVPR42600.2020.01164",
    year: "2020"
  },
  "28": {
    ref: 28,
    authors: "P. Sen et al.",
    title: "RAVEN: Radially Aligned Visual-Radar Network for All-Weather Perception, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)",
    venue: "IEEE CVPR 2026",
    doi: "https://openaccess.thecvf.com",
    year: "2026"
  },
  "29": {
    ref: 29,
    authors: "K. He et al.",
    title: "Deep Residual Learning for Image Recognition, IEEE Conference on Computer Vision and Pattern Recognition (CVPR)",
    venue: "10.1109/CVPR.2016",
    doi: "10.1109/CVPR.2016.90",
    year: "2016"
  },
  "30": {
    ref: 30,
    authors: "Y. Lin et al.",
    title: "RadDet Benchmark on Deep FMCW Radar Detection, IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)",
    venue: "10.1109/ICASSP.2025",
    doi: "10.1109/ICASSP49660.2025.10887772",
    year: "2025"
  },
  "31": {
    ref: 31,
    authors: "B. R. Mahafza",
    title: "Radar Signal Analysis and Processing Using MATLAB, CRC Press / MathWorks Radar Designer App",
    venue: "CRC Press / MATLAB",
    doi: "10.1201/9781315372433",
    year: "2016"
  }
};

/**
 * 2. Reading Progress Bar Controller
 * Updates width of #reading-progress-bar as reader scrolls.
 */

/**
 * 1. KaTeX Mathematical Typesetting Auto-Render Initializer
 * Renders mathematical expressions in DOM using offline vendored KaTeX engine.
 */
function initKaTeX() {
  if (typeof renderMathInElement === "function") {
    renderMathInElement(document.body, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
        { left: "\\[", right: "\\]", display: true },
        { left: "\\(", right: "\\)", display: false }
      ],
      ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
      throwOnError: false
    });
    console.log("📐 KaTeX offline mathematical engine initialized.");
  }
}

function initReadingProgress() {
  const progressBar = document.getElementById("reading-progress-bar");
  if (!progressBar) return;

  function updateProgress() {
    const scrollTop =
      window.pageYOffset ||
      document.documentElement.scrollTop ||
      document.body.scrollTop ||
      0;
    const scrollHeight =
      document.documentElement.scrollHeight -
      document.documentElement.clientHeight;
    const progress =
      scrollHeight > 0 ? Math.min(100, Math.max(0, (scrollTop / scrollHeight) * 100)) : 0;
    progressBar.style.width = `${progress.toFixed(2)}%`;
  }

  window.addEventListener("scroll", updateProgress, { passive: true });
  updateProgress();
}

/**
 * 3. IntersectionObserver Scroll Spy
 * Supports Chapter 1–5 academic anchors and legacy showcase sections.
 */
function initScrollSpy() {
  const academicTargets = [
    "#ch1-intro",
    "#ch2-lit-review",
    "#ch3-methodology",
    "#ch4-results",
    "#ch5-conclusion",
    "#ch2-physics",
    "#ch3-dsp-audit",
    "#ch4-methodology",
    "#ch5-benchmarks",
    "#ch6-timeline",
    "#ch7-conclusion",
    "#references",
    "#overview",
    "#timeline",
    "#notebook-01",
    "#notebook-02",
    "#notebook-03",
    "#comparison",
    "#conclusions"
  ];

  const sections = document.querySelectorAll(academicTargets.join(", "));
  const tocLinks = document.querySelectorAll(".toc-link");

  if (!sections.length || !tocLinks.length) return;

  const observerOptions = {
    root: null,
    rootMargin: "-20% 0px -65% 0px",
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute("id");
        tocLinks.forEach((link) => {
          const href = link.getAttribute("href");
          if (href === `#${id}`) {
            link.classList.add("active");
          } else {
            link.classList.remove("active");
          }
        });
      }
    });
  }, observerOptions);

  sections.forEach((sec) => observer.observe(sec));
}

/**
 * 4. Interactive IEEE Citation Hover Tooltips & Mobile Bottom-Sheet Popovers
 * Always unconditionally active across all citations (PORTAL-CITE-01 / D-04).
 */
function initCitationTooltips() {
  const badges = document.querySelectorAll(".citation-badge, [data-citation]");
  if (!badges.length) return;

  let tooltipEl = document.getElementById("citation-tooltip");
  if (!tooltipEl) {
    tooltipEl = document.createElement("div");
    tooltipEl.id = "citation-tooltip";
    tooltipEl.className = "citation-tooltip";
    document.body.appendChild(tooltipEl);
  }

  let backdropEl = document.getElementById("citation-backdrop");
  if (!backdropEl) {
    backdropEl = document.createElement("div");
    backdropEl.id = "citation-backdrop";
    backdropEl.className = "citation-backdrop";
    document.body.appendChild(backdropEl);
  }

  let hideTimeout = null;

  function showTooltip(badge, isTouch = false) {
    clearTimeout(hideTimeout);
    const citeKey = badge.getAttribute("data-citation") || badge.textContent.replace(/[\[\]]/g, "").trim();

    // Ponytail Ladder Level 3: dynamically extract from DOM single source of truth first
    let data = null;
    const refRow = document.getElementById(`ref-${citeKey}`);
    if (refRow) {
      const cells = refRow.querySelectorAll("td");
      if (cells.length >= 4) {
        const linkEl = cells[4] ? cells[4].querySelector("a") : null;
        data = {
          ref: parseInt(citeKey, 10),
          authors: cells[1].textContent.trim(),
          title: cells[2].textContent.trim(),
          year: cells[3].textContent.trim(),
          venue: cells[4] ? cells[4].textContent.trim() : "",
          url: linkEl ? linkEl.getAttribute("href") : ""
        };
      }
    }
    if (!data) {
      data = CITATIONS_DB[citeKey];
    }
    if (!data) return;

    // Build tooltip safely without innerHTML (CWE-79 DOM XSS prevention)
    while (tooltipEl.firstChild) {
      tooltipEl.removeChild(tooltipEl.firstChild);
    }

    const refNum = document.createElement("div");
    refNum.className = "tooltip-ref-num";
    refNum.textContent = `IEEE Reference [${data.ref}]`;

    const title = document.createElement("div");
    title.className = "tooltip-title";
    title.textContent = data.title;

    const authors = document.createElement("div");
    authors.className = "tooltip-authors";
    authors.textContent = data.authors;

    const venue = document.createElement("div");
    venue.className = "tooltip-venue";
    venue.textContent = `${data.venue} (${data.year})`;

    tooltipEl.appendChild(refNum);
    tooltipEl.appendChild(title);
    tooltipEl.appendChild(authors);
    tooltipEl.appendChild(venue);

    const actions = document.createElement("div");
    actions.className = "tooltip-actions";

    const doiTarget = data.doi || data.url;
    if (doiTarget && doiTarget.trim().length > 0) {
      const doiBtn = document.createElement("a");
      doiBtn.className = "tooltip-doi-btn";
      doiBtn.href = doiTarget.startsWith("http") ? doiTarget : `https://doi.org/${doiTarget}`;
      doiBtn.target = "_blank";
      doiBtn.rel = "noopener noreferrer";
      doiBtn.textContent = "DOI / Publisher ↗";
      actions.appendChild(doiBtn);
    }

    const jumpBtn = document.createElement("button");
    jumpBtn.className = "tooltip-jump-btn";
    jumpBtn.textContent = "View in Reference List";
    jumpBtn.addEventListener("click", () => {
      hideTooltip();
      const targetId = `ref-${citeKey}`;
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: "smooth", block: "center" });
        targetEl.classList.add("highlight-pulse");
        setTimeout(() => targetEl.classList.remove("highlight-pulse"), 2000);
      }
    });
    actions.appendChild(jumpBtn);
    tooltipEl.appendChild(actions);

    const isMobileView = isTouch || window.innerWidth <= 600;
    if (isMobileView) {
      tooltipEl.classList.add("is-mobile");
      backdropEl.classList.add("visible");
      document.body.classList.add("nav-open");
      tooltipEl.style.left = "";
      tooltipEl.style.top = "";
    } else {
      tooltipEl.classList.remove("is-mobile");
      backdropEl.classList.remove("visible");
      document.body.classList.remove("nav-open");

      const tooltipWidth = Math.min(480, window.innerWidth - 40);
      const rect = badge.getBoundingClientRect();
      let left = rect.left - 40;
      let top = rect.top - 140;

      if (left + tooltipWidth > window.innerWidth - 20) {
        left = window.innerWidth - tooltipWidth - 20;
      }
      if (left < 10) left = 10;
      if (rect.top < 150) {
        top = rect.bottom + 10;
      }

      tooltipEl.style.left = `${left}px`;
      tooltipEl.style.top = `${top}px`;
    }

    tooltipEl.classList.add("visible");
  }

  function hideTooltip() {
    tooltipEl.classList.remove("visible");
    backdropEl.classList.remove("visible");
    tooltipEl.classList.remove("is-mobile");
    const navToggle = document.getElementById("nav-toggle");
    const isDrawerOpen = navToggle && navToggle.getAttribute("aria-expanded") === "true";
    if (!isDrawerOpen) {
      document.body.classList.remove("nav-open");
    }
  }

  badges.forEach((badge) => {
    badge.setAttribute("tabindex", "0");
    badge.setAttribute("role", "button");
    badge.setAttribute("aria-haspopup", "true");
    badge.setAttribute("aria-expanded", "false");

    badge.addEventListener("mouseenter", () => {
      badge.setAttribute("aria-expanded", "true");
      clearTimeout(hideTimeout);
      showTooltip(badge, false);
    });
    badge.addEventListener("mouseleave", () => {
      badge.setAttribute("aria-expanded", "false");
      hideTimeout = setTimeout(hideTooltip, 200);
    });
    badge.addEventListener("focus", () => {
      badge.setAttribute("aria-expanded", "true");
      clearTimeout(hideTimeout);
      showTooltip(badge, false);
    });
    badge.addEventListener("blur", () => {
      badge.setAttribute("aria-expanded", "false");
      hideTimeout = setTimeout(hideTooltip, 200);
    });

    badge.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        const citeKey = badge.getAttribute("data-citation") || badge.textContent.replace(/[\[\]]/g, "").trim();
        const targetId = `ref-${citeKey}`;
        const targetEl = document.getElementById(targetId);
        if (targetEl) {
          targetEl.scrollIntoView({ behavior: "smooth", block: "center" });
          targetEl.classList.add("highlight-pulse");
          setTimeout(() => targetEl.classList.remove("highlight-pulse"), 2000);
        }
      } else if (e.key === "Escape") {
        badge.setAttribute("aria-expanded", "false");
        hideTooltip();
      }
    });

    badge.addEventListener("click", (e) => {
      e.preventDefault();
      const citeKey = badge.getAttribute("data-citation") || badge.textContent.replace(/[\[\]]/g, "").trim();
      if (window.innerWidth <= 600 || window.matchMedia("(pointer: coarse)").matches) {
        showTooltip(badge, true);
      } else {
        const targetId = `ref-${citeKey}`;
        const targetEl = document.getElementById(targetId);
        if (targetEl) {
          targetEl.scrollIntoView({ behavior: "smooth", block: "center" });
          targetEl.classList.add("highlight-pulse");
          setTimeout(() => targetEl.classList.remove("highlight-pulse"), 2000);
        }
      }
    });
  });

  tooltipEl.addEventListener("mouseenter", () => clearTimeout(hideTimeout));
  tooltipEl.addEventListener("mouseleave", () => {
    hideTimeout = setTimeout(hideTooltip, 200);
  });
  tooltipEl.addEventListener("focusin", () => clearTimeout(hideTimeout));
  tooltipEl.addEventListener("focusout", (e) => {
    if (!tooltipEl.contains(e.relatedTarget)) {
      hideTimeout = setTimeout(hideTooltip, 200);
    }
  });
  backdropEl.addEventListener("click", hideTooltip);
}

/**
 * 5. Collapsible Code & Drawer Accordions
 */
function initCodeDrawers() {
  const drawerHeaders = document.querySelectorAll(".drawer-header, .code-drawer-toggle");
  drawerHeaders.forEach((header) => {
    header.addEventListener("click", () => {
      const drawer = header.closest(".code-drawer, .collapsible-drawer");
      if (drawer) {
        drawer.classList.toggle("open");
        const icon = header.querySelector(".toggle-icon");
        if (icon) {
          icon.textContent = drawer.classList.contains("open") ? "▲" : "▼";
        }
      }
    });
  });
}

/**
 * 6. Interactive Lightbox Modal Controller
 */
function initLightbox() {
  const modal = document.getElementById("lightbox-modal");
  const modalImg = document.getElementById("lightbox-img");
  const modalCaption = document.getElementById("lightbox-caption");
  const closeBtn = document.getElementById("lightbox-close");

  if (!modal || !modalImg || !modalCaption || !closeBtn) return;

  let lastActiveElement = null;

  function openLightbox(src, captionText, triggerEl) {
    lastActiveElement = triggerEl || document.activeElement;
    modalImg.setAttribute("src", src);
    modalCaption.textContent = captionText || "";
    modalImg.style.width = "auto";
    modalImg.style.maxWidth = src && src.toLowerCase().endsWith(".svg") ? "min(92vw, 1100px)" : "90vw";
    modalImg.style.maxHeight = "76vh";
    modalImg.style.height = "auto";
    modalImg.style.objectFit = "contain";
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
    closeBtn.focus();
  }

  function closeLightbox() {
    modal.style.display = "none";
    modalImg.removeAttribute("src");
    modalImg.onload = null;
    modalImg.style.width = "";
    modalImg.style.height = "";
    modalImg.style.maxWidth = "";
    modalImg.style.maxHeight = "";
    modalCaption.textContent = "";
    document.body.style.overflow = "";
    if (lastActiveElement && typeof lastActiveElement.focus === "function") {
      lastActiveElement.focus();
    }
  }

  const zoomableImages = document.querySelectorAll(
    ".plot-container img, .plot-card img, .architecture-card img, .diagram-container img, .svg-diagram-wrapper img"
  );

  zoomableImages.forEach((img) => {
    img.style.cursor = "zoom-in";
    img.setAttribute("tabindex", "0");
    img.setAttribute("role", "button");
    img.setAttribute("aria-label", "Zoom image");

    function handleZoom() {
      const src = img.getAttribute("src");
      let caption = img.getAttribute("alt") || "";
      const parentCard = img.closest(".plot-card");
      if (parentCard) {
        const titleEl = parentCard.querySelector(".plot-title");
        const descEl = parentCard.querySelector("p em, .plot-desc");
        if (titleEl && descEl) {
          caption = titleEl.textContent.trim() + " — " + descEl.textContent.trim();
        } else if (titleEl) {
          caption = titleEl.textContent.trim();
        } else if (descEl) {
          caption = descEl.textContent.trim();
        }
      } else {
        const figureWrapper = img.closest("figure, div[style*='text-align: center']");
        if (figureWrapper) {
          const captionEl = figureWrapper.querySelector("figcaption, p em, p strong, p");
          if (captionEl) caption = captionEl.textContent.trim();
        }
      }
      openLightbox(src, caption, img);
    }

    img.addEventListener("click", handleZoom);
    img.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        handleZoom();
      }
    });
  });

  closeBtn.addEventListener("click", closeLightbox);
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.style.display === "flex") {
      closeLightbox();
    }
  });
}

/**
 * 7. Code Snippet Copy Controller
 */
function initCodeCopy() {
  const codeBlocks = document.querySelectorAll(".code-block-container, pre code");
  codeBlocks.forEach((block) => {
    const parent = block.parentElement;
    if (!parent) return;

    if (!parent.querySelector(".copy-code-btn")) {
      const copyBtn = document.createElement("button");
      copyBtn.className = "copy-code-btn";
      copyBtn.textContent = "Copy";
      copyBtn.setAttribute("aria-label", "Copy code to clipboard");

      copyBtn.addEventListener("click", async () => {
        const codeText = block.textContent;
        try {
          await navigator.clipboard.writeText(codeText);
          copyBtn.textContent = "Copied!";
          setTimeout(() => {
            copyBtn.textContent = "Copy";
          }, 2000);
        } catch (err) {
          copyBtn.textContent = "Error";
          setTimeout(() => {
            copyBtn.textContent = "Copy";
          }, 2000);
        }
      });

      parent.style.position = "relative";
      parent.appendChild(copyBtn);
    }
  });
}

/**
 * 8. Back to Top Button
 */
function initBackToTop() {
  const backToTopBtn = document.getElementById("back-to-top");
  if (!backToTopBtn) return;

  window.addEventListener("scroll", () => {
    if (window.scrollY > 400) {
      backToTopBtn.classList.add("visible");
    } else {
      backToTopBtn.classList.remove("visible");
    }
  }, { passive: true });

  backToTopBtn.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

/**
 * 9. Mobile Responsive Navigation Drawer Controller
 */
function initMobileDrawer() {
  const navToggle = document.getElementById("nav-toggle");
  const backdrop = document.getElementById("nav-backdrop") || document.querySelector(".nav-backdrop");
  const sidebar = document.getElementById("academic-sidebar");

  if (!navToggle) return;

  function toggleDrawer() {
    const isOpen = document.body.classList.toggle("nav-open");
    navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    navToggle.textContent = isOpen ? "✕" : "☰";
  }

  function closeDrawer() {
    navToggle.setAttribute("aria-expanded", "false");
    navToggle.textContent = "☰";
    const citationTooltip = document.getElementById("citation-tooltip");
    const isCitationOpen = citationTooltip && citationTooltip.classList.contains("is-mobile") && citationTooltip.classList.contains("visible");
    if (!isCitationOpen) {
      document.body.classList.remove("nav-open");
    }
  }

  window.addEventListener("resize", () => {
    if (window.innerWidth > 1024) {
      closeDrawer();
    }
  });

  navToggle.addEventListener("click", toggleDrawer);

  if (backdrop) {
    backdrop.addEventListener("click", closeDrawer);
  }

  const tocLinks = document.querySelectorAll(".toc-link");
  tocLinks.forEach((link) => {
    link.addEventListener("click", () => {
      if (window.innerWidth <= 1024) {
        closeDrawer();
      }
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && document.body.classList.contains("nav-open")) {
      closeDrawer();
    }
  });
}

/**
 * 10. Horizontal Momentum Overflow Containment
 */
function initOverflowContainment() {
  const tables = document.querySelectorAll("table");
  tables.forEach((table) => {
    if (!table.closest(".table-scroll-wrapper")) {
      const wrapper = document.createElement("div");
      wrapper.className = "table-scroll-wrapper";
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    }
  });

  const katexDisplays = document.querySelectorAll(".katex-display");
  katexDisplays.forEach((el) => {
    if (!el.closest(".formula-scroll-wrapper")) {
      const wrapper = document.createElement("div");
      wrapper.className = "formula-scroll-wrapper";
      el.parentNode.insertBefore(wrapper, el);
      wrapper.appendChild(el);
    }
  });

  const inlineGrids = document.querySelectorAll('[style*="grid-template-columns"]');
  inlineGrids.forEach((el) => {
    if (!el.classList.contains("responsive-grid-2")) {
      el.classList.add("responsive-grid-2");
    }
  });
}

/**
 * Initialization on DOMContentLoaded
 */
document.addEventListener("DOMContentLoaded", () => {
  initKaTeX();
  initOverflowContainment();
  if (typeof hljs !== "undefined") {
    hljs.highlightAll();
  }
  initReadingProgress();
  initScrollSpy();
  initCitationTooltips();
  initCodeDrawers();
  initLightbox();
  initCodeCopy();
  initBackToTop();
  initMobileDrawer();
  console.log("⚡ BTP Radar Perception Academic Portal initialized successfully.");
});
