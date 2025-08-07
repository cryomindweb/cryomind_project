document.addEventListener('DOMContentLoaded', function() {
    // Obtener datos del usuario del localStorage
    const displayUsername = document.getElementById('display-username');
    const displayRole = document.getElementById('display-role');
    const logoutBtn = document.getElementById('logout-btn');
    const searchInput = document.getElementById('search-input');
    const patientsList = document.getElementById('patients-list');

    // Cargar información del usuario
    const username = localStorage.getItem('username') || 'Usuario';
    const role = localStorage.getItem('role') || 'Rol no definido';
    const currentPath = window.location.pathname;
    if (currentPath === "/medico") {
        localStorage.removeItem('selectedPatientId');
    }

    displayUsername.textContent = username;
    displayRole.textContent = role;

    // Manejar logout
    logoutBtn.addEventListener('click', handleLogout);

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

    // Cargar lista de pacientes
    loadPatients();

    // Buscador de pacientes
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        filterPatients(searchTerm);
    });

    // Función para cargar pacientes
    async function loadPatients() {
        try {
            const response = await fetch('/patients/patients', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('jwt')}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Error al cargar pacientes');
            }

            const data = await response.json();
            renderPatients(data.pacientes); // ← ahora usamos la clave correcta
        } catch (error) {
            console.error('Error:', error);
            alert('Error al cargar la lista de pacientes');
        }
    }

    // Función para renderizar pacientes
    function renderPatients(pacientes) {
        patientsList.innerHTML = '';
        
        if (!pacientes || pacientes.length === 0) {
            patientsList.innerHTML = `
                <tr>
                    <td colspan="3" style="text-align: center;">No se encontraron pacientes</td>
                </tr>
            `;
            return;
        }

        pacientes.forEach(patient => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${patient.id_clinico || 'N/A'}</td>
                <td>${patient.nombre_completo || 'Nombre no disponible'}</td>
                <td>
                    <button class="action-btn view-btn" data-patient-id="${patient.id_clinico}">
                        Ver
                    </button>
                </td>
            `;
            patientsList.appendChild(row);
        });

        // Agregar event listeners a los botones
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const patientId = this.getAttribute('data-patient-id');
                viewPatientDetails(patientId);
            });
        });
    }

    // Función para filtrar pacientes
    function filterPatients(searchTerm) {
        const rows = document.querySelectorAll('#patients-list tr');
        
        rows.forEach(row => {
            const idClinico = row.cells[0].textContent.toLowerCase();
            const nombre = row.cells[1].textContent.toLowerCase();
            
            if (idClinico.includes(searchTerm) || nombre.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    // Función para ver detalles del paciente
    function viewPatientDetails(patientId) {
        localStorage.setItem('selectedPatientId', patientId);
        window.location.href = `/medico/${patientId}`;
    }

});