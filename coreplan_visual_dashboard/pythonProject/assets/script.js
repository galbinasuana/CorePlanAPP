document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        const exportBtn = document.getElementById("export-pdf-icon");

        if (exportBtn) {
            exportBtn.addEventListener("click", function () {
                const title = document.querySelector(".canvas-title");
                if (title) title.style.display = "none";

                // Creează un header pentru print
                const header = document.createElement("div");
                header.className = "print-header";

                const titleEl = document.createElement("h1");
                titleEl.className = "print-title";
                titleEl.textContent = "📊 Custom Dashboard Report";

                const dateEl = document.createElement("p");
                dateEl.className = "print-date";

                const now = new Date();
                const options = { year: 'numeric', month: 'long', day: 'numeric' };
                dateEl.textContent = "Generated on: " + now.toLocaleDateString('en-US', options);

                header.appendChild(titleEl);
                header.appendChild(dateEl);

                const canvasArea = document.getElementById("canvas-area");
                if (canvasArea) {
                    canvasArea.parentNode.insertBefore(header, canvasArea);
                }

                // ✅ Adaugă footer cu paginare
                const footer = document.createElement("div");
                footer.className = "print-footer";
                document.body.appendChild(footer);

                // Trigger print
                window.print();

                // Cleanup după print
                setTimeout(() => {
                    if (title) title.style.display = "block";
                    if (header && header.parentNode) header.parentNode.removeChild(header);
                    if (footer && footer.parentNode) footer.parentNode.removeChild(footer);
                }, 2000);
            });
        }
    }, 1000);
});
