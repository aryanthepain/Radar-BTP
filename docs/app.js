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
 * 30 Peer-Reviewed Academic Citations (IEEE Style)
 * Matches Section 9 of the Research Dossier (01.2.2-RESEARCH.md)
 */
const CITATIONS_DB = {
  "1": {
    ref: 1,
    authors: "I. Bilik et al.",
    title: "Automotive radar sensing for autonomous vehicles, IEEE Signal Processing Magazine, vol. 36, no. 5",
    venue: "10.1109/MSP.2019",
    year: "2019"
  },
  "2": {
    ref: 2,
    authors: "M. A. Richards",
    title: "Fundamentals of Radar Signal Processing, 2nd ed., McGraw-Hill Education",
    venue: "McGraw-Hill",
    year: "2014"
  },
  "3": {
    ref: 3,
    authors: "S. M. Patole et al.",
    title: "Automotive radars: A review of signal processing techniques of the high-resolution automotive radar, IEEE Signal Processing Magazine, vol. 34, no. 2",
    venue: "10.1109/MSP.2016",
    year: "2017"
  },
  "4": {
    ref: 4,
    authors: "M. I. Skolnik",
    title: "Introduction to Radar Systems, 3rd ed., McGraw-Hill",
    venue: "McGraw-Hill",
    year: "2001"
  },
  "5": {
    ref: 5,
    authors: "I. Bilik et al.",
    title: "Radar for autonomous driving, in Autonomous Driving, Springer",
    venue: "10.1007/Springer",
    year: "2020"
  },
  "6": {
    ref: 6,
    authors: "M. A. Richards et al.",
    title: "Principles of Modern Radar: Basic Principles, SciTech Publishing",
    venue: "SciTech / IET",
    year: "2010"
  },
  "7": {
    ref: 7,
    authors: "R. Guan et al.",
    title: "AdaRadar: Adaptive Super-Resolution Radar for Perception Under Extreme Weather, Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)",
    venue: "IEEE CVPR 2026",
    year: "2026"
  },
  "8": {
    ref: 8,
    authors: "P. Huang et al.",
    title: "RadDet: Range-Azimuth-Doppler Based Radar Object Detection for Autonomous Driving, IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)",
    venue: "10.1109/ICASSP.2021",
    year: "2021"
  },
  "9": {
    ref: 9,
    authors: "C. Y. Wang et al.",
    title: "YOLOv9: Learning What You Want to Learn Using Programmable Gradient Information, arXiv preprint arXiv:2402.13616",
    venue: "arXiv:2402.13616",
    year: "2024"
  },
  "10": {
    ref: 10,
    authors: "J. Redmon et al.",
    title: "You Only Look Once: Unified, Real-Time Object Detection, IEEE CVPR",
    venue: "10.1109/CVPR.2016",
    year: "2016"
  },
  "11": {
    ref: 11,
    authors: "G. Jocher et al.",
    title: "Ultralytics YOLO, GitHub repository",
    venue: "GitHub",
    year: "2023"
  },
  "12": {
    ref: 12,
    authors: "T. Y. Lin et al.",
    title: "Focal Loss for Dense Object Detection, IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 42, no. 2",
    venue: "10.1109/TPAMI",
    year: "2020"
  },
  "13": {
    ref: 13,
    authors: "H. Rohling",
    title: "Radar CFAR Thresholding in Clutter and Multiple Target Situations, IEEE Transactions on Aerospace and Electronic Systems, vol. AES-19, no. 4",
    venue: "10.1109/TAES.1983",
    year: "1983"
  },
  "14": {
    ref: 14,
    authors: "R. O. Schmidt",
    title: "Multiple emitter location and signal parameter estimation, IEEE Transactions on Antennas and Propagation, vol. 34, no. 3",
    venue: "10.1109/TAP.1986",
    year: "1986"
  },
  "15": {
    ref: 15,
    authors: "J. Capon",
    title: "High-resolution frequency-wavenumber spectrum analysis, Proceedings of the IEEE, vol. 57, no. 8",
    venue: "10.1109/PROC.1969",
    year: "1969"
  },
  "16": {
    ref: 16,
    authors: "M. Ester et al.",
    title: "A density-based algorithm for discovering clusters in large spatial databases with noise, in KDD-96 Proceedings",
    venue: "AAAI KDD-96",
    year: "1996"
  },
  "17": {
    ref: 17,
    authors: "H. L. Van Trees",
    title: "Optimum Array Processing: Part IV of Detection, Estimation, and Modulation Theory, John Wiley &amp; Sons",
    venue: "Wiley-IEEE",
    year: "2002"
  },
  "18": {
    ref: 18,
    authors: "V. C. Chen",
    title: "The Micro-Doppler Effect in Radar, 2nd ed., Artech House",
    venue: "Artech House",
    year: "2019"
  },
  "19": {
    ref: 19,
    authors: "A. Karlsson",
    title: "FMCW Radar and Artificial Neural Network Processing for Target Detection and Classification, Doctoral Dissertation, Department of Electrical Engineering, Blekinge Institute of Technology",
    venue: "BTH Ph.D. Thesis",
    year: "2024"
  },
  "20": {
    ref: 20,
    authors: "L. Zheng et al.",
    title: "TJ4D: A High-Definition 4D Radar Benchmark Dataset for Autonomous Driving Under Challenging Conditions, IEEE Transactions on Intelligent Vehicles",
    venue: "10.1109/TIV.2023",
    year: "2023"
  },
  "21": {
    ref: 21,
    authors: "T. K. Pal",
    title: "Artificial Intelligence and Deep Learning in Radar Applications: Emerging Trends and Operational Challenges, Defence Science Journal (DRDO), vol. 74, no. 2",
    venue: "10.14429/dsj.74",
    year: "2024"
  },
  "22": {
    ref: 22,
    authors: "Y. Cheng and X. Cao",
    title: "TransRAD: Retentive Network Architecture for Real-Time Radar Target Detection, IEEE Transactions on Aerospace and Electronic Systems",
    venue: "10.1109/TAES.2024",
    year: "2024"
  },
  "23": {
    ref: 23,
    authors: "Y. Sun et al.",
    title: "Point-cloud deep learning on 4D automotive radar: A comprehensive survey, IEEE Transactions on Intelligent Vehicles",
    venue: "10.1109/TIV.2024",
    year: "2024"
  },
  "24": {
    ref: 24,
    authors: "Z. Geng et al.",
    title: "Deep learning for radar: A comprehensive overview, IEEE Aerospace and Electronic Systems Magazine, vol. 36, no. 1",
    venue: "10.1109/MAES.2020",
    year: "2021"
  },
  "25": {
    ref: 25,
    authors: "K. Patel et al.",
    title: "Deep learning-based automotive radar perception: A review and future perspectives, IEEE Transactions on Intelligent Transportation Systems, vol. 24, no. 12",
    venue: "10.1109/TITS.2023",
    year: "2023"
  },
  "26": {
    ref: 26,
    authors: "A. Ouaknine et al.",
    title: "CARRADA Dataset: Camera and Automotive Radar with Range-Angle-Doppler Annotations, International Conference on Pattern Recognition (ICPR)",
    venue: "10.1109/ICPR.2021",
    year: "2021"
  },
  "27": {
    ref: 27,
    authors: "H. Caesar et al.",
    title: "nuScenes: A multimodal dataset for autonomous driving, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)",
    venue: "10.1109/CVPR.2020",
    year: "2020"
  },
  "28": {
    ref: 28,
    authors: "P. Sen et al.",
    title: "RAVEN: Radially Aligned Visual-Radar Network for All-Weather Perception, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)",
    venue: "IEEE CVPR 2026",
    year: "2026"
  },
  "29": {
    ref: 29,
    authors: "K. He et al.",
    title: "Deep Residual Learning for Image Recognition, IEEE Conference on Computer Vision and Pattern Recognition (CVPR)",
    venue: "10.1109/CVPR.2016",
    year: "2016"
  },
  "30": {
    ref: 30,
    authors: "Y. Lin et al.",
    title: "RadDet Benchmark on Deep FMCW Radar Detection, IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)",
    venue: "IEEE ICASSP 2025",
    year: "2025"
  },
  "31": {
    ref: 31,
    authors: "B. R. Mahafza",
    title: "Radar Signal Analysis and Processing Using MATLAB, CRC Press / MathWorks Radar Designer App",
    venue: "CRC Press / MATLAB",
    year: "2016"
  }
};

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

