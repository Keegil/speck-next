const STORAGE_KEY = 'daypack-items-v1';
const categories = { clothes: 'Clothes', food: 'Food', equipment: 'Equipment' };

let items = loadItems();

const form = document.querySelector('#item-form');
const nameInput = document.querySelector('#item-name');
const categoryInput = document.querySelector('#item-category');
const groups = document.querySelector('#groups');
const emptyState = document.querySelector('#empty-state');
const progressCopy = document.querySelector('#progress-copy');
const progressPercent = document.querySelector('#progress-percent');
const progressBar = document.querySelector('#progress-bar');
const remainingCount = document.querySelector('#remaining-count');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const name = nameInput.value.trim();
  if (!name) return;
  items.push({ id: crypto.randomUUID(), name, category: categoryInput.value, packed: false });
  persist();
  form.reset();
  nameInput.focus();
});

groups.addEventListener('click', (event) => {
  const button = event.target.closest('button[data-id]');
  if (!button) return;
  const index = items.findIndex((item) => item.id === button.dataset.id);
  if (index < 0) return;
  if (button.classList.contains('remove')) items.splice(index, 1);
  else items[index].packed = !items[index].packed;
  persist();
});

function loadItems() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    return Array.isArray(saved) ? saved : [];
  } catch { return []; }
}

function persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  render();
}

function render() {
  groups.replaceChildren();
  emptyState.hidden = items.length > 0;

  for (const [key, label] of Object.entries(categories)) {
    const categoryItems = items.filter((item) => item.category === key);
    if (!categoryItems.length) continue;
    const section = document.createElement('section');
    section.className = 'group';
    const heading = document.createElement('div');
    heading.className = 'group-heading';
    heading.textContent = `${label} · ${categoryItems.length}`;
    section.append(heading);
    for (const item of categoryItems) section.append(renderItem(item));
    groups.append(section);
  }

  const packed = items.filter((item) => item.packed).length;
  const left = items.length - packed;
  const percent = items.length ? Math.round((packed / items.length) * 100) : 0;
  progressPercent.textContent = `${percent}%`;
  progressBar.style.width = `${percent}%`;
  progressCopy.textContent = !items.length ? 'Your bag is empty' : left ? `${packed} of ${items.length} packed` : 'All packed. Have a good trip!';
  remainingCount.textContent = `${left} left`;
}

function renderItem(item) {
  const row = document.createElement('div');
  row.className = `item${item.packed ? ' packed' : ''}`;
  const check = document.createElement('button');
  check.type = 'button';
  check.className = 'check';
  check.dataset.id = item.id;
  check.setAttribute('aria-label', `${item.packed ? 'Mark unpacked' : 'Mark packed'}: ${item.name}`);
  check.textContent = '✓';
  const name = document.createElement('span');
  name.className = 'item-name';
  name.textContent = item.name;
  const remove = document.createElement('button');
  remove.type = 'button';
  remove.className = 'remove';
  remove.dataset.id = item.id;
  remove.setAttribute('aria-label', `Remove ${item.name}`);
  remove.textContent = '×';
  row.append(check, name, remove);
  return row;
}

render();
