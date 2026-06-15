const AUTH_TOKEN_KEY = "elibrary_token";
const AUTH_USER_KEY = "elibrary_user";

function getToken() {
  return localStorage.getItem(AUTH_TOKEN_KEY) || sessionStorage.getItem(AUTH_TOKEN_KEY);
}

function getUser() {
  const raw = localStorage.getItem(AUTH_USER_KEY) || sessionStorage.getItem(AUTH_USER_KEY);
  return raw ? JSON.parse(raw) : null;
}

function setAuth(token, user, remember = true) {
  const storage = remember ? localStorage : sessionStorage;
  storage.setItem(AUTH_TOKEN_KEY, token);
  storage.setItem(AUTH_USER_KEY, JSON.stringify(user));
}

function clearAuth() {
  localStorage.removeItem(AUTH_TOKEN_KEY);
  localStorage.removeItem(AUTH_USER_KEY);
  sessionStorage.removeItem(AUTH_TOKEN_KEY);
  sessionStorage.removeItem(AUTH_USER_KEY);
}

function isAuthenticated() {
  return !!getToken();
}

function hasRole(...roles) {
  const user = getUser();
  return !!user && roles.includes(user.role.name);
}

// Обёртка над fetch, добавляющая Authorization-заголовок
async function apiFetch(url, options = {}) {
  const token = getToken();
  const headers = options.headers ? { ...options.headers } : {};
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return fetch(url, { ...options, headers });
}

// Показывает flash-сообщение через query-параметр (имитация flash для SPA)
function showFlashFromQuery() {
  const params = new URLSearchParams(window.location.search);
  const msg = params.get("flash");
  const type = params.get("flash_type") || "success";
  if (msg) {
    const container = document.getElementById("flash-container");
    if (container) {
      container.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
          ${msg}
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>`;
    }
  }
}

function redirectWithFlash(url, message, type = "success") {
  const sep = url.includes("?") ? "&" : "?";
  window.location.href = `${url}${sep}flash=${encodeURIComponent(message)}&flash_type=${type}`;
}

// Перенаправление неаутентифицированных пользователей
function requireAuth() {
  if (!isAuthenticated()) {
    redirectWithFlash("/login", "Для выполнения данного действия необходимо пройти процедуру аутентификации", "warning");
    return false;
  }
  return true;
}

function requireRole(...roles) {
  if (!requireAuth()) return false;
  if (!hasRole(...roles)) {
    redirectWithFlash("/", "У вас недостаточно прав для выполнения данного действия", "danger");
    return false;
  }
  return true;
}

function logout() {
  clearAuth();
  redirectWithFlash("/", "Вы вышли из системы");
}

function renderNavbar() {
  const navAuth = document.getElementById("nav-auth");
  if (!navAuth) return;

  const user = getUser();
  if (user) {
    const fio = `${user.last_name} ${user.first_name} ${user.middle_name || ""}`.trim();
    navAuth.innerHTML = `
      <span class="navbar-text me-3">${fio}</span>
      <button class="btn btn-outline-light" id="logout-btn">Выйти</button>
    `;
    document.getElementById("logout-btn").addEventListener("click", logout);

    if (user.role.name === "user") {
      const selectionsLink = document.getElementById("nav-selections-item");
      if (selectionsLink) selectionsLink.classList.remove("d-none");
    }
    if (user.role.name === "admin") {
      const addBookBtn = document.querySelectorAll(".admin-only");
      addBookBtn.forEach((el) => el.classList.remove("d-none"));
    }
    if (user.role.name === "admin" || user.role.name === "moderator") {
      document.querySelectorAll(".editor-only").forEach((el) => el.classList.remove("d-none"));
    }
  } else {
    navAuth.innerHTML = `<a class="btn btn-outline-light" href="/login">Войти</a>`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  renderNavbar();
  showFlashFromQuery();
});
