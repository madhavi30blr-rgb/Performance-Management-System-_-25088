--
-- File: database/seed_data.sql
-- Description: Inserts sample data into the PMS tables.
--

-- Insert employees
INSERT INTO employees (first_name, last_name, email, manager_id) VALUES
('Alice', 'Manager', 'alice.m@startup.com', NULL),
('Bob', 'Employee', 'bob.e@startup.com', 1),
('Charlie', 'Employee', 'charlie.e@startup.com', 1);

-- Insert goals
INSERT INTO goals (employee_id, manager_id, description, due_date, status) VALUES
(2, 1, 'Complete Project Alpha by end of Q3', '2025-09-30', 'In Progress'),
(3, 1, 'Achieve 10% growth in user engagement', '2025-12-31', 'Draft');

-- Insert tasks
INSERT INTO tasks (goal_id, employee_id, description, status, is_approved) VALUES
(1, 2, 'Research user feedback for Project Alpha', 'Done', TRUE),
(1, 2, 'Develop new feature X', 'In Progress', TRUE);

-- Insert feedback
INSERT INTO feedback (goal_id, manager_id, feedback_text) VALUES
(1, 1, 'Great work on the research phase. Keep up the momentum!');
