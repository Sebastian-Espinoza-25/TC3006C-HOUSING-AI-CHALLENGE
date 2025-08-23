# Housing-AI Frontend

This repository contains the **frontend** of the **Housing-AI** project, built with [React](https://react.dev/).

---

## Branching Strategy

To keep the workflow clean and organized, we follow a **feature-based branching strategy**:

### Main branch
- **`main`** → Stable production branch.  

### Working branches
- **`feature/*`** → Development of new features.  
  Example: `feature/login-page`
- **`fix/*`** → Bug fixes.  
  Example: `fix/navbar-overflow`
- **`chore/*`** → Maintenance tasks (configs, dependencies, etc).  
  Example: `chore/eslint-prettier`
- **`docs/*`** → Documentation changes.  
  Example: `docs/readme-setup`
- **`hotfix/*`** → Urgent fixes applied directly to `main`.  
  Example: `hotfix/payments-timeout`

---

## Workflow

1. Create a branch from `main`  
2. Push the branch to remote  
3. Merge manually into `main` once the feature is complete  
4. Delete the local branch if no longer needed

---

## Commit Conventions

Examples of valid commit messages:
- `feat: add login page`
- `fix: handle invalid credentials`
- `chore: update dependencies`
- `docs: update contributing guide`
- `refactor: extract auth hook`

---

## Quick Example

```bash
# Create branch from main
git checkout main
git pull origin main
git checkout -b feature/login-page

# Work and commit
git add .
git commit -m "feat: add login page UI"

# Push branch
git push -u origin feature/login-page

# Merge back to main
git checkout main
git merge feature/login-page
git push origin main