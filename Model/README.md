# Housing-AI Model

This repository contains the **machine learning models** and related code for the **Housing-AI** project.

---

## Branching Strategy

To keep the workflow clean and organized, we follow a **feature-based branching strategy**:

### Main branch
- **`main`** → Stable production branch.  

### Working branches
- **`feature/*`** → Development of new features or model improvements.  
  Example: `feature/price-prediction-model`
- **`fix/*`** → Bug fixes in code or experiments.  
  Example: `fix/data-preprocessing-bug`
- **`chore/*`** → Maintenance tasks (configs, dependencies, etc).  
  Example: `chore/update-requirements`
- **`docs/*`** → Documentation changes.  
  Example: `docs/modeling-approach`
- **`hotfix/*`** → Urgent fixes applied directly to `main`.  
  Example: `hotfix/training-crash`

---

## Workflow

1. Create a branch from `main`  
2. Push the branch to remote  
3. Merge manually into `main` once the feature or fix is complete  
4. Delete the local branch if no longer needed

---

## Commit Conventions

Examples of valid commit messages:
- `feat: add data preprocessing pipeline`
- `feat: implement regression model`
- `fix: correct normalization step`
- `chore: update dependencies`
- `docs: add model training instructions`

---

## Quick Example

```bash
# Create branch from main
git checkout main
git pull origin main
git checkout -b feature/data-cleaning-pipeline

# Work and commit
git add .
git commit -m "feat: add initial data cleaning pipeline"

# Push branch
git push -u origin feature/data-cleaning-pipeline

# Merge back to main
git checkout main
git merge feature/data-cleaning-pipeline
git push origin main