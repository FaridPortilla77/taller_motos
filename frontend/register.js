document.getElementById('register-form').addEventListener('submit', async function(e) {
  e.preventDefault();

  const msgEl   = document.getElementById('msg');
  const username = document.getElementById('username').value.trim();
  const email    = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;

  msgEl.textContent = 'Enviando...';
  msgEl.style.color = '#333';

  try {
    const response = await fetch('http://127.0.0.1:8000/api/registro/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ username, email, password })
    });

    const data = await response.json();

    if (response.ok) {
      msgEl.textContent = '✅ Registro exitoso. Por favor inicia sesión.';
      msgEl.style.color = 'green';
      this.reset();
    } else {
      const errores = Array.isArray(data) ? data.join(', ')
                      : typeof data === 'object'
                        ? Object.values(data).flat().join(', ')
                        : data;
      msgEl.textContent = `❌ ${errores}`;
      msgEl.style.color = 'red';
    }
  } catch (err) {
    console.error('Error al registrar:', err);
    msgEl.textContent = '❌ Error de conexión con el servidor.';
    msgEl.style.color = 'red';
  }
});
