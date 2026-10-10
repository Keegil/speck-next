const STORAGE_KEY = "weekend-reading-v1";

const $ = (sel) => document.querySelector(sel);

const state = loadState();

const els = {
  availableHours: $("#available-hours"),
  plannedHours: $("#planned-hours"),
  remainingHours: $("#remaining-hours"),
  budgetMessage: $("#budget-message"),
  addForm: $("#add-form"),
  bookList: $("#book-list"),
  emptyState: $("#empty-state"),
  bookCount: $("#book-count"),
};

function defaultState() {
  return { availableHours: 8, books: [] };
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return defaultState();
    const parsed = JSON.parse(raw);
    return {
      availableHours: Number(parsed.availableHours) || 8,
      books: Array.isArray(parsed.books) ? parsed.books : [],
    };
  } catch {
    return defaultState();
  }
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function uid() {
  return crypto.randomUUID();
}

function plannedTotal() {
  return state.books
    .filter((b) => b.selected)
    .reduce((sum, b) => sum + b.hours, 0);
}

function formatHours(n) {
  const rounded = Math.round(n * 10) / 10;
  return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(1);
}

function updateBudget() {
  const available = Math.max(0, Number(els.availableHours.value) || 0);
  state.availableHours = available;
  const planned = plannedTotal();
  const remaining = available - planned;

  els.plannedHours.textContent = formatHours(planned);
  els.remainingHours.textContent = formatHours(remaining);

  els.budgetMessage.className = "budget-message";
  if (planned === 0) {
    els.budgetMessage.textContent = "Select books below to fill your weekend.";
  } else if (remaining < 0) {
    els.budgetMessage.textContent = `Over budget by ${formatHours(-remaining)} hours.`;
    els.budgetMessage.classList.add("over");
  } else if (remaining === 0) {
    els.budgetMessage.textContent = "Your stack matches your hours exactly.";
    els.budgetMessage.classList.add("ok");
  } else {
    els.budgetMessage.textContent = `${formatHours(remaining)} hours still open for more reading.`;
    els.budgetMessage.classList.add("ok");
  }

  saveState();
}

function renderList() {
  els.bookList.innerHTML = "";
  const count = state.books.length;
  els.bookCount.textContent = count === 1 ? "1 book" : `${count} books`;
  els.emptyState.hidden = count > 0;

  state.books.forEach((book) => {
    const li = document.createElement("li");
    li.className = `book-item${book.selected ? " selected" : ""}`;
    li.dataset.id = book.id;

    const check = document.createElement("input");
    check.type = "checkbox";
    check.checked = book.selected;
    check.setAttribute("aria-label", `Include ${book.title} this weekend`);
    check.addEventListener("change", () => {
      book.selected = check.checked;
      li.classList.toggle("selected", book.selected);
      updateBudget();
    });

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
    hours.textContent = `${formatHours(book.hours)} h`;
    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "btn btn-ghost";
    remove.textContent = "Remove";
    remove.addEventListener("click", () => {
      state.books = state.books.filter((b) => b.id !== book.id);
      renderList();
      updateBudget();
    });
    actions.append(hours, remove);

    li.append(check, meta, actions);
    els.bookList.append(li);
  });
}

els.availableHours.value = state.availableHours;
els.availableHours.addEventListener("input", updateBudget);

els.addForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const title = $("#title").value.trim();
  const author = $("#author").value.trim();
  const hours = Number($("#hours").value);
  if (!title || !author || !(hours > 0)) return;

  state.books.push({
    id: uid(),
    title,
    author,
    hours,
    selected: false,
  });

  els.addForm.reset();
  $("#hours").value = "4";
  renderList();
  updateBudget();
  $("#title").focus();
});

renderList();
updateBudget();
