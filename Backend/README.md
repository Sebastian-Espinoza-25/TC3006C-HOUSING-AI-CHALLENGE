# Housing-AI Backend

This repository contains the **backend services and APIs** for the **Housing-AI** project.

---

## Branching Strategy

To keep the workflow clean and organized, we follow a **feature-based branching strategy**:

### Main branch
- **`main`** → Stable production branch.  

### Working branches
- **`feature/*`** → Development of new backend features or services.  
  Example: `feature/authentication-api`
- **`fix/*`** → Bug fixes in backend logic.  
  Example: `fix/jwt-expiration-bug`
- **`chore/*`** → Maintenance tasks (configs, dependencies, etc).  
  Example: `chore/update-dockerfile`
- **`docs/*`** → Documentation changes.  
  Example: `docs/api-endpoints`
- **`hotfix/*`** → Urgent fixes applied directly to `main`.  
  Example: `hotfix/payment-service-down`

---

## Workflow

1. Create a branch from `main`  
2. Push the branch to remote  
3. Merge manually into `main` once the feature or fix is complete  
4. Delete the local branch if no longer needed

---

## Commit Conventions

Examples of valid commit messages:
- `feat: add authentication middleware`
- `feat: implement user registration endpoint`
- `fix: correct database connection pool`
- `chore: update environment variables`
- `docs: add API usage guide`

---

## Quick Example

```bash
# Create branch from main
git checkout main
git pull origin main
git checkout -b feature/authentication-api

# Work and commit
git add .
git commit -m "feat: add authentication middleware"

# Push branch
git push -u origin feature/authentication-api

# Merge back to main
git checkout main
git merge feature/authentication-api
git push origin main