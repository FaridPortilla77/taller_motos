// login.js

document.getElementById('login-form').addEventListener('submit', async function(e) {
  e.preventDefault();

  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value;
  const msgEl    = document.getElementById('login-message');

  msgEl.textContent = 'Verificando...';
  msgEl.style.color = '#333';

  try {
    // 1) Obtener tokens JWT
    const tokenRes = await fetch('http://127.0.0.1:8000/api/token/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const tokenData = await tokenRes.json();

    if (!tokenRes.ok) {
      msgEl.textContent = `❌ ${tokenData.detail || 'Credenciales inválidas'}`;
      msgEl.style.color = 'red';
      return;
    }

    // Guardar tokens en localStorage
    localStorage.setItem('access', tokenData.access);
    localStorage.setItem('refresh', tokenData.refresh);

    // 2) Obtener info básica de usuario
    const userRes = await fetch('http://127.0.0.1:8000/api/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const userData = await userRes.json();

    if (userRes.ok) {
      // Guardar datos del usuario
      localStorage.setItem('username', userData.username);
      localStorage.setItem('email', userData.email);
      localStorage.setItem('is_staff', userData.is_staff); // ✅ nuevo campo

      // Redirigir según el tipo de usuario
      if (userData.is_staff) {
        window.location.href = 'admin_citas.html'; // 👨‍🔧 administrador
      } else {
        window.location.href = 'dashboard.html';    // 🧑‍🔧 cliente
      }

    } else {
      msgEl.textContent = `❌ ${userData.error || 'No se pudo obtener datos de usuario'}`;
      msgEl.style.color = 'red';
    }

  } catch (err) {
    console.error('Error de conexión:', err);
    msgEl.textContent = '❌ Error de conexión con el servidor.';
    msgEl.style.color = 'red';
  }
});
