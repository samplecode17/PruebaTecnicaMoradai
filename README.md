# 🧩 Prueba Técnica – Full Stack Junior (Moradai)

## 📋 Descripción general

Este proyecto implementa un **módulo de referidos** para la plataforma de Moradai.  
Permite a los usuarios generar códigos de referido y validarlos desde una interfaz web simple.  
Consta de un **backend con API REST** y un **frontend para simular una compra con el codigo de referido**.

---

## ⚙️ Estructura del proyecto

### 1️⃣ Backend
```bash
backend/
├── app/
│ ├── api/
│ │ └── v1/ # Endpoints de la API versión 1
│ ├── core/
│ │ ├── config.py # Configuración del proyecto
│ │ └── security.py # Funciones de seguridad (hashing, tokens)
│ ├── crud/
│ │ ├── init.py
│ │ ├── referalcode.py # CRUD para códigos de referido
│ │ └── user.py # CRUD para usuarios
│ ├── models/
│ │ ├── init.py
│ │ ├── referalcode.py # Modelo de código de referido
│ │ └── user.py # Modelo de usuario
│ ├── schemas/
│ │ ├── init.py
│ │ ├── referalcode.py # Esquema de códigos de referido
│ │ ├── token.py # Esquema de tokens
│ │ └── user.py # Esquema de usuario
│ ├── session.py # Conexión a la base de datos
│ ├── main.py # Punto de entrada del backend
│ ├── init.py
│ └── test/
│ ├── init.py
│ ├── test_auth.py # Tests de autenticación
│ ├── test_main.py # Tests de endpoints generales
│ ├── test_referal.py # Tests de códigos de referido
│ └── test_user.py # Tests de usuarios
├── docker-compose.yml # Configuración de Docker
└── requirements.txt # Dependencias de Python
---
```
### 2️⃣ Frontend
```bash
frontend/
├── index.html
├── jsconfig.json
├── package.json
├── package-lock.json
├── vite.config.js
├── public/
│ └── favicon.ico
├── README.md
├── src/
│ ├── App.vue # Componente raíz de Vue
│ ├── main.js # Entrada principal
│ ├── assets/
│ │ └── main.css # Estilos globales
│ ├── components/
│ │ └── TopBar.vue # Componente reutilizable (barra superior)
│ ├── router/
│ │ └── index.js # Configuración de rutas (Vue Router)
│ ├── services/
│ │ └── appClient.js # Cliente para la API backend
│ ├── store/
│ │ ├── index.js # Configuración de Vuex para el estado global
│ │ └── modules/ # Módulos de estados globales de usuario y codigo de referido
│ └── views/ #vistas
│   ├── CreationReferal.vue # Página para crear/validar códigos
│   ├── Home.vue # Página de inicio
│   ├── Login.vue # Página de login
│   ├── Payed.vue # Confirmación de pago
│   ├── Payment.vue # Página de pago
│   └── Product.vue # Detalle de producto
```
---
## 🚀 Instalación y ejecución

### 🔧 Requisitos previos
- tener la versión de python y npm mas reciente
- poder ejecutar docker-compose
- tener un .env en cada carpeta tanto frontend como backend (copiar todo lo del .envexample es lo que use en este caso)

### 🖥️ Backend

```bash
cd backend
docker compose  up -d
pip install -r requirements.txt
```

