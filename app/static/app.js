function buildRequest() {
  const req = {
    origin: document.getElementById("origin").value.trim(),
    destination: document.getElementById("destination").value.trim(),
    depart_after: document.getElementById("depart_after").value.trim(),
    arrive_before: document.getElementById("arrive_before").value.trim(),
    max_layovers: Number(document.getElementById("max_layovers").value),
    optimize_for: document.getElementById("optimize_for").value,
  };

  return req;
}

function setStatus(msg) {
  document.getElementById("status").textContent = msg || "";
}

function renderResults(data) {
  const el = document.getElementById("results");
  el.innerHTML = "";

  const plans = data?.plans || [];
  if (!Array.isArray(plans) || plans.length === 0) {
    el.innerHTML = `<div class="muted">No plans returned.</div>`;
    return;
  }

  for (const p of plans) {
    const score = p.score ?? "—";
    const price = p.metrics?.total_price_gbp ?? "—";
    const duration = p.metrics?.total_duration_minutes ?? "—";
    const emissions = p.metrics?.total_emissions_kg ?? "—";
    const risk = p.metrics?.risk_score ?? "—";
    const legs = p.legs ?? [];

    const card = document.createElement("div");
    card.className = "result";

    const legsHtml = Array.isArray(legs)
      ? legs.map(l => {
          const from = l.origin ?? "?";
          const to = l.destination ?? "?";
          const provider = l.provider ?? "provider";
          const mins = l.duration_minutes ?? "";
          const mode = l.mode ?? "";
          return `<li><b>${from}</b> → <b>${to}</b> <span class="muted">(${provider}, ${mode}${mins ? `, ${mins}m` : ""})</span></li>`;
        }).join("")
      : "";

    const expl = p.explanation ?? "";

    card.innerHTML = `
      <div class="top">
        <div><b>Score:</b> ${score}</div>
        <div><b>Price:</b> £${price}</div>
        <div><b>Duration:</b> ${duration}m</div>
        <div><b>Emissions:</b> ${emissions} kg</div>
        <div><b>Risk:</b> ${risk}</div>
      </div>
      <div class="body">
        <ul>${legsHtml}</ul>
        ${expl ? `<details><summary>Explanation</summary><pre>${escapeHtml(expl)}</pre></details>` : ""}
      </div>
    `;

    el.appendChild(card);
  }
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

async function runSearch() {
  const req = buildRequest();
  document.getElementById("requestPreview").textContent = JSON.stringify(req, null, 2);

  setStatus("Searching…");
  document.getElementById("results").innerHTML = "";

  try {
    // If your endpoint differs, change this one line:
    const resp = await fetch("/api/search", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(req),
    });

    const text = await resp.text();
    const data = text ? JSON.parse(text) : {};

    if (!resp.ok) {
      setStatus(`Error ${resp.status}: ${data?.detail || text || "unknown"}`);
      return;
    }

    setStatus(`OK (${resp.status})`);
    renderResults(data);
  } catch (e) {
    setStatus(`Request failed: ${e?.message || e}`);
  }
}

document.getElementById("searchBtn").addEventListener("click", runSearch);

// live preview of request JSON
["origin","destination","depart_after","arrive_before","max_layovers","optimize_for"].forEach(id => {
  const el = document.getElementById(id);
  el.addEventListener("input", () => {
    const req = buildRequest();
    document.getElementById("requestPreview").textContent = JSON.stringify(req, null, 2);
  });
});
document.getElementById("requestPreview").textContent = JSON.stringify(buildRequest(), null, 2);