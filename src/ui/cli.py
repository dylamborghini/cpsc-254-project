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
    display_success,
    display_title,
    display_info
)
from src.ui.prompts import (
    prompt_for_username,
    prompt_for_menu_choice
)
from src.services.budget import (
    create_update_budget,
    record_new_budget,
    view_budget_summary,
    add_expense,
    view_expense_history,
    get_budget_recommendations,
    forecast_spending
)
from src.services.knowledge import (
    ask_financial_question,
    browse_financial_terms
)
from src.services.goals import (
    set_new_goal,
    view_all_goals,
    update_goal_progress,
    delete_goal
)
from src.services.simulator import (
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

        username = prompt_for_username()
        if username.lower() == 'exit':
            sys.exit(0)

        user = User.get_by_username(username)
        if user:
            current_user = user
            display_success(f"Welcome back, {username}!")
        else:
            user = User(username=username)
            user.save()
            current_user = user
            display_success(f"Welcome, {username}! A new account has been created for you.")
        input("\nPress Enter to continue…")

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

        display_menu(f"FINANCIAL LITERACY COACH — User: {current_user.username}", menu_options)
        choice = prompt_for_menu_choice(1, len(menu_options))

        if choice == 1:
            budget_manager()
        elif choice == 2:
            knowledge_assistant()
        elif choice == 3:
            goal_tracker()
        elif choice == 4:
            financial_simulator()
        elif choice == 5:
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
            "Record New Budget Entry",
            "View Budget Summary",
            "Add Expense",
            "View Expense History",
            "Get Budget Recommendations",
            "Forecast Spending",
            "Back to Main Menu"
        ]
        
        display_menu("BUDGET MANAGER", menu_options)
        choice = prompt_for_menu_choice(1, len(menu_options))
        
        if choice == 1:
            create_update_budget(current_user.id)
        elif choice == 2:
            record_new_budget(current_user.id)
        elif choice == 3:
            view_budget_summary(current_user.id)
        elif choice == 4:
            add_expense(current_user.id)
        elif choice == 5:
            view_expense_history(current_user.id)
        elif choice == 6:
            get_budget_recommendations(current_user.id)
        elif choice == 7:
            clear_screen()
            display_title("SPENDING FORECAST")
            prediction = forecast_spending(current_user.id)
            if prediction is None:
                display_error("Not enough data to forecast; using last known expenses.")
            else:
                display_info(f"Next month's projected total expenses: ${prediction:.2f}")
            input("\nPress Enter to continue...")
        elif choice == 8:
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
            ask_financial_question()
        elif choice == 2:
            browse_financial_terms()
        elif choice == 3:
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
            "Delete Goal",
            "Back to Main Menu"
        ]

        display_menu("GOAL TRACKER", menu_options)
        choice = prompt_for_menu_choice(1, len(menu_options))

        if choice == 1:
            set_new_goal(current_user.id)
        elif choice == 2:
            view_all_goals(current_user.id)
        elif choice == 3:
            update_goal_progress(current_user.id)
        elif choice == 4:
            delete_goal(current_user.id)
        elif choice == 5:
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
            run_housing_comparison(current_user.id)
        elif choice == 2:
            run_meal_plan_calculator(current_user.id)
        elif choice == 3:
            run_work_study_simulator(current_user.id)
        elif choice == 4:
            run_student_loan_calculator(current_user.id)
        elif choice == 5:
            return

def run_cli():
    """
    Main function to run the CLI
    """
    try:
        login()
        main_menu()
    except KeyboardInterrupt:
        clear_screen()
        print("\nThank you for using the Financial Literacy Coach!")
        sys.exit(0)
    except Exception as e:
        display_error(f"An unexpected error occurred: {e}")
        input("\nPress Enter to continue...")
        run_cli()
