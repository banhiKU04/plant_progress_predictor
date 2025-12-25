const form = document.getElementById("uploadForm");
const result = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  result.textContent = "Predicting…";

  const fd = new FormData();
  const img = document.getElementById("image").files[0];
  const city = document.getElementById("city").value.trim();

  fd.append("image", img);
  fd.append("city", city);

  try {
    const res = await fetch("/predict", { method: "POST", body: fd });
    const data = await res.json();

    if (!res.ok) {
      result.innerHTML = `<div class="error">Error: ${data.error || "Unknown error"}</div>`;
      return;
    }

    result.innerHTML =
`Disease: ${data.disease} (conf: ${data.confidence})
Severity Today: ${data.today_severity}
Risk in 7 Days: ${data.risk_7_days}
Risk in 14 Days: ${data.risk_14_days}
Weather: ${data.weather.city || ""}  T=${data.weather.temp ?? "?"}°C, H=${data.weather.humidity ?? "?"}%, Rain=${data.weather.rainfall ?? "0"}mm
Advice:
- ${data.advice.join("\n- ")}`;
  } catch (err) {
    result.innerHTML = `<div class="error">Network/Server error: ${err.message}</div>`;
  }
});
