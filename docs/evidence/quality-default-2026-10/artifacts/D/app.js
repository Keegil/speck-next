const STORAGE_KEY = "weekend-reading-v1";

const $ = (sel) => document.querySelector(sel);

const els = {
  form: $("#add-form"),
  title: $("#title"),
  author: $("#author"),
  hours: $("#hours"),
  available: $("#available-hours"),
  list: $("#book-list"),
  empty: $("#empty-state"),
  planned: $("#planned-hours"),
  displayAvailable: $("#display-available"),
  status: $("#budget-status"),
  budgetPanel: $(".budget-panel"),
};

/** @typedef {{ id: string, title: string, author: string, hours: number }} Book */

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { books: [], selectedIds: [], availableHours: 8 };
    const data = JSON.parse(raw);
    return {
      books: Array.isArray(data.books) ? data.books : [],
      selectedIds: Array.isArray(data.selectedIds) ? data.selectedIds : [],
      availableHours:
        typeof data.availableHours === "number" && data.availableHours >= 0
          ? data.availableHours
          : 8,
    };
  } catch {
    return { books: [], selectedIds: [], availableHours: 8 };
  }
}

function saveState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

let state = loadState();

function uid() {
  return crypto.randomUUID();
}

function plannedHours() {
  const selected = new Set(state.selectedIds);
  return state.books
    .filter((b) => selected.has(b.id))
    .reduce((sum, b) => sum + b.hours, 0);
}

function syncBudgetUI() {
  const available = state.availableHours;
  const planned = plannedHours();
  const remaining = available - planned;

  els.available.value = String(available);
  els.displayAvailable.textContent = formatHours(available);
  els.planned.textContent = formatHours(planned);

  els.budgetPanel.classList.remove("over-budget", "within-budget");
  els.status.classList.remove("ok", "tight", "over");

  if (planned === 0) {
    els.status.textContent = "Select books to build your weekend stack.";
    return;
  }

  if (remaining < 0) {
    els.budgetPanel.classList.add("over-budget");
    els.status.classList.add("over");
    els.status.textContent = `Over by ${formatHours(Math.abs(remaining))} h — trim the list or add time.`;
  } else if (remaining <= 1) {
    els.budgetPanel.classList.add("within-budget");
    els.status.classList.add("tight");
    els.status.textContent = `${formatHours(remaining)} h left — a tight but doable weekend.`;
  } else {
    els.budgetPanel.classList.add("within-budget");
    els.status.classList.add("ok");
    els.status.textContent = `${formatHours(remaining)} h still open for another chapter or two.`;
  }
}

function formatHours(n) {
  return Number.isInteger(n) ? String(n) : n.toFixed(1);
}

function renderList() {
  els.list.replaceChildren();
  const selected = new Set(state.selectedIds);

  for (const book of state.books) {
    const li = document.createElement("li");
    li.className = "book-item" + (selected.has(book.id) ? " selected" : "");
    li.dataset.id = book.id;

    const check = document.createElement("input");
    check.type = "checkbox";
    check.checked = selected.has(book.id);
    check.setAttribute("aria-label", `Include ${book.title} this weekend`);
    check.addEventListener("change", () => {
      toggleSelection(book.id, check.checked);
    });

    const meta = document.createElement("div");
    meta.className = "book-meta";
    meta.innerHTML = `<strong></strong><span></span>`;
    meta.querySelector("strong").textContent = book.title;
    meta.querySelector("span").textContent = book.author;

    const hours = document.createElement("span");
    hours.className = "book-hours";
    hours.textContent = `${formatHours(book.hours)} h`;

    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "btn ghost";
    remove.textContent = "Remove";
    remove.addEventListener("click", () => removeBook(book.id));

    li.append(check, meta, hours, remove);
    els.list.append(li);
  }

  els.empty.hidden = state.books.length > 0;
  syncBudgetUI();
}

function toggleSelection(id, on) {
  const set = new Set(state.selectedIds);
  if (on) set.add(id);
  else set.delete(id);
  state.selectedIds = [...set];
  saveState(state);
  renderList();
}

function removeBook(id) {
  state.books = state.books.filter((b) => b.id !== id);
  state.selectedIds = state.selectedIds.filter((sid) => sid !== id);
  saveState(state);
  renderList();
}

els.form.addEventListener("submit", (e) => {
  e.preventDefault();
  const title = els.title.value.trim();
  const author = els.author.value.trim();
  const hours = parseFloat(els.hours.value, 10);

  if (!title || !author || !Number.isFinite(hours) || hours <= 0) return;

  state.books.push({ id: uid(), title, author, hours });
  saveState(state);
  els.form.reset();
  els.title.focus();
  renderList();
});

els.available.addEventListener("input", () => {
  const val = parseFloat(els.available.value, 10);
  state.availableHours = Number.isFinite(val) && val >= 0 ? val : 0;
  saveState(state);
  syncBudgetUI();
});

renderList();
