let currentModel = null;
let modelDefs = {};
let currentRows = [];
let selectedIndexes = new Set();

function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  const color = { success: "text-bg-success", warning: "text-bg-warning", error: "text-bg-danger", info: "text-bg-primary" }[type] || "text-bg-primary";
  const toastId = `toast-${Date.now()}`;
  container.insertAdjacentHTML(
    "beforeend",
    `<div id="${toastId}" class="toast align-items-center ${color} border-0 mb-2" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body">${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>
    </div>`
  );
  const el = document.getElementById(toastId);
  const toast = new bootstrap.Toast(el, { delay: 2800 });
  toast.show();
  el.addEventListener("hidden.bs.toast", () => el.remove());
}

function getValuesFromForm() {
  const values = {};
  Object.keys(modelDefs[currentModel] || {}).forEach(() => {});
  (modelDefs[currentModel] || []).forEach((field) => {
    const input = document.querySelector(`[data-field="${field}"]`);
    values[field] = input ? input.value : null;
  });
  return values;
}

function renderForm() {
  const holder = document.getElementById("dynamic-form");
  holder.innerHTML = "";
  (modelDefs[currentModel] || []).forEach((field) => {
    const col = document.createElement("div");
    col.className = "col-md-4";
    col.innerHTML = `
      <label class="form-label">${field}</label>
      <input type="text" class="form-control" data-field="${field}" placeholder="${field}">
    `;
    holder.appendChild(col);
  });
}

function renderTable() {
  const table = document.getElementById("stewardship-table");
  const thead = table.querySelector("thead");
  const tbody = table.querySelector("tbody");
  const columns = modelDefs[currentModel] || [];

  thead.innerHTML = `<tr><th style="width: 50px;"></th>${columns.map((c) => `<th>${c}</th>`).join("")}</tr>`;
  tbody.innerHTML = currentRows
    .map((row, index) => {
      const checked = selectedIndexes.has(index) ? "checked" : "";
      return `<tr data-row-index="${index}">
        <td><input type="checkbox" class="row-checkbox" data-row-index="${index}" ${checked}></td>
        ${columns.map((c) => `<td>${row[c] ?? ""}</td>`).join("")}
      </tr>`;
    })
    .join("");

  document.querySelectorAll(".row-checkbox").forEach((checkbox) => {
    checkbox.addEventListener("change", (event) => {
      const idx = Number(event.target.dataset.rowIndex);
      if (event.target.checked) {
        selectedIndexes.add(idx);
      } else {
        selectedIndexes.delete(idx);
      }
    });
  });
}

async function loadRows() {
  const res = await fetch(`/api/stewardship/rows/${currentModel}`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Failed loading rows");
  }
  const data = await res.json();
  currentRows = data.rows || [];
  selectedIndexes.clear();
  renderTable();
}

function selectedRowsPayload() {
  return Array.from(selectedIndexes).map((idx) => currentRows[idx]).filter(Boolean);
}

async function mutate(method, body) {
  const res = await fetch(`/api/stewardship/rows/${currentModel}`, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.detail || "Operation failed");
  }
  return data;
}

async function init() {
  const modelRes = await fetch("/api/stewardship/models");
  const modelData = await modelRes.json();
  const selector = document.getElementById("model-selector");
  modelData.models.forEach((m) => {
    modelDefs[m.name] = m.columns;
    const opt = document.createElement("option");
    opt.value = m.name;
    opt.textContent = m.name;
    selector.appendChild(opt);
  });

  currentModel = selector.value;
  renderForm();
  await loadRows();

  selector.addEventListener("change", async () => {
    currentModel = selector.value;
    renderForm();
    await loadRows();
    showToast("Model changed.", "info");
  });

  document.getElementById("add-btn").addEventListener("click", async () => {
    try {
      const data = await mutate("POST", { values: getValuesFromForm() });
      await loadRows();
      showToast(data.message, "success");
    } catch (err) {
      showToast(err.message, "error");
    }
  });

  document.getElementById("edit-btn").addEventListener("click", async () => {
    const selected_rows = selectedRowsPayload();
    if (selected_rows.length === 0) {
      showToast("Select at least one row to edit.", "warning");
      return;
    }
    try {
      const data = await mutate("PUT", { selected_rows, values: getValuesFromForm() });
      await loadRows();
      showToast(data.message, "success");
    } catch (err) {
      showToast(err.message, "error");
    }
  });

  document.getElementById("delete-btn").addEventListener("click", async () => {
    const selected_rows = selectedRowsPayload();
    if (selected_rows.length === 0) {
      showToast("Select at least one row to delete.", "warning");
      return;
    }
    try {
      const data = await mutate("DELETE", { selected_rows });
      await loadRows();
      showToast(data.message, "success");
    } catch (err) {
      showToast(err.message, "error");
    }
  });

  document.getElementById("select-all-btn").addEventListener("click", () => {
    selectedIndexes = new Set(currentRows.map((_, i) => i));
    renderTable();
    showToast("All rows selected.", "info");
  });

  document.getElementById("clear-selection-btn").addEventListener("click", () => {
    selectedIndexes.clear();
    renderTable();
    showToast("Selection cleared.", "info");
  });

  document.getElementById("refresh-btn").addEventListener("click", async () => {
    try {
      await loadRows();
      showToast("Table refreshed.", "info");
    } catch (err) {
      showToast(err.message, "error");
    }
  });
}

init().catch((err) => showToast(err.message, "error"));

