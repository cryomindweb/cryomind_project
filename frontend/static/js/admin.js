document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const adminContent = document.querySelector('.admin-content');
    const homeLink = document.getElementById('home-link');
    const registerLink = document.getElementById('register-link');
    const searchLink = document.getElementById('search-link');
    const logoutBtn = document.getElementById('logout-btn');
    const menuItems = document.querySelectorAll('.menu-item');

    // Mostrar vista inicial
    showWelcomeView();

    // Event listeners
    homeLink.addEventListener('click', function(e) {
        e.preventDefault();
        showWelcomeView();
        setActiveMenuItem(null);
    });

    registerLink.addEventListener('click', function(e) {
        e.preventDefault();
        showRegisterView();
        setActiveMenuItem(registerLink.parentElement);
    });

    searchLink.addEventListener('click', function(e) {
        e.preventDefault();
        showSearchView();
        setActiveMenuItem(searchLink.parentElement);
    });

    logoutBtn.addEventListener('click', handleLogout);

    // Funciones para mostrar vistas
    function showWelcomeView() {
        adminContent.innerHTML = `
            <div class="welcome-message view-transition">
                <h2>Bienvenido, Administrador</h2>
                <p>Seleccione una opción del menú para comenzar.</p>
            </div>
        `;
    }

    function showRegisterView() {
        adminContent.innerHTML = `
            <div class="registration-form view-transition">
                <h2 class="form-title">Registro de nuevo usuario</h2>
                <form id="user-registration-form">
                    <div class="form-group">
                        <label for="username">Nombre de Usuario</label>
                        <input type="text" id="username" name="username" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="email">Correo Electrónico</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Contraseña</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="role">Rol</label>
                        <select id="role" name="role" required>
                            <option value="">Seleccione un rol</option>
                            <option value="administrador">Administrador</option>
                            <option value="medico">Medico</option>
                        </select>
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" id="cancel-btn" class="form-btn cancel-btn">Cancelar</button>
                        <button type="submit" class="form-btn submit-btn">Registrar</button>
                    </div>
                </form>
            </div>
        `;

        // Event listeners para el formulario
        document.getElementById('cancel-btn').addEventListener('click', showWelcomeView);
        document.getElementById('user-registration-form').addEventListener('submit', handleRegister);
    }

    async function showSearchView() {
    adminContent.innerHTML = `
        <div class="search-container view-transition">
            <h2 class="form-title">Buscar usuario</h2>
            <div class="search-form">
                <input type="text" class="search-input" placeholder="Buscar por nombre de usuario...">
            </div>
            <ul class="user-list" id="user-list">
                <!-- Los usuarios se cargarán aquí -->
            </ul>
        </div>
    `;

    let users = [];

    try {
        const token = localStorage.getItem("jwt");
        if (!token) {
            return redirectToLogin();
        }

        const res = await fetch("/users/users", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!res.ok) {
            if (res.status === 401 || res.status === 403) {
                return redirectToLogin();
            }
            throw new Error(`Error al obtener usuarios: ${res.status}`);
        }

        const data = await res.json();
        users = data.users || [];

        displayUsers(users);

    } catch (err) {
        console.error("Error al cargar usuarios:", err);
        alert("No se pudieron cargar los usuarios.");
    }

    // Event listener para búsqueda
    document.querySelector('.search-input').addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const filteredUsers = users.filter(user => 
            user.nombre_usuario.toLowerCase().includes(searchTerm)
        );
        displayUsers(filteredUsers);
    });
}


    // Funciones auxiliares
    function displayUsers(users) {
        const userList = document.getElementById('user-list');
        userList.innerHTML = users.map(user => `
            <li class="user-item">
                <div class="user-info">
                    <span class="user-name">${user.nombre_usuario}</span>
                    <span class="user-email">${user.email}</span>
                </div>
                <span class="user-role">${user.rol}</span>
                <button class="user-buttons" data_id="${user.usuario_id}">Eliminar</button>
            </li>
        `).join('');
        setupDeleteButtons();
    }

    function setupDeleteButtons() {
        document.querySelectorAll('.user-buttons').forEach(button => {
            button.addEventListener('click', async function () {
                const userId = this.getAttribute('data_id');
                const token = localStorage.getItem("jwt");

                if (!confirm("¿Seguro que deseas eliminar este usuario?")) {
                    return;
                }

                try {
                    const res = await fetch(`/users/users/${userId}`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (!res.ok) {
                        const errData = await res.json();
                        throw new Error(errData.detail || "Error al eliminar usuario");
                    }

                    alert("Usuario eliminado exitosamente");
                    // Recargar la lista de usuarios
                    showSearchView();

                } catch (err) {
                    console.error("Error eliminando usuario:", err);
                    alert(`Error: ${err.message}`);
                }
            });
        });
    }

    function setActiveMenuItem(activeItem) {
        menuItems.forEach(item => {
            item.classList.remove('active');
        });
        if (activeItem) {
            activeItem.classList.add('active');
        }
    }

    function handleRegister(e) {
        e.preventDefault();
        
        // Obtener datos del formulario
        const formData = {
            nombre_usuario: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            rol: document.getElementById('role').value
        };

        // Validación básica
        if (!formData.nombre_usuario || !formData.email || !formData.password || formData.rol.trim() === "Seleccione un rol") {
            alert('Por favor complete todos los campos');
            return;
        }

        // Aquí iría la llamada al backend para registrar el usuario
        fetch('/users/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('jwt')}` // Solo si el endpoint es protegido
            },
            body: JSON.stringify(formData)
        })
        .then(res => {
            if (!res.ok) {
                console.error('Error en la respuesta del servidor:', res);
                return res.json().then(err => { throw new Error(err.detail || 'Error al registrar usuario'); });
            }
            return res.json();
        })
        .then(data => {
            alert('Usuario registrado exitosamente');
            showWelcomeView();
            setActiveMenuItem(null);
        })
        .catch(err => {
            console.error('Error en registro:', err);
            alert(`Error: ${err.message}`);
        });
    }

    function handleLogout() {
        // Crear modal de confirmación
        const modal = document.createElement('div');
        modal.className = 'logout-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>¿Está seguro que desea cerrar sesión?</h3>
                <div class="modal-actions">
                    <button class="modal-btn confirm">Sí, cerrar sesión</button>
                    <button class="modal-btn cancel">Cancelar</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        modal.style.display = 'flex';

        // Manejar acciones del modal
        modal.addEventListener('click', function(e) {
            if (e.target.classList.contains('confirm')) {
                // Eliminar token y redirigir
                localStorage.removeItem('jwt');
                localStorage.removeItem('role');
                localStorage.removeItem('username');
                window.location.href = '/';
            } else if (e.target.classList.contains('cancel') || e.target === modal) {
                modal.style.display = 'none';
                modal.remove();
            }
        });
    }
});