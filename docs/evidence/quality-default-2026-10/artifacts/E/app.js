const STORAGE_KEY = "day-trip-bag-v1";

const CATEGORIES = ["clothes", "food", "equipment"];

/** @type {{ id: string, name: string, category: string, packed: boolean }[]} */
let items = [];
let activeFilter = "all";

const form = document.getElementById("add-form");
const nameInput = document.getElementById("item-name");
const categorySelect = document.getElementById("item-category");
const listEl = document.getElementById("item-list");
const emptyEl = document.getElementById("empty-state");
const remainingEl = document.getElementById("remaining-count");
const progressSubEl = document.getElementById("progress-sub");
const filterButtons = document.querySelectorAll(".filter-btn");

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      items = [];
      return;
    }
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      items = [];
      return;
    }
    items = parsed.filter(
      (row) =>
        row &&
        typeof row.id === "string" &&
        typeof row.name === "string" &&
        CATEGORIES.includes(row.category) &&
        typeof row.packed === "boolean"
    );
  } catch {
    items = [];
  }
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
}

function uid() {
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 9)}`;
}

function updateProgress() {
  const total = items.length;
  const remaining = items.filter((i) => !i.packed).length;
  remainingEl.textContent = String(remaining);
  progressSubEl.textContent =
    total === 0 ? "of 0 items" : `of ${total} item${total === 1 ? "" : "s"}`;
}

function visibleItems() {
  if (activeFilter === "all") return items;
  return items.filter((i) => i.category === activeFilter);
}

function render() {
  const visible = visibleItems();
  listEl.innerHTML = "";

  const showEmpty = items.length === 0;
  emptyEl.hidden = !showEmpty;
  listEl.hidden = showEmpty;

  if (showEmpty) {
    updateProgress();
    return;
  }

  if (visible.length === 0) {
    const li = document.createElement("li");
    li.className = "empty-state";
    li.textContent = `No ${activeFilter} items yet.`;
    listEl.appendChild(li);
    listEl.hidden = false;
    emptyEl.hidden = true;
    updateProgress();
    return;
  }

  for (const item of visible) {
    const li = document.createElement("li");
    li.className = "item" + (item.packed ? " is-packed" : "");
    li.dataset.id = item.id;

    const check = document.createElement("input");
    check.type = "checkbox";
    check.className = "item-check";
    check.checked = item.packed;
    check.setAttribute("aria-label", `Packed: ${item.name}`);
    check.addEventListener("change", () => {
      item.packed = check.checked;
      save();
      render();
    });

    const body = document.createElement("div");
    body.className = "item-body";
    const name = document.createElement("div");
    name.className = "item-name";
    name.textContent = item.name;
    const badge = document.createElement("span");
    badge.className = `badge badge--${item.category}`;
    badge.textContent = item.category;
    body.append(name, badge);

    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "btn-remove";
    removeBtn.textContent = "Remove";
    removeBtn.addEventListener("click", () => {
      items = items.filter((i) => i.id !== item.id);
      save();
      render();
    });

    li.append(check, body, removeBtn);
    listEl.appendChild(li);
  }

  updateProgress();
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const name = nameInput.value.trim();
  if (!name) return;
  const category = categorySelect.value;
  if (!CATEGORIES.includes(category)) return;

  items.push({ id: uid(), name, category, packed: false });
  save();
  nameInput.value = "";
  nameInput.focus();
  render();
});

filterButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    activeFilter = btn.dataset.filter || "all";
    filterButtons.forEach((b) => b.classList.toggle("is-active", b === btn));
    render();
  });
});

load();
render();
