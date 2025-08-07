document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.login-container');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        // Verificar campos llenos
        if (!usernameInput.value.trim() || !passwordInput.value.trim()) {
            showError('Por favor complete todos los campos');
            return;
        }
        try {
            // Enviar datos al backend
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: usernameInput.value.trim(),
                    password: passwordInput.value.trim(),
                })
            });
            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('jwt', data.access_token);
                localStorage.setItem("role", data.role);
                localStorage.setItem('username', data.nombre_usuario);
                if (data.role === 'administrador') {
                    window.location.href = '/admin';
                } else if (data.role === 'medico') {
                    console.log('Login exitoso:', data);
                    window.location.href = `/medico`;
                } else {
                    showError('Tipo de usuario no reconocido');
                }
                
            } else if (response.status === 403) {
                showError('Usuario o contraseña incorrectos');
            } else {
                showError('Error en el servidor. Intente nuevamente más tarde.');
            }
        } catch (error) {
            showError('Error de conexión. Intente nuevamente.');
        }
    });
    function showError(message) {
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.style.color = '#da627d';
        errorElement.style.marginTop = '1rem';
        errorElement.style.textAlign = 'center';
        errorElement.textContent = message;
        const submitButton = document.querySelector('button[type="submit"]');
        submitButton.insertAdjacentElement('afterend', errorElement);
    }
});