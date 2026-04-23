document.getElementById("submitBtn").addEventListener("click", async () => {
  const question = document.getElementById("questionInput").value.trim();
  const responseContainer = document.getElementById("responseContainer");
  const loading = document.getElementById("loading");

  if (!question) return;

  loading.classList.remove("hidden");
  responseContainer.textContent = "";

  const res = await fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });

  const data = await res.json();
  loading.classList.add("hidden");

  typeResponse(responseContainer, data.answer || "No response received.");
});

function typeResponse(container, text, speed = 25) {
  let i = 0;
  const interval = setInterval(() => {
    container.textContent += text.charAt(i);
    i++;
    if (i >= text.length) clearInterval(interval);
  }, speed);
}

document.getElementById("question-form").addEventListener("submit", function (e) {
    document.getElementById("form-box").style.display = "none";
    document.getElementById("loading-section").style.display = "flex";
});