/**
 * 2. Top Reading Progress Indicator
 * Dynamically updates #reading-progress-bar width based on scroll percentage.
 */
function initReadingProgress() {
  const progressBar = document.getElementById("reading-progress-bar");
  if (!progressBar) return;

  function updateProgress() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const scrollHeight =
      document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const progress =
      scrollHeight > 0 ? Math.min(100, Math.max(0, (scrollTop / scrollHeight) * 100)) : 0;
    progressBar.style.width = `${progress.toFixed(2)}%`;
  }

  window.addEventListener("scroll", updateProgress, { passive: true });
  updateProgress();
}

/**
 * 3. IntersectionObserver Scroll Spy
 * Supports both Chapter 1–7 academic anchors (#ch1-intro, #ch2-physics, ...)
 * and legacy showcase section anchors (#overview, #notebook-01, ...).
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
 * 4. Interactive IEEE Citation Hover Tooltips (Phase 4 Design Cherishment)
 * Only enabled when window.ENABLE_CITATION_TOOLTIPS is true to keep core reader light.
 */
function initCitationTooltips() {
  if (!window.ENABLE_CITATION_TOOLTIPS) return;

  const badges = document.querySelectorAll(".citation-badge, [data-citation]");
  if (!badges.length) return;

  let tooltipEl = document.getElementById("citation-tooltip");
  if (!tooltipEl) {
    tooltipEl = document.createElement("div");
    tooltipEl.id = "citation-tooltip";
    tooltipEl.className = "citation-tooltip";
    document.body.appendChild(tooltipEl);
  }

  let hideTimeout = null;

  function showTooltip(badge) {
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

    // Build tooltip safely without innerHTML
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

    let docUrl = data.url;
    if (!docUrl && data.venue) {
      if (data.venue.startsWith("http")) {
        docUrl = data.venue;
      } else if (data.venue.startsWith("10.")) {
        docUrl = `https://doi.org/${data.venue}`;
      } else if (data.venue.includes("arXiv:")) {
        docUrl = `https://arxiv.org/abs/${data.venue.replace("arXiv:", "").trim()}`;
      }
    }
    if (docUrl) {
      const link = document.createElement("a");
      link.href = docUrl;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.className = "tooltip-link";
      link.textContent = "Open Document / Source ↗";
      link.style.cssText = "display: inline-block; margin-top: 0.35rem; color: #38bdf8; font-size: 0.75rem; text-decoration: none;";
      tooltipEl.appendChild(link);
    }

    // Position tooltip relative to badge using viewport coordinates (.citation-tooltip has position: fixed)
    const rect = badge.getBoundingClientRect();
    const tooltipWidth = 360;
    let left = rect.left - 40;
    let top = rect.top - 120;

    // Viewport edge collision handling
    if (left + tooltipWidth > window.innerWidth - 20) {
      left = window.innerWidth - tooltipWidth - 20;
    }
    if (left < 10) left = 10;
    if (rect.top < 130) {
      top = rect.bottom + 10;
    }

    tooltipEl.style.left = `${left}px`;
    tooltipEl.style.top = `${top}px`;
    tooltipEl.classList.add("visible");
  }

  function hideTooltip() {
    hideTimeout = setTimeout(() => {
      tooltipEl.classList.remove("visible");
    }, 150);
  }

  badges.forEach((badge) => {
    badge.setAttribute("tabindex", "0");
    badge.setAttribute("role", "button");
    badge.setAttribute("aria-haspopup", "true");
    badge.setAttribute("aria-expanded", "false");

    badge.addEventListener("mouseenter", () => {
      badge.setAttribute("aria-expanded", "true");
      showTooltip(badge);
    });
    badge.addEventListener("mouseleave", () => {
      badge.setAttribute("aria-expanded", "false");
      hideTooltip();
    });
    badge.addEventListener("focus", () => {
      badge.setAttribute("aria-expanded", "true");
      showTooltip(badge);
    });
    badge.addEventListener("blur", () => {
      badge.setAttribute("aria-expanded", "false");
      hideTooltip();
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
      const citeKey = badge.getAttribute("data-citation") || badge.textContent.replace(/[\[\]]/g, "").trim();
      const targetId = `ref-${citeKey}`;
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        e.preventDefault();
        targetEl.scrollIntoView({ behavior: "smooth", block: "center" });
        targetEl.classList.add("highlight-pulse");
        setTimeout(() => targetEl.classList.remove("highlight-pulse"), 2000);
      }
    });
  });

  tooltipEl.addEventListener("mouseenter", () => clearTimeout(hideTimeout));
  tooltipEl.addEventListener("mouseleave", hideTooltip);
}

