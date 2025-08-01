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
            console.log('Enviando datos de inicio de sesión...'); // Debugging line
            console.log('Username:', usernameInput.value.trim()); // Debugging line
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: usernameInput.value.trim(),
                    password: passwordInput.value.trim()
                })
            });
            console.log('Response:', response); // Debugging line
            // Procesar respuesta
            if (response.ok) {
                const data = await response.json();
                // Guardar JWT en localStorage
                localStorage.setItem('jwt', data.access_token);
                // Redireccionar según tipo de usuario
                if (data.role === 'administrador') {
                    window.location.href = '/admin';
                } else if (data.role === 'medico') {
                    window.location.href = `/${data.username}`;
                } else {
                    showError('Tipo de usuario no reconocido');
                }
                
            } else if (response.status === 403) {
                showError('Usuario o contraseña incorrectos');
            } else {
                showError('Error en el servidor. Intente nuevamente más tarde.');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Error de conexión. Intente nuevamente.');
        }
    });

    // Función para mostrar mensajes de error
    function showError(message) {
        // Eliminar mensajes de error anteriores
        const existingError = document.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        // Crear elemento de error
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.style.color = '#da627d'; // Usando --blush de la paleta
        errorElement.style.marginTop = '1rem';
        errorElement.style.textAlign = 'center';
        errorElement.textContent = message;

        // Insertar después del botón
        const submitButton = document.querySelector('button[type="submit"]');
        submitButton.insertAdjacentElement('afterend', errorElement);
    }
});