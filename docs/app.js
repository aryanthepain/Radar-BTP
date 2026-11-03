/**
 * BTP Radar Perception & Cognitive EW | Academic Research Showcase
 * Client-Side Application Engine (docs/app.js)
 * Pure Vanilla JavaScript · Zero External Runtime Dependencies (D-01, D-02)
 *
 * Security Mitigations:
 *  - T-01.2.1-03 (CWE-79 / DOM XSS): Strictly uses textContent, setAttribute,
 *    and classList without dynamic innerHTML string evaluation.
 */

"use strict";

/**
 * 1. IntersectionObserver Scroll Spy
 * Dynamically tracks viewport section headers and highlights active navigation link in sidebar.
 */
function initScrollSpy() {
  const sections = document.querySelectorAll(
    "#overview, #timeline, #notebook-01, #notebook-02, #notebook-03, #comparison, #conclusions"
  );
  const tocLinks = document.querySelectorAll(".toc-link");

  if (!sections.length || !tocLinks.length) return;

  const observerOptions = {
    root: null,
    rootMargin: "-20% 0px -70% 0px",
    threshold: 0,
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute("id");
        tocLinks.forEach((link) => {
          if (link.getAttribute("href") === `#${id}`) {
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
 * 2. Interactive Lightbox Modal
 * Provides full-screen zoomed inspection for plots, spectrograms, and architecture SVGs (D-09).
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

  // Attach to zoomable images, flowcharts, and plot cards
  const zoomableImages = document.querySelectorAll(
    "img.zoomable, .flowchart-container img, .plot-img-wrapper img"
  );

  zoomableImages.forEach((img) => {
    img.style.cursor = "zoom-in";
    img.addEventListener("click", () => {
      const src = img.getAttribute("src");
      // Extract caption safely from alt or surrounding card
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

  // Close on backdrop click (outside the image)
  modal.addEventListener("click", (e) => {
    if (e.target === modal || e.target.classList.contains("lightbox-content")) {
      closeLightbox();
    }
  });

  // Close on ESC key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.style.display === "flex") {
      closeLightbox();
    }
  });
}

/**
 * 3. 1-Click Code Copy Handler
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
          // Fallback for older browsers
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
 * 4. Floating Back-to-Top Button
 * Smoothly scrolls user to the top of the presentation when clicked.
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
      behavior: "smooth",
    });
  });
}

/**
 * 5. Responsive Mobile Navigation Drawer
 * Toggles sidebar drawer on touch / mobile viewports (<1024px).
 */
function initMobileDrawer() {
  const toggleBtn = document.getElementById("nav-toggle");
  const sidebar = document.querySelector(".sidebar");
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
  initScrollSpy();
  initLightbox();
  initCodeCopy();
  initBackToTop();
  initMobileDrawer();
  console.log("⚡ BTP Radar Perception Showcase initialized successfully.");
});

