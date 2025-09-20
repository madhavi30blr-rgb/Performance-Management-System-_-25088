#
# File: backend/main.py
# Description: FastAPI backend for the PMS.
#

import os
from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import DictCursor
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Optional

app = FastAPI()

# Database connection details
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "pms_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except psycopg2.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

# Pydantic models for data validation
class GoalBase(BaseModel):
    description: str = Field(min_length=1)
    due_date: date
    status: str = Field(pattern='^(Draft|In Progress|Completed|Cancelled)$')

class GoalCreate(GoalBase):
    employee_id: int
    manager_id: int

class GoalUpdate(BaseModel):
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None

class Goal(GoalBase):
    goal_id: int
    employee_id: int
    manager_id: int
    class Config:
        orm_mode = True

# --- API Endpoints ---

@app.post("/goals/", response_model=Goal, status_code=201)
def create_goal(goal: GoalCreate):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            try:
                cur.execute(
                    "INSERT INTO goals (employee_id, manager_id, description, due_date, status) VALUES (%s, %s, %s, %s, %s) RETURNING *;",
                    (goal.employee_id, goal.manager_id, goal.description, goal.due_date, goal.status)
                )
                new_goal = cur.fetchone()
                conn.commit()
                return new_goal
            except psycopg2.Error as e:
                conn.rollback()
                raise HTTPException(status_code=400, detail=f"Database error: {e}")

@app.get("/goals/{goal_id}", response_model=Goal)
def read_goal(goal_id: int):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM goals WHERE goal_id = %s;", (goal_id,))
            goal = cur.fetchone()
            if not goal:
                raise HTTPException(status_code=404, detail="Goal not found")
            return goal

@app.put("/goals/{goal_id}", response_model=Goal)
def update_goal(goal_id: int, goal_update: GoalUpdate):
    updates = {k: v for k, v in goal_update.dict().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
    values = list(updates.values())
    values.append(goal_id)
    
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            try:
                cur.execute(
                    f"UPDATE goals SET {set_clause} WHERE goal_id = %s RETURNING *;",
                    tuple(values)
                )
                updated_goal = cur.fetchone()
                if not updated_goal:
                    raise HTTPException(status_code=404, detail="Goal not found")
                conn.commit()
                return updated_goal
            except psycopg2.Error as e:
                conn.rollback()
                raise HTTPException(status_code=400, detail=f"Database error: {e}")

@app.delete("/goals/{goal_id}", status_code=204)
def delete_goal(goal_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM goals WHERE goal_id = %s;", (goal_id,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Goal not found")
            conn.commit()
    return {"message": "Goal deleted successfully"}
