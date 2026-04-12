(function () {
    function setupImageZoom() {
        const zoomableImages = Array.from(document.querySelectorAll("img.tap-zoom"));
        if (zoomableImages.length === 0) {
            return;
        }

        const lightbox = document.createElement("div");
        lightbox.className = "image-lightbox";
        lightbox.setAttribute("role", "dialog");
        lightbox.setAttribute("aria-modal", "true");
        lightbox.setAttribute("aria-label", "Image preview");

        const closeButton = document.createElement("button");
        closeButton.className = "image-lightbox-close";
        closeButton.type = "button";
        closeButton.setAttribute("aria-label", "Close image preview");
        closeButton.textContent = "x";

        const preview = document.createElement("img");
        preview.alt = "";

        const hint = document.createElement("p");
        hint.className = "image-lightbox-hint";
        hint.textContent = "Tap outside the image to close";

        lightbox.appendChild(closeButton);
        lightbox.appendChild(preview);
        lightbox.appendChild(hint);
        document.body.appendChild(lightbox);

        function closeLightbox() {
            lightbox.classList.remove("is-open");
            preview.removeAttribute("src");
            document.body.style.overflow = "";
        }

        function openLightbox(sourceImage) {
            preview.src = sourceImage.currentSrc || sourceImage.src;
            preview.alt = sourceImage.alt || "Volunteer submission image";
            lightbox.classList.add("is-open");
            document.body.style.overflow = "hidden";
        }

        zoomableImages.forEach(function (img) {
            if (!img.hasAttribute("tabindex")) {
                img.setAttribute("tabindex", "0");
            }

            img.addEventListener("click", function () {
                openLightbox(img);
            });

            img.addEventListener("keydown", function (event) {
                if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    openLightbox(img);
                }
            });
        });

        closeButton.addEventListener("click", closeLightbox);

        lightbox.addEventListener("click", function (event) {
            if (event.target === lightbox) {
                closeLightbox();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && lightbox.classList.contains("is-open")) {
                closeLightbox();
            }
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", setupImageZoom);
    } else {
        setupImageZoom();
    }
})();
