const POLL_INTERVAL_MS = 2000;
const BYTES_PER_GB = 1e9;

function setMetric(name, percent, detail) {
  const value = Number(percent);
  const safePercent = Number.isFinite(value) ? Math.max(0, Math.min(value, 100)) : 0;
  document.getElementById(`${name}-value`).textContent =
    Number.isFinite(value) ? value.toFixed(name === "cpu" ? 1 : 0) : "--";
  const meter = document.getElementById(`${name}-meter`);
  meter.style.width = `${safePercent}%`;
  meter.classList.toggle("high", safePercent >= 85);
  document.getElementById(`${name}-detail`).textContent = detail;
}

async function updateDashboard() {
  const dot = document.getElementById("status-dot");
  const label = document.getElementById("connection-label");
  try {
    const response = await fetch("/status", { cache: "no-store" });
    if (!response.ok) throw new Error(`Request failed (${response.status})`);
    const data = await response.json();

    setMetric("cpu", data.cpu.usage, `${Math.round(data.cpu.frequency ?? 0)} MHz`);
    setMetric("ram", data.ram.percent,
      `${(data.ram.used / BYTES_PER_GB).toFixed(1)} / ${(data.ram.total / BYTES_PER_GB).toFixed(1)} GB`);
    setMetric("disk", data.disk.percent,
      `${(data.disk.used / BYTES_PER_GB).toFixed(0)} / ${(data.disk.total / BYTES_PER_GB).toFixed(0)} GB`);

    dot.classList.add("online");
    label.textContent = "System online";
    document.getElementById("updated-at").textContent =
      `Updated ${new Date().toLocaleTimeString()}`;
  } catch {
    dot.classList.remove("online");
    label.textContent = "Connection lost";
    document.getElementById("updated-at").textContent = "Retrying telemetry…";
  }
}

updateDashboard();
window.setInterval(updateDashboard, POLL_INTERVAL_MS);
