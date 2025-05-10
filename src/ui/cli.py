"""
Command-line interface for the Financial Literacy Coach
"""
import os
import sys
from src.db.models import User
from src.ui.display import (
    clear_screen, 
    display_menu, 
    display_error,
    display_success
)
from src.ui.prompts import (
    prompt_for_username,
    prompt_for_menu_choice
)
from src.services.budget import (
    budget_menu,
    create_update_budget,
    view_budget_summary,
    add_expense,
    view_expense_history,
    get_budget_recommendations
)
from src.services.knowledge import (
    knowledge_menu,
    ask_financial_question,
    browse_financial_terms
)
from src.services.goals import (
    goals_menu,
    set_new_goal,
    view_all_goals,
    update_goal_progress
)
from src.services.simulator import (
    simulator_menu,
    run_housing_comparison,
    run_meal_plan_calculator,
    run_work_study_simulator,
    run_student_loan_calculator
)

# Current user session
current_user = None

def login():
    """
    Log in or create a user account
    """
    global current_user
    
    while current_user is None:
        clear_screen()
        print("Welcome to the Financial Literacy Coach!")
        print("Please log in or create a new account.\n")
        
        # Get username
        username = prompt_for_username()
        
        if username.lower() == 'exit':
            sys.exit(0)
        
        # Find or create user
        user = User.get_by_username(username)
        
        if user:
            current_user = user
            display_success(f"Welcome back, {username}!")
        else:
            # Create new user
            user = User(username=username)
            user.save()
            current_user = user
            display_success(f"Welcome, {username}! A new account has been created for you.")

def main_menu():
    """
    Display and handle the main menu
    """
    while True:
        clear_screen()
        
        menu_options = [
            "Budget Manager",
            "Financial Knowledge Assistant",
            "Goal Tracker",
            "Financial Simulator",
            "Exit"
        ]
        
        display_menu("FINANCIAL LITERACY COACH", menu_options)
        choice = prompt_for_menu_choice(1, len(menu_options))
        
        if choice == 1:
            # Budget Manager
            budget_manager()
        elif choice == 2:
            # Financial Knowledge Assistant
            knowledge_assistant()
        elif choice == 3:
            # Goal Tracker
            goal_tracker()
        elif choice == 4:
            # Financial Simulator
            financial_simulator()
        elif choice == 5:
            # Exit
            clear_screen()
            print("Thank you for using the Financial Literacy Coach!")
            sys.exit(0)

def budget_manager():
    """
    Budget management menu and functions
    """
    while True:
        clear_screen()
        
        menu_options = [
            "Create/Update Budget",
            "View Budget Summary",
            "Add Expense",
            "View Expense History",
            "Get Budget Recommendations",
            "Back to Main Menu"
        ]
        
        display_menu("BUDGET MANAGER", menu_options)
        choice = prompt_for_menu_choice(1, len(menu_options))
        
        if choice == 1:
            # Create/Update Budget
            create_update_budget(current_user.id)
        elif choice == 2:
            # View Budget Summary
            view_budget_summary(current_user.id)
        elif choice == 3:
            # Add Expense
            add_expense(current_user.id)
        elif choice == 4:
            # View Expense History
            view_expense_history(current_user.id)
        elif choice == 5:
            # Get Budget Recommendations
            get_budget_recommendations(current_user.id)
        elif choice == 6:
            # Back to Main Menu
            return

def knowledge_assistant():
    """
    Financial knowledge assistant menu and functions
    """
    while True:
        clear_screen()
        
        menu_options = [
            "Ask a Financial Question",
            "Browse Financial Terms",
            "Back to Main Menu"
        ]
        
        display_menu("FINANCIAL KNOWLEDGE ASSISTANT", menu_options)
        choice = prompt_for_menu_choice(1, len(menu_options))
        
        if choice == 1:
            # Ask a Financial Question
            ask_financial_question()
        elif choice == 2:
            # Browse Financial Terms
            browse_financial_terms()
        elif choice == 3:
            # Back to Main Menu
            return

def goal_tracker():
    """
    Goal tracking menu and functions
    """
    while True:
        clear_screen()
        
        menu_options = [
            "Set New Goal",
            "View All Goals",
            "Update Goal Progress",
            "Back to Main Menu"
        ]
        
        display_menu("GOAL TRACKER", menu_options)
        choice = prompt_for_menu_choice(1, len(menu_options))
        
        if choice == 1:
            # Set New Goal
            set_new_goal(current_user.id)
        elif choice == 2:
            # View All Goals
            view_all_goals(current_user.id)
        elif choice == 3:
            # Update Goal Progress
            update_goal_progress(current_user.id)
        elif choice == 4:
            # Back to Main Menu
            return

def financial_simulator():
    """
    Financial simulator menu and functions
    """
    while True:
        clear_screen()
        
        menu_options = [
            "Housing Cost Comparison",
            "Meal Plan Calculator",
            "Work-Study Balance",
            "Student Loan Calculator",
            "Back to Main Menu"
        ]
        
        display_menu("FINANCIAL SIMULATOR", menu_options)
        choice = prompt_for_menu_choice(1, len(menu_options))
        
        if choice == 1:
            # Housing Cost Comparison
            run_housing_comparison(current_user.id)
        elif choice == 2:
            # Meal Plan Calculator
            run_meal_plan_calculator(current_user.id)
        elif choice == 3:
            # Work-Study Balance
            run_work_study_simulator(current_user.id)
        elif choice == 4:
            # Student Loan Calculator
            run_student_loan_calculator(current_user.id)
        elif choice == 5:
            # Back to Main Menu
            return

def run_cli():
    """
    Main function to run the CLI
    """
    try:
        # Login or create account
        login()
        
        # Show main menu
        main_menu()
        
    except KeyboardInterrupt:
        clear_screen()
        print("\nThank you for using the Financial Literacy Coach!")
        sys.exit(0)
    except Exception as e:
        display_error(f"An unexpected error occurred: {str(e)}")
        input("\nPress Enter to continue...")
        run_cli()