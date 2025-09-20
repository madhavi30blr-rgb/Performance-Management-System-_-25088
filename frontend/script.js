//
// File: frontend/script.js
// Description: Handles front-end logic and API calls.
//

document.addEventListener('DOMContentLoaded', () => {
    const goalsContainer = document.getElementById('goals-container');
    const createGoalForm = document.getElementById('create-goal-form');

    // Function to fetch and display all goals
    const fetchGoals = async () => {
        goalsContainer.innerHTML = '';
        try {
            const response = await fetch('http://localhost:8000/goals/');
            if (!response.ok) {
                throw new Error('Failed to fetch goals');
            }
            const goals = await response.json();
            goals.forEach(goal => {
                const goalItem = document.createElement('li');
                goalItem.className = 'goal-item';
                goalItem.innerHTML = `
                    <h3>Goal ID: ${goal.goal_id}</h3>
                    <p><strong>Description:</strong> ${goal.description}</p>
                    <p><strong>Due Date:</strong> ${goal.due_date}</p>
                    <p><strong>Status:</strong> ${goal.status}</p>
                `;
                goalsContainer.appendChild(goalItem);
            });
        } catch (error) {
            console.error('Error fetching goals:', error);
            goalsContainer.innerHTML = '<p>Failed to load goals. Please check the backend server.</p>';
        }
    };

    // Handle form submission to create a new goal
    createGoalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const newGoal = {
            employee_id: parseInt(document.getElementById('employee_id').value),
            manager_id: parseInt(document.getElementById('manager_id').value),
            description: document.getElementById('description').value,
            due_date: document.getElementById('due_date').value,
            status: document.getElementById('status').value
        };

        try {
            const response = await fetch('http://localhost:8000/goals/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newGoal)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to create goal');
            }

            // Refresh the goal list
            alert('Goal created successfully!');
            createGoalForm.reset();
            fetchGoals();

        } catch (error) {
            console.error('Error creating goal:', error);
            alert(`Error: ${error.message}`);
        }
    });

    // Initial fetch of goals
    fetchGoals();
});
