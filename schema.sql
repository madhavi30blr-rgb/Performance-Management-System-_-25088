--
-- File: database/schema.sql
-- Description: Creates the database schema for the PMS.
--

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    manager_id INTEGER,
    CONSTRAINT fk_manager FOREIGN KEY (manager_id) REFERENCES employees(employee_id) ON DELETE SET NULL
);

CREATE TABLE goals (
    goal_id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    manager_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    due_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('Draft', 'In Progress', 'Completed', 'Cancelled')),
    CONSTRAINT fk_employee_goal FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE,
    CONSTRAINT fk_manager_goal FOREIGN KEY (manager_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    goal_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('To Do', 'In Progress', 'Done')),
    is_approved BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_goal_task FOREIGN KEY (goal_id) REFERENCES goals(goal_id) ON DELETE CASCADE,
    CONSTRAINT fk_employee_task FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);

CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    goal_id INTEGER NOT NULL,
    manager_id INTEGER NOT NULL,
    feedback_text TEXT NOT NULL,
    CONSTRAINT fk_goal_feedback FOREIGN KEY (goal_id) REFERENCES goals(goal_id) ON DELETE CASCADE,
    CONSTRAINT fk_manager_feedback FOREIGN KEY (manager_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);
