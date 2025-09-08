document.addEventListener('DOMContentLoaded', function() {
    // Obtener elementos del DOM
    const displayUsername = document.getElementById('display-username');
    const displayRole = document.getElementById('display-role');
    const logoutBtn = document.getElementById('logout-btn');
    const patientName = document.getElementById('patient-name');
    const clinicalId = document.getElementById('clinical-id');
    const patientInfo = document.getElementById('patient-info');
    const treatmentInfo = document.getElementById('treatment-info');
    
    // Obtener ID del paciente de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const patientId = localStorage.getItem('selectedPatientId') || urlParams.get('id');

    // Cargar información del usuario
    const username = localStorage.getItem('username') || 'Usuario';
    const role = localStorage.getItem('role') || 'Rol no definido';
    
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

    // Cargar datos del paciente
    if (patientId) {
        loadPatientData(patientId);
        loadTreatmentData(patientId);
        loadTemperatureData(patientId);
    } else {
        alert('No se ha especificado un paciente');
        window.location.href = '/medico';
    }

    // Función para cargar datos del paciente
    async function loadPatientData(patientId) {
        try {
            const response = await fetch(`/patients/${patientId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('jwt')}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Error al cargar datos del paciente');
            }

            const data = await response.json();
            renderPatientData(data);
        } catch (error) {
            console.error('Error:', error);
            alert('Error al cargar los datos del paciente');
        }
    }

    // Función para renderizar datos del paciente
// Función para renderizar datos del paciente
    function renderPatientData(patient) {
        patientName.textContent = patient.nombre_completo || 'Nombre no disponible';
        clinicalId.textContent = patient.id_clinico || 'N/A';
        
        const patientFields = [
            { label: 'Progenitor', value: patient.nombre_progenitor || 'N/A' },
            { label: 'Fecha de Nacimiento', value: patient.fecha_nacimiento || 'N/A' },
            // Título añadido
            { type: 'title', content: 'Tiempo desde el Nacimiento' },
            { label: 'Hora de Nacimiento', value: patient.hora_nacimiento || 'N/A' },
            { label: 'Minutos de Nacimiento', value: patient.minuto_nacimiento || 'N/A' },
            { label: 'Semanas de Gestación', value: patient.semanas_gestacion || 'N/A' },
            { label: 'Días de Gestación', value: patient.dias_gestacion || 'N/A' },
            { label: 'Peso', value: patient.peso ? `${patient.peso} kg` : 'N/A' }
        ];

        patientInfo.innerHTML = patientFields.map(field => {
            if (field.type === 'title') {
                return `<div class="info-title">${field.content}</div>`;
            } else {
                return `
                    <div class="info-item">
                        <div class="info-label">${field.label}</div>
                        <div class="info-value">${field.value}</div>
                    </div>
                `;
            }
        }).join('');
    }

    // Función para cargar datos del tratamiento
    async function loadTreatmentData(patientId) {
        try {
            const response = await fetch(`/treatments/${patientId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('jwt')}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Error al cargar datos del tratamiento');
            }

            const data = await response.json();
            renderTreatmentData(data);
        } catch (error) {
            console.error('Error:', error);
            treatmentInfo.innerHTML = `
                <div class="info-item" style="grid-column: span 2;">
                    <div class="info-value">No se pudo cargar la información del tratamiento</div>
                </div>
            `;
        }
    }

    // Función para renderizar datos del tratamiento
    function renderTreatmentData(treatment) {
        const treatmentFields = [
            { label: 'Hora de Inicio', value: treatment.hora_inicio || 'N/A' },
            { label: 'Hora de Finalización', value: treatment.hora_finalizacion || 'N/A' },
            { label: 'Fecha Finalización', value: treatment.fecha_tratamiento || 'N/A' },
            { label: 'Observaciones', value: treatment.observaciones || 'N/A' },
            { label: 'Setpoint', value: treatment.setpoint || 'N/A' }
        ];

        treatmentInfo.innerHTML = treatmentFields.map(field => `
            <div class="info-item">
                <div class="info-label">${field.label}</div>
                <div class="info-value">${field.value}</div>
            </div>
        `).join('');
    }

    // Función para cargar datos de temperatura
    async function loadTemperatureData(patientId) {
        try {
            const response = await fetch(`/temperatures/${patientId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('jwt')}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Error al cargar datos de temperatura');
            }

            const data = await response.json();
            console.log('Temperature Data:', data);
            renderTemperatureChart(data.temperaturas);
        } catch (error) {
            console.error('Error:', error);
            document.querySelector('.chart-container').innerHTML = `
                <div class="info-value">No se pudo cargar el gráfico de temperatura</div>
            `;
        }
    }

    // Función para renderizar gráfico de temperatura
    function renderTemperatureChart(temperatureData) {
        const ctx = document.getElementById('temperature-chart').getContext('2d');

        // Transformar los datos para usar el eje X fijo
        const dataPoints = temperatureData.map(item => ({
            x: item.marca_temporal_horas,
            y: item.temperatura
        }));

        console.log('Temperatura:', dataPoints.map(d => d.y));
        console.log('Horas:', dataPoints.map(d => d.x));

        new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: 'Temperatura (°C)',
                    data: dataPoints,
                    borderColor: "#048a81", // dark cyan
                    backgroundColor: 'rgba(4, 138, 129, 0.2)', // dark cyan con transparencia
                    pointBackgroundColor: "#da627d", // blush
                    pointRadius: 2,
                    pointHoverRadius: 4,
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        type: 'linear',
                        min: 12.5,
                        max: 39.7,
                        ticks: {
                            stepSize: 1.7,
                            color: "#320e3b", // russian violet
                            font: {
                                family: 'Arial',
                                size: 12,
                                weight: 'bold'
                            }
                        },
                        grid: {
                            color: 'rgba(50, 14, 59, 0.1)' // soft violet grid
                        },
                        title: {
                            display: true,
                            text: "Temperatura (°C)",
                            color: "#320e3b",
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    x: {
                        type: 'linear',
                        min: 0,
                        max: 72,
                        ticks: {
                            stepSize: 24, // Marcas cada 24 horas
                            color: "#656256", // ebony
                            callback: function(value) {
                                // Mostrar solo las marcas de 24 en 24 horas
                                return value % 24 === 0 ? `${value}h` : '';
                            }
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        title: {
                            display: true,
                            text: "Tiempo (h)",
                            color: "#320e3b",
                            font: {
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            color: "#320e3b", // russian violet
                            font: {
                                weight: 'bold'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: "#fcfaf9", // seasalt
                        titleColor: "#320e3b",
                        bodyColor: "#048a81",
                        borderColor: "#048a81",
                        borderWidth: 1,
                        callbacks: {
                            title: function(context) {
                                // Mostrar la hora en el tooltip
                                return `Hora: ${context[0].raw.x}h`;
                            },
                            label: function(context) {
                                return `Temperatura: ${context.raw.y}°C`;
                            }
                        }
                    }
                }
            }
        });
    }

});