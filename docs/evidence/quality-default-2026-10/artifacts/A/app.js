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
  meter: $("#meter-fill"),
  message: $("#budget-message"),
  count: $("#book-count"),
};

/** @type {{ books: { id: string, title: string, author: string, hours: number, selected: boolean }[], availableHours: number }} */
let state = loadState();

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { books: [], availableHours: 8 };
    const parsed = JSON.parse(raw);
    if (!parsed || !Array.isArray(parsed.books)) return { books: [], availableHours: 8 };
    return {
      books: parsed.books.map(normalizeBook).filter(Boolean),
      availableHours: clampHours(parsed.availableHours ?? 8),
    };
  } catch {
    return { books: [], availableHours: 8 };
  }
}

function normalizeBook(b) {
  if (!b || typeof b.title !== "string") return null;
  return {
    id: String(b.id || crypto.randomUUID()),
    title: b.title.trim(),
    author: String(b.author || "").trim() || "Unknown",
    hours: clampHours(b.hours),
    selected: Boolean(b.selected),
  };
}

function clampHours(n) {
  const v = Number(n);
  if (!Number.isFinite(v) || v < 0) return 0;
  return Math.round(v * 2) / 2;
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function plannedHours() {
  return state.books.filter((b) => b.selected).reduce((sum, b) => sum + b.hours, 0);
}

function renderBudget() {
  const available = clampHours(state.availableHours);
  const planned = plannedHours();
  els.displayAvailable.textContent = String(available);
  els.planned.textContent = String(planned);

  const ratio = available > 0 ? planned / available : planned > 0 ? 2 : 0;
  const pct = available > 0 ? Math.min(100, (planned / available) * 100) : planned > 0 ? 100 : 0;
  els.meter.style.width = `${pct}%`;
  els.meter.classList.remove("warn", "over");

  if (planned > available) {
    els.meter.classList.add("over");
    els.message.textContent = `Over budget by ${(planned - available).toFixed(1)} h — trim the stack or add time.`;
    els.message.classList.add("over");
  } else if (ratio >= 0.85 && available > 0) {
    els.meter.classList.add("warn");
    els.message.textContent = "Almost full — a tight but doable weekend.";
    els.message.classList.remove("over");
  } else if (planned === 0) {
    els.message.textContent = "Select books below to fill the weekend.";
    els.message.classList.remove("over");
  } else {
    els.message.textContent = `${(available - planned).toFixed(1)} h still open.`;
    els.message.classList.remove("over");
  }
}

function renderList() {
  els.list.innerHTML = "";
  const n = state.books.length;
  els.count.textContent = n === 1 ? "1 book" : `${n} books`;
  els.empty.classList.toggle("hidden", n > 0);

  state.books.forEach((book) => {
    const li = document.createElement("li");
    li.className = "book-item" + (book.selected ? " selected" : "");
    li.dataset.id = book.id;

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = book.selected;
    cb.setAttribute("aria-label", `Include ${book.title} this weekend`);

    const meta = document.createElement("div");
    meta.className = "book-meta";
    const title = document.createElement("strong");
    title.textContent = book.title;
    const author = document.createElement("span");
    author.textContent = book.author;
    meta.append(title, author);

    const actions = document.createElement("div");
    actions.className = "book-actions";
    const hours = document.createElement("span");
    hours.className = "book-hours";
    hours.textContent = `${book.hours} h`;
    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "btn ghost";
    remove.textContent = "Remove";
    remove.setAttribute("aria-label", `Remove ${book.title}`);
    actions.append(hours, remove);

    li.append(cb, meta, actions);
    els.list.append(li);

    cb.addEventListener("change", () => {
      book.selected = cb.checked;
      saveState();
      render();
    });

    remove.addEventListener("click", () => {
      state.books = state.books.filter((b) => b.id !== book.id);
      saveState();
      render();
    });
  });

  renderBudget();
}

function render() {
  els.available.value = String(state.availableHours);
  renderList();
}

els.form.addEventListener("submit", (e) => {
  e.preventDefault();
  const title = els.title.value.trim();
  const author = els.author.value.trim();
  const hours = clampHours(els.hours.value);
  if (!title || hours <= 0) return;

  state.books.push({
    id: crypto.randomUUID(),
    title,
    author: author || "Unknown",
    hours,
    selected: false,
  });
  saveState();
  els.form.reset();
  els.hours.value = "6";
  render();
  els.title.focus();
});

els.available.addEventListener("input", () => {
  state.availableHours = clampHours(els.available.value);
  saveState();
  renderBudget();
});

els.available.addEventListener("change", () => {
  if (state.availableHours === 0 && els.available.value === "") {
    state.availableHours = 0;
  }
  saveState();
  renderBudget();
});

render();
