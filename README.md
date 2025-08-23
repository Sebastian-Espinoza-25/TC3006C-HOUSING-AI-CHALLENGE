# Housing-AI Challenge

This repository contains the **Backend**, **Frontend**, and **Model** components for the Housing-AI Challenge project.

---

## Project Structure

- **Backend/**: FastAPI-based REST API for serving data and business logic.
- **Frontend/**: React-based web application for user interaction.
- **Model/**: Machine learning models and related code.

---

## Getting Started

### Running the Frontend (Development)

1. Clone this repository:
   ```bash
   git clone <https://github.com/Sebastian-Espinoza-25/TC3006C-HOUSING-AI-CHALLENGE.git>
   cd Housing-AI-CHALLENGE/Frontend/housing-ai
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
   The app will be available at [http://localhost:3000](http://localhost:3000).

---

### Running the Backend (Development)

1. Navigate to the backend directory:
   ```bash
   cd Housing-AI-CHALLENGE/Backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at [http://localhost:8000](http://localhost:8000).

---

## Additional Information

- For more details on each component, see the respective `README.md` files in [Backend/](Backend/README.md), [Frontend/](Frontend/README.md), and [Model/](Model/README.md).
