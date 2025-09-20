# Performance Management System (PMS)

This is a simple web-based Performance Management System built for a startup to help managers and employees track goals, tasks, and feedback.

## Features
- **Goal & Task Setting**: Managers can set goals, and employees can track tasks.
- **Progress Tracking**: Clear status updates for goals and tasks.
- **Feedback**: Managers can provide written feedback on goals.
- **Reporting**: Basic view of an employee's performance history.

## Technologies
- **Backend**: Python with FastAPI
- **Database**: PostgreSQL
- **Frontend**: Simple HTML, CSS, and JavaScript
- **Dashboard**: (Placeholder for future implementation with tools like Plotly Dash)

## Setup and Installation

### 1. Database Setup

1.  **Install PostgreSQL**: Ensure PostgreSQL is installed and running on your system.
2.  **Create Database**: Connect to PostgreSQL and create a new database.
    ```bash
    CREATE DATABASE pms_db;
    ```
3.  **Run SQL Scripts**: Navigate to the `database/` directory and execute the schema and seed data scripts.
    ```bash
    # From the project root
    psql -d pms_db -f database/schema.sql
    psql -d pms_db -f database/seed_data.sql
    ```

### 2. Backend Setup

1.  **Install Python**: Make sure you have Python 3.8+ installed.
2.  **Create Virtual Environment**: It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install Dependencies**:
    ```bash
    pip install fastapi uvicorn "psycopg2-binary<2.9"
    ```
4.  **Configure Database Connection**: Create a `.env` file or set environment variables for your database credentials.
    ```bash
    export DB_HOST=localhost
    export DB_NAME=pms_db
    export DB_USER=postgres
    export DB_PASS=password
    ```
    Replace `password` with your actual PostgreSQL password.
5.  **Run the Backend Server**:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### 3. Frontend

The frontend is a simple HTML/CSS/JS application. You can view it by simply opening `frontend/index.html` in your web browser. Note that modern browsers may require a local server to handle CORS requests.

### 4. Running the Application

1.  Start the PostgreSQL server.
2.  Start the FastAPI backend server as described above.
3.  Open `frontend/index.html` in your web browser. You can use a simple Python server for this:
    ```bash
    # From the project root
    python -m http.server 8080 -d frontend/
    ```
    Then, navigate to `http://localhost:8080` in your browser.