El backend se iniciará en [http://localhost:8000](http://localhost:8000)

#### Endpoints disponibles:
#### 🔗 Endpoints de la API

##### 1️⃣ Users

| Método | Endpoint | Descripción |
|--------|---------|-------------|
| GET    | `/users/` | Listar todos los usuarios |
| POST   | `/users/` | Crear un nuevo usuario |
| GET    | `/users/{user_id}` | Obtener detalles de un usuario |
| PUT    | `/users/{user_id}` | Actualizar información de un usuario |

---

##### 2️⃣ ReferralCodes

| Método | Endpoint | Descripción |
|--------|---------|-------------|
| GET    | `/referalcodes/` | Obtener todos los códigos de referido |
| POST   | `/referalcodes/` | Crear un código de referido |
| GET    | `/referalcodes/{referralcode_id}` | Obtener detalles de un código de referido |
| PUT    | `/referalcodes/{referralcode_id}` | Actualizar un código de referido existente |
| DELETE | `/referalcodes/{referralcode_id}` | Eliminar un código de referido |
| GET    | `/referalcodes/verify/{referralcode}` | Verificar el código de referido |

---

##### 3️⃣ Auth

| Método | Endpoint | Descripción |
|--------|---------|-------------|
| POST   | `/auth/token` | Login y obtención de token de acceso |
| GET    | `/auth/me` | Obtener información del usuario autenticado |

---

##### 4️⃣ Default

| Método | Endpoint | Descripción |
|--------|---------|-------------|
| GET    | `/` | Página Home del API (inicio) |
**Ejemplo POST**
Acceder a la documentación de la api [http://localhost:8000/docs](http://localhost:8000/docs) para ver como usar.

---

### 🌐 Frontend

```bash
cd frontend
npm install
npm run dev
```

El frontend se iniciará en [http://localhost:5173](http://localhost:5173)

#### Funcionalidades:
- Pagina de inicio con 2 botones , 1 para acceder a la validacion y otro para crear codigo de referido
- Pagina de compra y pagina de validación de codigo de referido
- Mensaje de validación (válido / no válido)  
- Botón para **avanzar a página de compra finalizada** (simulada)
- Login necesario en algunas paginas

---

## 🧠 Decisiones técnicas

| Área | Decisión | Motivo |
|------|-----------|--------|
| **Frontend** | Vue + Vite | Rápido, modular y fácil de desplegar |
| **Backend** | FastApi | Simple, cómodo y con documentación via openapi por defecto  |
| **Persistencia** | Una DB postgres desplegada via docker|
| **Código de referido** | Generador aleatorio alfanumérico de 10 caracteres | Simple y único |
| **Testing** | Pytest | Cobertura básica de endpoints |
| **Estructura modular** | Separación por capas (enpoints, operaciones crud, models) | Facilita escalabilidad y mantenibilidad |

---

## 🧪 Ejecución de tests

```bash
cd backend
pytest -v
```

## ⚖️ Limitaciones y posibles mejoras

- 🔹 Validación de código simple, no conectada a flujo real de compra  
- 🔹 Sin paginación
- 🔹 UI básica (sin diseño avanzado)
- 🔹 Falta encriptación de contraseña y login muy basico.
- 🔹 Faltan mejorar schemas
- 🔹 Falta HTML semantico, responsividad mínima

---

## 🧩 Preguntas teóricas

### a) El código de referido no deja de ser una promoción para captar clientes. Existen diferentes tipos de promociones como afiliaciones, promos de descuento, etc. ¿Cómo modularizarías el código para que en el futuro fuera escalable y los mismos servicios aceptasen otro tipo de promociones?

Diseñaría una **entidad genérica `Promotion`** con un campo `type` (`referral`, `discount`, `affiliate`, etc.).  
Cada tipo implementaría su propia lógica mediante **polimorfismo**.  
Así, `ReferralService`, `DiscountService`, etc., compartirían una interfaz común para creación, validación y expiración.

---

### b) Aspectos de seguridad en producción
- Sanitizar entradas y prevenir inyección SQL/JSON.  
- Validar payloads con un esquema (p. ej. Joi o Zod).  
- Limitar la tasa de peticiones por IP(rate limiting).  
- HTTPS obligatorio.  
- Logging de accesos y errores.  
- Uso de tokens o API keys si se expone externamente.
- Usar ids aleatorias y schemas //hablando de fastapi// con poca informacion critica como ids.

---

### c) Paginación en `GET /code`
Usaría parámetros `limit` y `offset` (o `page`/`per_page`):
```bash
GET /code?limit=20&offset=40
```
En SQL → `SELECT * FROM codes LIMIT 20 OFFSET 40`  
En NoSQL → usar `skip` y `limit` (MongoDB).  
También incluiría metadatos en la respuesta:  
```json
{
  "data": [...],
  "pagination": { "total": 120, "page": 3, "pages": 6 }
}
```

---

### d) Relacional vs NoSQL

| Tipo | Ventajas | Desventajas |
|------|-----------|-------------|
| **Relacional (PostgreSQL, MySQL)** | Estructura clara, relaciones entre usuarios y códigos, integridad referencial | Menos flexible ante cambios de esquema |
| **NoSQL (MongoDB)** | Flexible, rápido de prototipar, ideal si los datos no son muy relacionados | Dificulta consultas complejas o transacciones |

Para este módulo de referidos, una base **relacional** es más adecuada por la relación *usuario → códigos*.

---

## 🌍 Despliegue (opcional)

- Backend: Render  
- Frontend: Netlify  
- Desplegado en: [https://moradai.netlify.app/](https://moradai.netlify.app/)
- Usar usuario y contraseña->
  - usuario: admin
  - contraseña: password

---

## 🧱 Autor

**Nombre:** _Ibrahim Moussafia_  
**Fecha:** Octubre 2025  
**Versión:** 1.0  
