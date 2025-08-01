document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logout-btn');
    
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

    // Mostrar modal al hacer clic en cerrar sesión
    logoutBtn.addEventListener('click', function() {
        document.querySelector('.logout-modal').style.display = 'flex';
    });

    // Manejar acciones del modal
    modal.addEventListener('click', function(e) {
        if (e.target.classList.contains('confirm')) {
            // Eliminar token y redirigir
            localStorage.removeItem('jwt');
            window.location.href = '/login.html';
        } else if (e.target.classList.contains('cancel') || e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Verificar autenticación al cargar la página
    checkAuth();
});

function checkAuth() {
    const token = localStorage.getItem('jwt');
    if (!token) {
        window.location.href = '/login.html';
    }
    
    // Aquí podrías verificar también el tipo de usuario
    // para asegurarte que es un administrador
}