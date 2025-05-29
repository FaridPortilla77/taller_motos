// script.js

/**
 * Devuelve las cabeceras necesarias para peticiones autenticadas con JWT.
 */
function getAuthHeaders() {
  const token = localStorage.getItem('access');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  };
}

/**
 * Refresca el token de acceso usando el refresh token.
 * Si tiene éxito, actualiza localStorage y devuelve el nuevo access token.
 */
async function refreshAccessToken() {
  const refresh = localStorage.getItem('refresh');
  if (!refresh) return null;

  try {
    const res = await fetch('http://127.0.0.1:8000/api/token/refresh/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh })
    });
    const data = await res.json();
    if (res.ok && data.access) {
      localStorage.setItem('access', data.access);
      return data.access;
    } else {
      console.error('Error refrescando token:', data);
      logout();
      return null;
    }
  } catch (err) {
    console.error('Error en refreshAccessToken:', err);
    logout();
    return null;
  }
}

/**
 * Realiza una petición protegida con autenticación JWT.
 * Si el token expira, intenta refrescarlo una vez automáticamente.
 */
async function fetchWithAuth(url, options = {}, retry = true) {
  const headers = getAuthHeaders();
  options.headers = { ...headers, ...options.headers };

  try {
    const res = await fetch(url, options);

    // Si el token expiró e intentamos una vez refrescarlo
    if (res.status === 401 && retry) {
      const newToken = await refreshAccessToken();
      if (newToken) {
        options.headers['Authorization'] = `Bearer ${newToken}`;
        return fetchWithAuth(url, options, false);
      }
    }

    return res;
  } catch (err) {
    console.error('Error en fetchWithAuth:', err);
    throw err;
  }
}

/**
 * Cierra la sesión limpiando localStorage y redirigiendo al login.
 */
function logout() {
  localStorage.clear();
  window.location.href = 'login.html';
}
