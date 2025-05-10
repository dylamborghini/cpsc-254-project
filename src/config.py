"""
Configuration settings for the Financial Literacy Coach application
"""
import os
import json

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database settings
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'app.db')

# Resources directory
RESOURCES_DIR = os.path.join(BASE_DIR, 'src', 'resources')

# Student budget categories
EXPENSE_CATEGORIES = [
    "Housing",
    "Groceries",
    "Dining Out",
    "Utilities",
    "Transportation",
    "Textbooks",
    "School Supplies",
    "Entertainment",
    "Clothing",
    "Personal Care",
    "Health & Wellness",
    "Insurance",
    "Phone & Internet",
    "Subscriptions",
    "Loan Payments",
    "Miscellaneous"
]

# Income sources for students
INCOME_SOURCES = [
    "Part-time Job",
    "Work Study",
    "Financial Aid",
    "Scholarships",
    "Grants",
    "Family Support",
    "Freelance Work",
    "Summer Savings",
    "Other"
]

# Budget recommendation thresholds (percentages)
BUDGET_THRESHOLDS = {
    "Housing": 30,
    "Food": 15,  # Groceries + Dining Out
    "Transportation": 10,
    "Education": 20,  # Textbooks + School Supplies
    "Entertainment": 5,
    "Savings": 10,
    "Other": 10
}

# Goal categories
GOAL_CATEGORIES = [
    "Emergency Fund",
    "Textbook Fund",
    "Spring Break",
    "Summer Travel",
    "New Computer",
    "Study Abroad",
    "Graduation Expenses",
    "Moving Expenses",
    "Loan Payment",
    "Car Purchase",
    "Other"
]

# UI Settings
ENABLE_COLORS = True
APP_NAME = "Financial Literacy Coach"
VERSION = "1.0.0"

# Load financial knowledge base
def load_knowledge_base():
    """
    Load the financial knowledge base from JSON
    """
    kb_path = os.path.join(RESOURCES_DIR, 'financial_terms.json')
    try:
        with open(kb_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return empty dict if file not found or invalid

# Create necessary directories
def ensure_app_directories():
    """
    Ensure all required directories exist
    """
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    os.makedirs(RESOURCES_DIR, exist_ok=True)