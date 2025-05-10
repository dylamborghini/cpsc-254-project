"""
Database models for the Financial Literacy Coach
"""
import json
import sqlite3
from datetime import datetime
from src.db.database import get_db_connection

class User:
    """User model for storing basic user information"""
    
    def __init__(self, username, user_id=None):
        self.id = user_id
        self.username = username
    
    def save(self):
        """Save user to database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE username = ?", (self.username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                self.id = existing_user['id']
                return self.id
            
            # Insert new user
            cursor.execute(
                "INSERT INTO users (username) VALUES (?)",
                (self.username,)
            )
            self.id = cursor.lastrowid
            conn.commit()
            return self.id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT id, username, created_at FROM users WHERE username = ?",
                (username,)
            )
            user_row = cursor.fetchone()
            
            if not user_row:
                return None
            
            user = User(username=user_row['username'], user_id=user_row['id'])
            return user
        except Exception as e:
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT id, username, created_at FROM users WHERE id = ?",
                (user_id,)
            )
            user_row = cursor.fetchone()
            
            if not user_row:
                return None
            
            user = User(username=user_row['username'], user_id=user_row['id'])
            return user
        except Exception as e:
            raise e
        finally:
            conn.close()

class Budget:
    """Budget model for storing user budget information"""
    
    def __init__(self, user_id, income=0, savings=0, expenses=None, income_sources=None, budget_id=None):
        self.id = budget_id
        self.user_id = user_id
        self.income = income
        self.savings = savings
        self.expenses = expenses or []
        self.income_sources = income_sources or []
    
    def save(self):
        """Save budget to database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Begin transaction
            conn.execute("BEGIN")
            
            # Insert or update budget
            if self.id:
                cursor.execute(
                    "UPDATE budgets SET income = ?, savings = ? WHERE id = ?",
                    (self.income, self.savings, self.id)
                )
                
                # Delete existing expenses and income sources for update
                cursor.execute("DELETE FROM expenses WHERE budget_id = ?", (self.id,))
                cursor.execute("DELETE FROM income_sources WHERE budget_id = ?", (self.id,))
            else:
                cursor.execute(
                    "INSERT INTO budgets (user_id, income, savings) VALUES (?, ?, ?)",
                    (self.user_id, self.income, self.savings)
                )
                self.id = cursor.lastrowid
            
            # Insert expenses
            for expense in self.expenses:
                cursor.execute(
                    "INSERT INTO expenses (budget_id, category, amount) VALUES (?, ?, ?)",
                    (self.id, expense['category'], expense['amount'])
                )
            
            # Insert income sources
            for source in self.income_sources:
                cursor.execute(
                    "INSERT INTO income_sources (budget_id, source, amount) VALUES (?, ?, ?)",
                    (self.id, source['source'], source['amount'])
                )
            
            # Commit transaction
            conn.commit()
            return self.id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def get_latest_by_user_id(user_id):
        """Get the most recent budget for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get the latest budget
            cursor.execute(
                """
                SELECT id, user_id, income, savings, created_at 
                FROM budgets 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT 1
                """,
                (user_id,)
            )
            budget_row = cursor.fetchone()
            
            if not budget_row:
                return None
            
            # Create Budget object
            budget = Budget(
                user_id=budget_row['user_id'],
                income=budget_row['income'],
                savings=budget_row['savings'],
                budget_id=budget_row['id']
            )
            
            # Get expenses
            cursor.execute(
                "SELECT category, amount FROM expenses WHERE budget_id = ?",
                (budget.id,)
            )
            expense_rows = cursor.fetchall()
            budget.expenses = [dict(row) for row in expense_rows]
            
            # Get income sources
            cursor.execute(
                "SELECT source, amount FROM income_sources WHERE budget_id = ?",
                (budget.id,)
            )
            income_rows = cursor.fetchall()
            budget.income_sources = [dict(row) for row in income_rows]
            
            return budget
        except Exception as e:
            raise e
        finally:
            conn.close()

class Goal:
    """Goal model for tracking financial goals"""
    
    def __init__(self, user_id, title, target_amount, current_amount=0, deadline=None, goal_id=None):
        self.id = goal_id
        self.user_id = user_id
        self.title = title
        self.target_amount = target_amount
        self.current_amount = current_amount
        self.deadline = deadline
    
    def save(self):
        """Save goal to database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            if self.id:
                # Update existing goal
                cursor.execute(
                    """
                    UPDATE goals 
                    SET title = ?, target_amount = ?, current_amount = ?, deadline = ?
                    WHERE id = ?
                    """,
                    (self.title, self.target_amount, self.current_amount, 
                     self.deadline, self.id)
                )
            else:
                # Insert new goal
                cursor.execute(
                    """
                    INSERT INTO goals 
                    (user_id, title, target_amount, current_amount, deadline) 
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (self.user_id, self.title, self.target_amount, 
                     self.current_amount, self.deadline)
                )
                self.id = cursor.lastrowid
            
            conn.commit()
            return self.id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def update_progress(self, new_amount):
        """Update goal progress"""
        self.current_amount = new_amount
        return self.save()
    
    def delete(self):
        """Delete goal"""
        if not self.id:
            raise ValueError("Cannot delete goal without ID")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM goals WHERE id = ?", (self.id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(goal_id):
        """Get goal by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                SELECT id, user_id, title, target_amount, current_amount, 
                       deadline, created_at
                FROM goals 
                WHERE id = ?
                """,
                (goal_id,)
            )
            goal_row = cursor.fetchone()
            
            if not goal_row:
                return None
            
            goal = Goal(
                user_id=goal_row['user_id'],
                title=goal_row['title'],
                target_amount=goal_row['target_amount'],
                current_amount=goal_row['current_amount'],
                deadline=goal_row['deadline'],
                goal_id=goal_row['id']
            )
            
            return goal
        except Exception as e:
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def get_all_by_user_id(user_id):
        """Get all goals for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                SELECT id, user_id, title, target_amount, current_amount, 
                       deadline, created_at
                FROM goals 
                WHERE user_id = ?
                ORDER BY created_at DESC
                """,
                (user_id,)
            )
            goal_rows = cursor.fetchall()
            
            goals = []
            for row in goal_rows:
                goal = Goal(
                    user_id=row['user_id'],
                    title=row['title'],
                    target_amount=row['target_amount'],
                    current_amount=row['current_amount'],
                    deadline=row['deadline'],
                    goal_id=row['id']
                )
                goals.append(goal)
            
            return goals
        except Exception as e:
            raise e
        finally:
            conn.close()

class Simulation:
    """Model for storing simulation results"""
    
    def __init__(self, user_id, scenario_type, parameters, result=None, simulation_id=None):
        self.id = simulation_id
        self.user_id = user_id
        self.scenario_type = scenario_type
        self.parameters = parameters  # Dictionary to be stored as JSON
        self.result = result  # Dictionary to be stored as JSON
    
    def save(self):
        """Save simulation to database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Convert dictionaries to JSON strings
            parameters_json = json.dumps(self.parameters)
            result_json = json.dumps(self.result) if self.result else None
            
            if self.id:
                cursor.execute(
                    """
                    UPDATE simulations
                    SET scenario_type = ?, parameters = ?, result = ?
                    WHERE id = ?
                    """,
                    (self.scenario_type, parameters_json, result_json, self.id)
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO simulations
                    (user_id, scenario_type, parameters, result)
                    VALUES (?, ?, ?, ?)
                    """,
                    (self.user_id, self.scenario_type, parameters_json, result_json)
                )
                self.id = cursor.lastrowid
            
            conn.commit()
            return self.id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def get_by_user_id(user_id, limit=5):
        """Get recent simulations for a user"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                SELECT id, user_id, scenario_type, parameters, result, created_at
                FROM simulations
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (user_id, limit)
            )
            rows = cursor.fetchall()
            
            simulations = []
            for row in rows:
                # Parse JSON strings back to dictionaries
                parameters = json.loads(row['parameters'])
                result = json.loads(row['result']) if row['result'] else None
                
                simulation = Simulation(
                    user_id=row['user_id'],
                    scenario_type=row['scenario_type'],
                    parameters=parameters,
                    result=result,
                    simulation_id=row['id']
                )
                simulations.append(simulation)
            
            return simulations
        except Exception as e:
            raise e
        finally:
            conn.close()