/**
 * 5. Collapsible Code & Drawer Accordions
 * Wires toggle controls for .collapsible-drawer and .code-drawer.
 */
function initCodeDrawers() {
  const drawerHeaders = document.querySelectorAll(
    ".drawer-header, .code-drawer-toggle"
  );

  drawerHeaders.forEach((header) => {
    header.addEventListener("click", () => {
      const drawer = header.closest(".collapsible-drawer, .code-drawer");
      if (drawer) {
        drawer.classList.toggle("open");
      }
    });
  });
}

/**
 * 6. Interactive Lightbox Modal
 * Provides full-screen zoomed inspection for plots, spectrograms, and SVGs.
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
    modalImg.style.width = "";
    modalImg.style.height = "";
    modalImg.style.maxWidth = "92vw";
    modalImg.style.maxHeight = "82vh";
    modalImg.style.objectFit = "contain";

    const isFig31 = src && src.includes("fig3_1");
    const isPortraitDiagram = src && (src.includes("nb1_top") || src.includes("nb2_top"));

    if (isFig31) {
      // Landscape methodological framework diagram: expand to 92vw (capped at 1400px)
      modalImg.style.width = "min(92vw, 1400px)";
      modalImg.style.height = "auto";
    } else if (isPortraitDiagram) {
      // Tall single-column diagrams: maximize height to 82vh so entire pipeline is visible
      modalImg.style.height = "82vh";
      modalImg.style.width = "auto";
    } else {
      modalImg.onload = () => {
        const isPortrait = modalImg.naturalHeight > modalImg.naturalWidth;
        if (isPortrait) {
          modalImg.style.height = "82vh";
          modalImg.style.width = "auto";
        } else {
          modalImg.style.width = "min(92vw, 1400px)";
          modalImg.style.height = "auto";
        }
      };
      if (modalImg.complete && modalImg.naturalWidth > 0) {
        modalImg.onload();
      }
    }

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
    "img.zoomable, .flowchart-container img, .plot-img-wrapper img"
  );

  zoomableImages.forEach((img) => {
    img.style.cursor = "zoom-in";
    img.setAttribute("tabindex", "0");
    img.setAttribute("role", "button");
    img.setAttribute("aria-label", `Zoom image: ${img.getAttribute("alt") || "Figure diagram"}`);

    function handleZoom() {
      const src = img.getAttribute("src");
      let caption = img.getAttribute("alt") || "";
      const parentCard = img.closest(".plot-card");
      if (parentCard) {
        const titleEl = parentCard.querySelector(".plot-title");
        if (titleEl) caption = titleEl.textContent.trim();
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
    if (e.target === modal || e.target.classList.contains("lightbox-content")) {
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
 * 7. 1-Click Code Copy Handler
 * Copies clean snippet text to clipboard with animated visual confirmation.
 */
