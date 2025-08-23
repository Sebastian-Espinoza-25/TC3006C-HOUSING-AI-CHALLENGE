# Housing-AI Frontend

Este repositorio contiene el **frontend** del proyecto **Housing-AI**, creado con [React](https://react.dev/).

---

## Esquema de Ramas (Branching Strategy)

Para mantener un flujo de trabajo limpio y organizado, usamos un esquema de ramas basado en **features**:

### Ramas principales
- **`main`** → Rama estable de producción.  

### Ramas de trabajo
- **`feature/*`** → Desarrollo de nuevas funcionalidades.  
  Ejemplo: `feature/login-page`
- **`fix/*`** → Corrección de errores puntuales.  
  Ejemplo: `fix/navbar-overflow`
- **`chore/*`** → Tareas de mantenimiento (configs, dependencias, etc).  
  Ejemplo: `chore/eslint-prettier`
- **`docs/*`** → Cambios en la documentación.  
  Ejemplo: `docs/readme-setup`
- **`hotfix/*`** → Arreglos urgentes en `main`.  
  Ejemplo: `hotfix/payments-timeout`

---

## Flujo de Trabajo

1. Crear rama desde `main`  
2. Subir la rama al remoto  
3. Fusionar manualmente a `main` cuando la funcionalidad esté lista  
4. Eliminar la rama local si ya no es necesaria

---

## Convenciones de Commits

Ejemplos de mensajes válidos:
- `feat: add login page`
- `fix: handle invalid credentials`
- `chore: update dependencies`
- `docs: update contributing guide`
- `refactor: extract auth hook`

---

## Ejemplo rápido

```bash
# Crear rama desde main
git checkout main
git pull origin main
git checkout -b feature/login-page

# Trabajar y commitear
git add .
git commit -m "feat: add login page UI"

# Subir rama
git push -u origin feature/login-page

# Fusionar a main
git checkout main
git merge feature/login-page
git push origin main