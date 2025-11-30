async function showResults(data) {
  const container = document.getElementById("results");
  container.innerHTML = "";
  if (!data) {
    container.innerText = "No data.";
    return;
  }
  if (data.error) {
    container.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
    return;
  }
  const list = data.recommendations || [];
  if (list.length === 0) {
    container.innerHTML =
      '<div class="alert alert-info">No recommendations found.</div>';
    return;
  }
  const ul = document.createElement("div");
  ul.className = "list-group";
  list.forEach((item) => {
    const el = document.createElement("div");
    el.className = "list-group-item";
    el.innerHTML = `<div class="fw-bold">${
      item.title
    } <small class="text-muted">(${item.year || "N/A"})</small></div>
                        <div class="small">${item.genres || ""}</div>
                        <div class="mt-1">${
                          item.overview ? item.overview.substring(0, 200) : ""
                        }</div>`;
    ul.appendChild(el);
  });
  container.appendChild(ul);
}

document.getElementById("titleForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("titleInput").value;
  const n = document.getElementById("titleN").value || 5;
  if (!title) {
    alert("Enter a title");
    return;
  }
  const res = await fetch(
    `/recommend?title=${encodeURIComponent(title)}&n=${n}`
  );
  const data = await res.json();
  showResults(data);
});

document.getElementById("plotForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const plot = document.getElementById("plotInput").value;
  const n = document.getElementById("plotN").value || 5;
  if (!plot) {
    alert("Paste a plot");
    return;
  }
  const res = await fetch("/recommend_text", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ plot: plot, n: n }),
  });
  const data = await res.json();
  showResults(data);
});
