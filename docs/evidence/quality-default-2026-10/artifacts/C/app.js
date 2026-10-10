const STORAGE_KEY = "weekend-reading-v1";

const defaultState = () => ({
  availableHours: 8,
  books: [],
});

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultState();
    const parsed = JSON.parse(raw);
    return {
      availableHours: Number(parsed.availableHours) || 0,
      books: Array.isArray(parsed.books) ? parsed.books : [],
    };
  } catch {
    return defaultState();
  }
}

function saveState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

let state = loadState();

const els = {
  availableHours: document.getElementById("available-hours"),
  plannedHours: document.getElementById("planned-hours"),
  displayAvailable: document.getElementById("display-available"),
  budgetMessage: document.getElementById("budget-message"),
  budgetFill: document.getElementById("budget-fill"),
  addForm: document.getElementById("add-form"),
  bookList: document.getElementById("book-list"),
  emptyState: document.getElementById("empty-state"),
};

function plannedHours() {
  return state.books
    .filter((b) => b.selected)
    .reduce((sum, b) => sum + Number(b.hours) || 0, 0);
}

function updateBudget() {
  const available = Math.max(0, Number(state.availableHours) || 0);
  const planned = plannedHours();
  const remaining = available - planned;

  els.plannedHours.textContent = String(planned);
  els.displayAvailable.textContent = String(available);

  const ratio = available > 0 ? Math.min(planned / available, 1) : planned > 0 ? 1 : 0;
  els.budgetFill.style.width = `${ratio * 100}%`;
  els.budgetFill.classList.remove("warn", "over");
  els.budgetMessage.classList.remove("ok", "warn", "over");

  if (planned === 0) {
    els.budgetMessage.textContent = "Select books to plan your weekend.";
    els.budgetMessage.classList.add("ok");
  } else if (remaining >= 0) {
    els.budgetMessage.textContent =
      remaining === 0
        ? "Your stack fills the weekend exactly."
        : `${remaining} h left for breaks or another short read.`;
    els.budgetMessage.classList.add(remaining === 0 ? "warn" : "ok");
    if (remaining === 0) els.budgetFill.classList.add("warn");
  } else {
    els.budgetMessage.textContent = `Over budget by ${Math.abs(remaining)} h — drop a title or add time.`;
    els.budgetMessage.classList.add("over");
    els.budgetFill.classList.add("over");
  }
}

function render() {
  els.availableHours.value = state.availableHours;

  const hasBooks = state.books.length > 0;
  els.emptyState.classList.toggle("hidden", hasBooks);
  els.bookList.innerHTML = "";

  state.books.forEach((book) => {
    const li = document.createElement("li");
    li.className = `book-item${book.selected ? " selected" : ""}`;
    li.dataset.id = book.id;

    const check = document.createElement("input");
    check.type = "checkbox";
    check.checked = book.selected;
    check.setAttribute("aria-label", `Include ${book.title} this weekend`);

    const meta = document.createElement("div");
    meta.className = "book-meta";
    const title = document.createElement("h3");
    title.textContent = book.title;
    const author = document.createElement("p");
    author.textContent = book.author;
    meta.append(title, author);

    const actions = document.createElement("div");
    actions.className = "book-actions";
    const hours = document.createElement("span");
    hours.className = "book-hours";
    hours.textContent = `${book.hours} h`;
    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "btn danger";
    removeBtn.textContent = "Remove";
    removeBtn.setAttribute("aria-label", `Remove ${book.title}`);
    actions.append(hours, removeBtn);

    check.addEventListener("change", () => {
      book.selected = check.checked;
      saveState(state);
      render();
    });

    removeBtn.addEventListener("click", () => {
      state.books = state.books.filter((b) => b.id !== book.id);
      saveState(state);
      render();
    });

    li.append(check, meta, actions);
    els.bookList.appendChild(li);
  });

  updateBudget();
}

els.availableHours.addEventListener("input", () => {
  state.availableHours = Math.max(0, Number(els.availableHours.value) || 0);
  saveState(state);
  updateBudget();
});

els.addForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value.trim();
  const author = document.getElementById("author").value.trim();
  const hours = Number(document.getElementById("hours").value);

  if (!title || !author || !(hours > 0)) return;

  state.books.push({
    id: crypto.randomUUID(),
    title,
    author,
    hours,
    selected: false,
  });
  saveState(state);
  els.addForm.reset();
  document.getElementById("hours").value = "4";
  render();
});

render();
