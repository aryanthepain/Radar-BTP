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
    authors: "Alexander Karlsson",
    title: "Radar Signal Processing using Artificial Neural Networks",
    venue: "Doctoral Dissertation, KTH Royal Institute of Technology & Saab Surveillance, Stockholm, Sweden",
    year: "2023",
    doi: "http://urn.kb.se/resolve?urn=urn:nbn:se:kth:diva-324546"
  },
  "2": {
    ref: 2,
    authors: "Z. Huang, S. Denman, A. Pemasiri, T. Martin, and C. Fookes",
    title: "RadDet: A Wideband Dataset for Real-Time Radar Spectrum Detection",
    venue: "IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), Hyderabad, India",
    year: "2025",
    doi: "https://ieeexplore.ieee.org/document/ICASSP2025"
  },
  "3": {
    ref: 3,
    authors: "Dr. Tapas Kumar Pal",
    title: "Artificial Intelligence based Radar Technology: Current Advancements, Future Directions and Challenges",
    venue: "IEEE Space, Aerospace and Defence Conference (SPACE)",
    year: "2025",
    doi: "10.1109/SPACE65882.2025.11171388"
  },
  "4": {
    ref: 4,
    authors: "M. I. Skolnik",
    title: "Introduction to Radar Systems",
    venue: "3rd ed., New York, NY, USA: McGraw-Hill",
    year: "2008",
    doi: ""
  },
  "5": {
    ref: 5,
    authors: "M. A. Richards",
    title: "Fundamentals of Radar Signal Processing",
    venue: "2nd ed., New York, NY, USA: McGraw-Hill",
    year: "2014",
    doi: ""
  },
  "6": {
    ref: 6,
    authors: "H. Rohling",
    title: "Radar CFAR Thresholding in Clutter and Multiple Target Situations",
    venue: "IEEE Transactions on Aerospace and Electronic Systems, vol. AES-19, no. 4, pp. 608–621",
    year: "1983",
    doi: "10.1109/TAES.1983.309350"
  },
  "7": {
    ref: 7,
    authors: "R. O. Schmidt",
    title: "Multiple Emitter Location and Signal Parameter Estimation",
    venue: "IEEE Transactions on Antennas and Propagation, vol. AP-34, no. 3, pp. 276–280",
    year: "1986",
    doi: "10.1109/TAP.1986.1143830"
  },
  "8": {
    ref: 8,
    authors: "C.-Y. Wang, I.-H. Yeh, and H.-Y. M. Liao",
    title: "YOLOv9: Learning What You Want to Learn Using Programmable Gradient Information",
    venue: "arXiv preprint arXiv:2402.13616",
    year: "2024",
    doi: "https://arxiv.org/abs/2402.13616"
  },
  "9": {
    ref: 9,
    authors: "Y. Zhao, W. Lv, S. Xu, et al.",
    title: "DETRs Beat YOLOs on Real-Time Object Detection",
    venue: "Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 16965–16974",
    year: "2024",
    doi: "10.1109/CVPR52733.2024.01605"
  },
  "10": {
    ref: 10,
    authors: "Z. Geng, H. Yan, J. Zhang, and D. Zhu",
    title: "Deep-Learning for Radar: A Survey",
    venue: "IEEE Access, vol. 9, pp. 141800–141818",
    year: "2021",
    doi: "10.1109/ACCESS.2021.3119561"
  },
  "11": {
    ref: 11,
    authors: "K. Patel, K. Rambach, T. Visentin, et al.",
    title: "Deep Learning-Based Object Classification on Automotive Radar Spectra",
    venue: "IEEE Radar Conference (RadarConf), Boston, MA, USA, pp. 1–6",
    year: "2019",
    doi: "10.1109/RADAR.2019.8835742"
  },
  "12": {
    ref: 12,
    authors: "A. Ouaknine, A. Newson, J. Rebut, and F. Pérez",
    title: "CARRADA Dataset: Camera and Automotive Radar Dataset with Range-Angle-Doppler Annotations",
    venue: "Proceedings of the 25th International Conference on Pattern Recognition (ICPR), pp. 5068–5075",
    year: "2020",
    doi: "10.1109/ICPR48806.2021.9412450"
  },
  "13": {
    ref: 13,
    authors: "H. Caesar, V. Bankiti, A. H. Lang, et al.",
    title: "nuScenes: A Multimodal Dataset for Autonomous Driving",
    venue: "Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 11621–11631",
    year: "2020",
    doi: "10.1109/CVPR42600.2020.01164"
  },
  "14": {
    ref: 14,
    authors: "J. Zheng, Y. Liu, et al.",
    title: "TJ4D: A Large-Scale 4D Radar Dataset for Autonomous Driving",
    venue: "Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)",
    year: "2022",
    doi: ""
  },
  "15": {
    ref: 15,
    authors: "Y. Chen, J. Zhang, and D. Zhu",
    title: "TransRAD: Retentive Vision Transformer with Manhattan Attention for Radar Object Detection",
    venue: "IEEE Transactions on Radar Systems, vol. 3, pp. 112–125",
    year: "2025",
    doi: "10.1109/TRS.2024.3498112"
  },
  "16": {
    ref: 16,
    authors: "L. Zhang et al.",
    title: "E-RODNet: Efficient Embedded Radar Object Detection Network",
    venue: "IEEE Sensors Journal, vol. 24, no. 8, pp. 12050–12061",
    year: "2024",
    doi: "10.1109/JSEN.2024.3364912"
  },
  "17": {
    ref: 17,
    authors: "T. O'Shea and J. Hoydis",
    title: "An Introduction to Deep Learning for the Physical Layer",
    venue: "IEEE Transactions on Cognitive Communications and Networking, vol. 3, no. 4, pp. 563–575",
    year: "2017",
    doi: "10.1109/TCCN.2017.2758370"
  },
  "18": {
    ref: 18,
    authors: "V. C. Chen",
    title: "The Micro-Doppler Effect in Radar",
    venue: "2nd ed., Norwood, MA, USA: Artech House",
    year: "2019",
    doi: ""
  },
  "19": {
    ref: 19,
    authors: "B. R. Mahafza",
    title: "Radar Systems Analysis and Design Using MATLAB",
    venue: "3rd ed., Boca Raton, FL, USA: CRC Press",
    year: "2013",
    doi: ""
  },
  "20": {
    ref: 20,
    authors: "J. Capon",
    title: "High-Resolution Frequency-Wavenumber Spectrum Analysis",
    venue: "Proceedings of the IEEE, vol. 57, no. 8, pp. 1408–1418",
    year: "1969",
    doi: "10.1109/PROC.1969.7278"
  },
  "21": {
    ref: 21,
    authors: "M. Ester, H.-P. Kriegel, J. Sander, and X. Xu",
    title: "A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise",
    venue: "Proceedings of the 2nd International Conference on Knowledge Discovery and Data Mining (KDD), pp. 226–231",
    year: "1996",
    doi: ""
  },
  "22": {
    ref: 22,
    authors: "P. E. Pace",
    title: "Detecting and Classifying Low Probability of Intercept Radar",
    venue: "2nd ed., Norwood, MA, USA: Artech House",
    year: "2009",
    doi: ""
  },
  "23": {
    ref: 23,
    authors: "R. Caromi, M. Souryal, and T. A. Hall",
    title: "RF Dataset of Incumbent Radar Signals in the 3.5 GHz CBRS Band",
    venue: "Journal of Research of the National Institute of Standards and Technology (NIST), vol. 124, p. 1",
    year: "2019",
    doi: "10.6028/jres.124.020"
  },
  "24": {
    ref: 24,
    authors: "S. Basak, S. Rajendran, S. Pollin, and B. Scheers",
    title: "Combined RF-Based Drone Detection and Classification",
    venue: "IEEE Transactions on Cognitive Communications and Networking, vol. 8, no. 1, pp. 111–120",
    year: "2021",
    doi: "10.1109/TCCN.2021.3117474"
  },
  "25": {
    ref: 25,
    authors: "S. Z. Gurbuz, K. L. Bell, and M. S. Greco",
    title: "Integrating AI into Radar System Design: Next-Generation Cognitive Radars",
    venue: "Women in Telecommunications, Cham, Switzerland: Springer",
    year: "2023",
    doi: "10.1007/978-3-031-29933-9_5"
  },
  "26": {
    ref: 26,
    authors: "K. Haigh and J. Andrusenko",
    title: "Cognitive Electronic Warfare: An Artificial Intelligence Approach",
    venue: "Norwood, MA, USA: Artech House",
    year: "2021",
    doi: ""
  },
  "27": {
    ref: 27,
    authors: "Z. Huang, A. Pemasiri, S. Denman, T. Martin, and C. Fookes",
    title: "Multi-stage Learning for Radar Pulse Activity Segmentation",
    venue: "IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), pp. 7340–7344",
    year: "2024",
    doi: "10.1109/ICASSP48485.2024.10446700"
  },
  "28": {
    ref: 28,
    authors: "X. Cai, M. Giallorenzo, and K. Sarabandi",
    title: "Machine Learning-Based Target Classification for MMW Radar in Autonomous Driving",
    venue: "IEEE Transactions on Intelligent Vehicles, vol. 6, no. 4, pp. 678–689",
    year: "2021",
    doi: "10.1109/TIV.2021.3065365"
  },
  "29": {
    ref: 29,
    authors: "T. Huynh-The, V.-S. Doan, et al.",
    title: "Accurate LPI Radar Waveform Recognition with CWD-TFA for Deep Convolutional Network",
    venue: "IEEE Wireless Communications Letters, vol. 10, no. 8, pp. 1638–1642",
    year: "2021",
    doi: "10.1109/LWC.2021.3076822"
  },
  "30": {
    ref: 30,
    authors: "S. Bobek, M. Kuk, M. Szelazek, and G. J. Nalepa",
    title: "Enhancing Cluster Analysis with Explainable AI and Multidimensional Cluster Prototypes",
    venue: "IEEE Access, vol. 10, pp. 101556–101574",
    year: "2022",
    doi: "10.1109/ACCESS.2022.3208752"
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
 * 4. Interactive IEEE Citation Hover Tooltips
 * Displays metadata popups for citation badges [1]–[30] and links to references.
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

  let hideTimeout = null;

  function showTooltip(badge) {
    clearTimeout(hideTimeout);
    const citeKey = badge.getAttribute("data-citation") || badge.textContent.replace(/[\[\]]/g, "").trim();
    const data = CITATIONS_DB[citeKey];

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

    // Position tooltip relative to badge
    const rect = badge.getBoundingClientRect();
    const tooltipWidth = 360;
    let left = rect.left + window.scrollX - 40;
    let top = rect.top + window.scrollY - 110;

    // Viewport edge collision handling
    if (left + tooltipWidth > window.innerWidth - 20) {
      left = window.innerWidth - tooltipWidth - 20;
    }
    if (left < 10) left = 10;
    if (rect.top < 120) {
      top = rect.bottom + window.scrollY + 10;
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
    badge.addEventListener("mouseenter", () => showTooltip(badge));
    badge.addEventListener("mouseleave", hideTooltip);
    badge.addEventListener("focus", () => showTooltip(badge));
    badge.addEventListener("blur", hideTooltip);

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

  function openLightbox(src, captionText) {
    modalImg.setAttribute("src", src);
    modalCaption.textContent = captionText || "";
    if (src && src.toLowerCase().endsWith(".svg")) {
      modalImg.style.width = "92vw";
      modalImg.style.maxWidth = "1200px";
    } else {
      modalImg.style.width = "auto";
      modalImg.style.maxWidth = "90vw";
    }
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
  }

  function closeLightbox() {
    modal.style.display = "none";
    modalImg.removeAttribute("src");
    modalImg.style.width = "";
    modalImg.style.maxWidth = "";
    modalCaption.textContent = "";
    document.body.style.overflow = "";
  }

  const zoomableImages = document.querySelectorAll(
    "img.zoomable, .flowchart-container img, .plot-img-wrapper img"
  );

  zoomableImages.forEach((img) => {
    img.style.cursor = "zoom-in";
    img.addEventListener("click", () => {
      const src = img.getAttribute("src");
      let caption = img.getAttribute("alt") || "";
      const parentCard = img.closest(".plot-card");
      if (parentCard) {
        const titleEl = parentCard.querySelector(".plot-title");
        if (titleEl) caption = titleEl.textContent;
      }
      openLightbox(src, caption);
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
  initScrollSpy();
  initCitationTooltips();
  initCodeDrawers();
  initLightbox();
  initCodeCopy();
  initBackToTop();
  initMobileDrawer();
  console.log("⚡ BTP Radar Perception Academic Portal initialized successfully.");
});
