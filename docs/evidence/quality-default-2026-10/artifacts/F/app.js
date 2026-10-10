const STORAGE_KEY = "daytrip-pack-list-v1";

const CATEGORY_LABELS = {
  clothes: "Clothes",
  food: "Food",
  equipment: "Equipment",
};

/** @type {{ id: string, name: string, category: string, packed: boolean }[]} */
let items = [];
let activeFilter = "all";

const form = document.getElementById("add-form");
const nameInput = document.getElementById("item-name");
const categorySelect = document.getElementById("item-category");
const listEl = document.getElementById("item-list");
const emptyEl = document.getElementById("empty-state");
const packedCountEl = document.getElementById("packed-count");
const totalCountEl = document.getElementById("total-count");
const leftLabelEl = document.getElementById("left-label");
const progressBar = document.getElementById("progress-bar");
const progressFill = document.getElementById("progress-fill");
const filterButtons = document.querySelectorAll(".filter-chip");

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return;
    items = parsed.filter(
      (row) =>
        row &&
        typeof row.id === "string" &&
        typeof row.name === "string" &&
        CATEGORY_LABELS[row.category] &&
        typeof row.packed === "boolean"
    );
  } catch {
    items = [];
  }
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
}

function newId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

function visibleItems() {
  if (activeFilter === "all") return items;
  return items.filter((item) => item.category === activeFilter);
}

function updateProgress() {
  const total = items.length;
  const packed = items.filter((i) => i.packed).length;
  const left = total - packed;
  const pct = total === 0 ? 0 : Math.round((packed / total) * 100);

  packedCountEl.textContent = String(packed);
  totalCountEl.textContent = String(total);
  progressFill.style.width = `${pct}%`;
  progressBar.setAttribute("aria-valuenow", String(pct));
  progressBar.setAttribute("aria-valuemax", "100");

  if (total === 0) {
    leftLabelEl.textContent = "Nothing on the list yet.";
  } else if (left === 0) {
    leftLabelEl.textContent = "All set — bag is ready!";
  } else {
    leftLabelEl.textContent =
      left === 1 ? "1 item left to pack." : `${left} items left to pack.`;
  }
}

function render() {
  const visible = visibleItems();
  const hasAny = items.length > 0;
  const showList = hasAny && (activeFilter === "all" || visible.length > 0);

  listEl.innerHTML = "";
  listEl.classList.toggle("is-hidden", !showList);
  emptyEl.classList.toggle("is-hidden", hasAny);

  if (!hasAny) {
    emptyEl.textContent = "Add your first item above.";
  } else if (visible.length === 0) {
    emptyEl.classList.remove("is-hidden");
    emptyEl.textContent = `No ${CATEGORY_LABELS[activeFilter].toLowerCase()} items yet.`;
  }

  for (const item of visible) {
    const li = document.createElement("li");
    li.className = `item${item.packed ? " is-packed" : ""}`;
    li.dataset.id = item.id;

    const check = document.createElement("input");
    check.type = "checkbox";
    check.className = "item__check";
    check.checked = item.packed;
    check.setAttribute("aria-label", `Mark ${item.name} as packed`);
    check.addEventListener("change", () => {
      item.packed = check.checked;
      save();
      render();
    });

    const body = document.createElement("div");
    body.className = "item__body";
    const name = document.createElement("span");
    name.className = "item__name";
    name.textContent = item.name;
    const badge = document.createElement("span");
    badge.className = `badge badge--${item.category}`;
    badge.textContent = CATEGORY_LABELS[item.category];
    body.append(name, badge);

    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "btn btn--ghost";
    removeBtn.textContent = "Remove";
    removeBtn.setAttribute("aria-label", `Remove ${item.name}`);
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
  items.push({
    id: newId(),
    name,
    category: categorySelect.value,
    packed: false,
  });
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