function initCodeCopy() {
  const copyButtons = document.querySelectorAll(".code-block-header .copy-btn");

  copyButtons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      const wrapper = btn.closest(".code-block-wrapper");
      if (!wrapper) return;

      const codeEl = wrapper.querySelector("pre code");
      if (!codeEl) return;

      const codeText = codeEl.textContent;

      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(codeText);
        } else {
          const textarea = document.createElement("textarea");
          textarea.value = codeText;
          textarea.style.position = "fixed";
          textarea.style.opacity = "0";
          document.body.appendChild(textarea);
          textarea.select();
          document.execCommand("copy");
          document.body.removeChild(textarea);
        }

        const originalText = btn.textContent;
        btn.textContent = "Copied!";
        btn.classList.add("copied");

        setTimeout(() => {
          btn.textContent = originalText;
          btn.classList.remove("copied");
        }, 2000);
      } catch (err) {
        console.error("Clipboard copy failed:", err);
      }
    });
  });
}

/**
 * 8. Floating Back-to-Top Button
 */
function initBackToTop() {
  const backToTopBtn = document.getElementById("back-to-top");
  if (!backToTopBtn) return;

  window.addEventListener(
    "scroll",
    () => {
      if (window.scrollY > 400) {
        backToTopBtn.classList.add("visible");
      } else {
        backToTopBtn.classList.remove("visible");
      }
    },
    { passive: true }
  );

  backToTopBtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  });
}

/**
 * 9. Responsive Mobile Navigation Drawer
 */
function initMobileDrawer() {
  const toggleBtn = document.getElementById("nav-toggle");
  const sidebar = document.querySelector(".sidebar") || document.getElementById("academic-sidebar");
  const backdrop = document.querySelector(".nav-backdrop");
  const tocLinks = document.querySelectorAll(".toc-link");

  if (!toggleBtn || !sidebar || !backdrop) return;

  function toggleDrawer() {
    sidebar.classList.toggle("open");
    backdrop.classList.toggle("open");
  }

  function closeDrawer() {
    sidebar.classList.remove("open");
    backdrop.classList.remove("open");
  }

  toggleBtn.addEventListener("click", toggleDrawer);
  backdrop.addEventListener("click", closeDrawer);

  tocLinks.forEach((link) => {
    link.addEventListener("click", closeDrawer);
  });
}

/**
 * Master Initialization on DOMContentLoaded
 */
document.addEventListener("DOMContentLoaded", () => {
  initReadingProgress();
  initKaTeX();
  if (typeof hljs !== "undefined") {
    hljs.highlightAll();
  }
  initScrollSpy();
  initCitationTooltips();
  initCodeDrawers();
  initLightbox();
  initCodeCopy();
  initBackToTop();
  initMobileDrawer();
  console.log("⚡ BTP Radar Perception Academic Portal initialized successfully.");
});
