# CryoMind

**CryoMind** es un proyecto académico diseñado para gestionar pacientes neonatales que requieren monitoreo térmico. El sistema permite registrar datos clínicos, administrar tratamientos y visualizar la evolución de la temperatura del paciente mediante gráficas interactivas.

## 🧠 Objetivo

Ofrecer una solución web para profesionales médicos que necesitan registrar y visualizar en tiempo real el tratamiento térmico de neonatos en incubadoras.

---

## 📦 Estructura del Proyecto

```
CryoMind/
├── Backend/
│   ├── api/              # Rutas FastAPI (auth, usuarios, pacientes, etc.)
│   ├── core/             # Configuración y dependencias del sistema
│   ├── schemas/          # Modelos de datos (Pydantic)
│   ├── services/         # Lógica de negocio e integración con Supabase
│   ├── views/            # Plantillas HTML renderizadas por FastAPI
│   └── main.py           # Punto de entrada de la API
├── Frontend/
│   ├── static/           # Archivos estáticos (CSS, JS, imágenes)
│   ├── templates/        # Páginas HTML
├── requirements.txt      # Dependencias del backend
├── .gitignore            # Archivos a ignorar por Git
└── README.md             # Descripción del proyecto
```

---

## ⚙️ Tecnologías

- **FastAPI** – Framework web para el backend (Python)
- **Supabase** – Base de datos y autenticación
- **JavaScript** – Lógica del frontend
- **Chart.js** – Visualización de datos (temperatura)
- **HTML & CSS** – Interfaz de usuario

---

## 🚀 Instalación

1. **Clona el repositorio:**

```bash
git clone https://github.com/tu-usuario/cryoMind.git
cd cryoMind
```

2. **Crea un entorno virtual:**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

4. **Configura tus variables de entorno (por ejemplo, URL y claves de Supabase)**  
Puedes hacerlo directamente en `core/config.py`.

5. **Ejecuta el backend:**

```bash
uvicorn main:app --reload
```

6. **Accede a la aplicación:**

Abre tu navegador en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🩺 Funcionalidades

### Usuarios
- Autenticación para rol médico y administrador
- Gestión de sesiones con JWT

### Pacientes
- Registro de datos clínicos al nacer
- Asociación con tratamientos

### Tratamientos
- Creación de sesiones térmicas con horarios y setpoint

### Temperaturas
- Carga masiva (batch) de temperaturas
- Visualización en gráficos (Chart.js)
- Escalado de tiempo hasta 72 horas

---

## 📊 Ejemplo de Gráfica de Temperatura

- Eje Y: de 12.5°C a 38°C con separación cada 1.7°C
- Eje X: de 0 a 72 horas, con marcas cada 24h

---

## 🧪 Estado

Este proyecto está en etapa académica y puede ser mejorado para incluir:
- Test unitarios
- Carga de datos por sensores IoT
- Dashboard estadístico