"""
User input prompts for the Financial Literacy Coach CLI
"""
import sys
from datetime import datetime
from src.ui.display import colored_text, Colors, display_error

def prompt_for_username():
    """
    Prompt user for a username
    
    Returns:
        str: Username
    """
    while True:
        username = input(colored_text("Username (type 'exit' to quit): ", Colors.CYAN)).strip()
        
        if not username:
            display_error("Username cannot be empty. Please try again.")
            continue
        
        if len(username) < 3:
            display_error("Username must be at least 3 characters long.")
            continue
        
        return username

def prompt_for_menu_choice(min_value, max_value):
    """
    Prompt user to select from a menu
    
    Args:
        min_value: Minimum valid value (inclusive)
        max_value: Maximum valid value (inclusive)
    
    Returns:
        int: Selected menu option
    """
    while True:
        try:
            choice = input(colored_text(f"Enter your choice ({min_value}-{max_value}): ", Colors.CYAN))
            
            # Check for exit command
            if choice.lower() in ['q', 'quit', 'exit']:
                print("\nReturning to previous menu...")
                return max_value  # Return the "back" option
            
            choice_int = int(choice)
            
            if min_value <= choice_int <= max_value:
                return choice_int
            else:
                display_error(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            display_error("Please enter a valid number.")

def prompt_for_float(prompt_text, min_value=None, max_value=None, allow_zero=True):
    """
    Prompt user for a floating-point value
    
    Args:
        prompt_text: Text to display for the prompt
        min_value: Minimum valid value (inclusive)
        max_value: Maximum valid value (inclusive)
        allow_zero: Whether zero is allowed as a valid input
    
    Returns:
        float: The input value
    """
    while True:
        try:
            value = input(colored_text(f"{prompt_text}: ", Colors.CYAN))
            
            # Check for back command
            if value.lower() in ['b', 'back']:
                return None
            
            value_float = float(value)
            
            # Check if zero is allowed
            if not allow_zero and value_float == 0:
                display_error("Value cannot be zero.")
                continue
            
            # Check min value if specified
            if min_value is not None and value_float < min_value:
                display_error(f"Value must be at least {min_value}.")
                continue
            
            # Check max value if specified
            if max_value is not None and value_float > max_value:
                display_error(f"Value must be at most {max_value}.")
                continue
            
            return value_float
        except ValueError:
            display_error("Please enter a valid number.")

def prompt_for_int(prompt_text, min_value=None, max_value=None, allow_zero=True):
    """
    Prompt user for an integer value
    
    Args:
        prompt_text: Text to display for the prompt
        min_value: Minimum valid value (inclusive)
        max_value: Maximum valid value (inclusive)
        allow_zero: Whether zero is allowed as a valid input
    
    Returns:
        int: The input value
    """
    while True:
        try:
            value = input(colored_text(f"{prompt_text}: ", Colors.CYAN))
            
            # Check for back command
            if value.lower() in ['b', 'back']:
                return None
            
            value_int = int(value)
            
            # Check if zero is allowed
            if not allow_zero and value_int == 0:
                display_error("Value cannot be zero.")
                continue
            
            # Check min value if specified
            if min_value is not None and value_int < min_value:
                display_error(f"Value must be at least {min_value}.")
                continue
            
            # Check max value if specified
            if max_value is not None and value_int > max_value:
                display_error(f"Value must be at most {max_value}.")
                continue
            
            return value_int
        except ValueError:
            display_error("Please enter a valid integer.")

def prompt_for_date(prompt_text, allow_past=True, allow_empty=False):
    """
    Prompt user for a date in YYYY-MM-DD format
    
    Args:
        prompt_text: Text to display for the prompt
        allow_past: Whether past dates are allowed
        allow_empty: Whether empty input is allowed
    
    Returns:
        str: Date string in YYYY-MM-DD format, or None if empty and allowed
    """
    while True:
        date_str = input(colored_text(f"{prompt_text} (YYYY-MM-DD or 'back'): ", Colors.CYAN))
        
        # Check for back command
        if date_str.lower() in ['b', 'back']:
            return None
        
        # Check if empty is allowed
        if not date_str and allow_empty:
            return None
        elif not date_str:
            display_error("Date cannot be empty.")
            continue
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Check if past dates are allowed
            if not allow_past and date_obj.date() < datetime.now().date():
                display_error("Date cannot be in the past.")
                continue
            
            return date_str
        except ValueError:
            display_error("Please enter a valid date in YYYY-MM-DD format.")

def prompt_for_text(prompt_text, min_length=None, max_length=None, allow_empty=False):
    """
    Prompt user for text input
    
    Args:
        prompt_text: Text to display for the prompt
        min_length: Minimum length of text (inclusive)
        max_length: Maximum length of text (inclusive)
        allow_empty: Whether empty input is allowed
    
    Returns:
        str: The input text, or None if empty and allowed
    """
    while True:
        text = input(colored_text(f"{prompt_text}: ", Colors.CYAN))
        
        # Check for back command
        if text.lower() in ['b', 'back']:
            return None
        
        # Check if empty is allowed
        if not text and allow_empty:
            return None
        elif not text:
            display_error("Input cannot be empty.")
            continue
        
        # Check min length if specified
        if min_length is not None and len(text) < min_length:
            display_error(f"Input must be at least {min_length} characters long.")
            continue
        
        # Check max length if specified
        if max_length is not None and len(text) > max_length:
            display_error(f"Input must be at most {max_length} characters long.")
            continue
        
        return text

def prompt_for_confirmation(prompt_text, default=None):
    """
    Prompt user for yes/no confirmation
    
    Args:
        prompt_text: Text to display for the prompt
        default: Default value if user just presses enter ('y', 'n', or None)
    
    Returns:
        bool: True for yes, False for no
    """
    default_text = ""
    if default is not None:
        default_text = f" [{'Y/n' if default.lower() == 'y' else 'y/N'}]"
    
    while True:
        response = input(colored_text(f"{prompt_text}{default_text}: ", Colors.CYAN)).strip().lower()
        
        # Check for back command
        if response in ['b', 'back']:
            return None
        
        # Use default if empty and default is provided
        if not response and default is not None:
            response = default.lower()
        
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            display_error("Please enter 'y' or 'n'.")

def prompt_for_selection(prompt_text, options, allow_back=True):
    """
    Prompt user to select from a list of options
    
    Args:
        prompt_text: Text to display for the prompt
        options: List of options to choose from
        allow_back: Whether to allow going back
    
    Returns:
        The selected option, or None if back is selected
    """
    if not options:
        display_error("No options available for selection.")
        return None
    
    print(colored_text(f"\n{prompt_text}:", Colors.BOLD))
    
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    if allow_back:
        print(f"{len(options) + 1}. Back")
    
    max_value = len(options) + (1 if allow_back else 0)
    choice = prompt_for_menu_choice(1, max_value)
    
    if allow_back and choice == max_value:
        return None
    
    return options[choice - 1]

def prompt_for_multichoice(prompt_text, options, allow_back=True):
    """
    Prompt user to select multiple options from a list
    
    Args:
        prompt_text: Text to display for the prompt
        options: List of options to choose from
        allow_back: Whether to allow going back
    
    Returns:
        List of selected options, or None if back is selected
    """
    if not options:
        display_error("No options available for selection.")
        return None
    
    print(colored_text(f"\n{prompt_text}:", Colors.BOLD))
    print("(Enter option numbers separated by commas, e.g., '1,3,5')")
    
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    if allow_back:
        print(f"b. Back")
    
    while True:
        response = input(colored_text("Enter your choices: ", Colors.CYAN)).strip()
        
        # Check for back command
        if allow_back and response.lower() in ['b', 'back']:
            return None
        
        # Process comma-separated selection
        try:
            if ',' in response:
                # Multiple selections
                selected_indices = [int(i.strip()) for i in response.split(',')]
            else:
                # Single selection
                selected_indices = [int(response)]
            
            # Validate selections
            valid_indices = True
            for idx in selected_indices:
                if idx < 1 or idx > len(options):
                    valid_indices = False
                    break
            
            if not valid_indices:
                display_error(f"Please enter valid option numbers (1-{len(options)}).")
                continue
            
            # Return selected options
            return [options[idx - 1] for idx in selected_indices]
        except ValueError:
            display_error("Please enter valid option numbers.")

def prompt_for_budget_income():
    """
    Prompt user for budget income details
    
    Returns:
        tuple: (total_income, income_sources)
    """
    from src.config import INCOME_SOURCES
    
    print(colored_text("\nINCOME SOURCES", Colors.BOLD))
    print("Enter your monthly income from each source (enter 0 if not applicable)")
    
    income_sources = []
    total_income = 0
    
    for source in INCOME_SOURCES:
        amount = prompt_for_float(f"{source}", min_value=0)
        
        if amount is None:  # User entered 'back'
            return None, None
        
        if amount > 0:
            income_sources.append({"source": source, "amount": amount})
            total_income += amount
    
    return total_income, income_sources

def prompt_for_budget_expenses():
    """
    Prompt user for budget expense details
    
    Returns:
        list: List of expense dictionaries
    """
    from src.config import EXPENSE_CATEGORIES
    
    print(colored_text("\nEXPENSE CATEGORIES", Colors.BOLD))
    print("Enter your monthly expenses for each category (enter 0 if not applicable)")
    
    expenses = []
    
    for category in EXPENSE_CATEGORIES:
        amount = prompt_for_float(f"{category}", min_value=0)
        
        if amount is None:  # User entered 'back'
            return None
        
        if amount > 0:
            expenses.append({"category": category, "amount": amount})
    
    return expenses

def prompt_for_budget_savings():
    """
    Prompt user for monthly savings target
    
    Returns:
        float: Savings amount
    """
    print(colored_text("\nSAVINGS GOAL", Colors.BOLD))
    savings = prompt_for_float("Monthly savings target", min_value=0)
    
    return savings

def prompt_for_goal_details():
    """
    Prompt user for financial goal details
    
    Returns:
        tuple: (title, target_amount, current_amount, deadline)
    """
    from src.config import GOAL_CATEGORIES
    
    print(colored_text("\nNEW FINANCIAL GOAL", Colors.BOLD))
    
    # Goal category selection
    goal_category = prompt_for_selection("Select goal category", GOAL_CATEGORIES)
    if goal_category is None:
        return None, None, None, None
    
    # Custom title
    if goal_category == "Other":
        title = prompt_for_text("Enter goal title", min_length=3, max_length=50)
    else:
        title = goal_category
    
    if title is None:
        return None, None, None, None
    
    # Target amount
    target_amount = prompt_for_float("Target amount ($)", min_value=1)
    if target_amount is None:
        return None, None, None, None
    
    # Current amount (if already started)
    current_amount = prompt_for_float("Current amount ($) (0 if just starting)", min_value=0)
    if current_amount is None:
        return None, None, None, None
    
    # Deadline (optional)
    deadline = prompt_for_date("Deadline", allow_past=False, allow_empty=True)
    
    return title, target_amount, current_amount, deadline

def prompt_for_housing_comparison_params():
    """
    Prompt user for housing comparison parameters
    
    Returns:
        dict: Housing comparison parameters
    """
    print(colored_text("\nHOUSING COST COMPARISON", Colors.BOLD))
    print("Let's compare different housing options")
    
    # Number of months to simulate
    timeframe = prompt_for_int("Number of months to simulate (e.g., 9 for academic year)", 
                              min_value=1, max_value=60, allow_zero=False)
    if timeframe is None:
        return None
    
    # Housing options
    options = []
    while True:
        print(colored_text(f"\nOption #{len(options) + 1}", Colors.BOLD))
        
        # Option name
        name = prompt_for_text("Option name (e.g., 'On-campus dorm', 'Off-campus apartment')", 
                              min_length=3, max_length=30)
        if name is None:
            if options:  # If we have at least one option, allow going back to continue
                break
            return None
        
        # Monthly rent
        cost = prompt_for_float("Monthly rent ($)", min_value=0)
        if cost is None:
            if options:
                break
            return None
        
        # Utilities
        utilities = prompt_for_float("Monthly utilities ($)", min_value=0)
        if utilities is None:
            if options:
                break
            return None
        
        # Commute cost
        commute_cost = prompt_for_float("Monthly commute cost ($)", min_value=0)
        if commute_cost is None:
            if options:
                break
            return None
        
        # Commute time
        commute_time = prompt_for_float("Daily commute time (hours)", min_value=0, max_value=24)
        if commute_time is None:
            if options:
                break
            return None
        
        # Distance to campus
        distance = prompt_for_float("Distance to campus (miles)", min_value=0)
        if distance is None:
            if options:
                break
            return None
        
        # Roommates
        roommates = prompt_for_int("Number of roommates (0 if living alone)", min_value=0)
        if roommates is None:
            if options:
                break
            return None
        
        # Furnished
        furnished = prompt_for_confirmation("Is it furnished?", default='n')
        if furnished is None:
            if options:
                break
            return None
        
        # Add option to list
        options.append({
            "name": name,
            "cost": cost,
            "utilities": utilities,
            "commute_cost": commute_cost,
            "commute_time": commute_time,
            "distance": distance,
            "roommates": roommates,
            "furnished": furnished
        })
        
        # Ask if user wants to add another option
        if len(options) >= 5:
            print("Maximum of 5 options reached.")
            break
        
        add_another = prompt_for_confirmation("Add another housing option?", default='y')
        if add_another is None or not add_another:
            break
    
    # Ensure we have at least two options for comparison
    if len(options) < 2:
        display_error("At least two housing options are needed for comparison.")
        return None
    
    return {
        "options": options,
        "timeframe": timeframe
    }

def prompt_for_meal_plan_params():
    """
    Prompt user for meal plan comparison parameters
    
    Returns:
        dict: Meal plan comparison parameters
    """
    print(colored_text("\nMEAL PLAN CALCULATOR", Colors.BOLD))
    print("Let's compare meal plan costs with self-prepared meals")
    
    # Meal plan details
    print(colored_text("\nMeal Plan Details", Colors.BOLD))
    meal_plan_cost = prompt_for_float("Total meal plan cost for the term ($)", min_value=0)
    if meal_plan_cost is None:
        return None
    
    meals_per_week = prompt_for_int("Number of meals included per week", min_value=0)
    if meals_per_week is None:
        return None
    
    # Self-prepared meal details
    print(colored_text("\nSelf-Prepared Meal Details", Colors.BOLD))
    grocery_budget = prompt_for_float("Weekly grocery budget ($)", min_value=0)
    if grocery_budget is None:
        return None
    
    dining_out_budget = prompt_for_float("Weekly dining out budget ($)", min_value=0)
    if dining_out_budget is None:
        return None
    
    # Term length
    weeks = prompt_for_int("Number of weeks in the term", min_value=1, max_value=52)
    if weeks is None:
        return None
    
    return {
        "meal_plan_cost": meal_plan_cost,
        "meals_per_week": meals_per_week,
        "grocery_budget": grocery_budget,
        "dining_out_budget": dining_out_budget,
        "weeks": weeks
    }

def prompt_for_work_study_params():
    """
    Prompt user for work-study balance parameters
    
    Returns:
        dict: Work-study balance parameters
    """
    print(colored_text("\nWORK-STUDY BALANCE CALCULATOR", Colors.BOLD))
    print("Let's analyze how work hours affect your finances and academics")
    
    # Hourly wage
    hourly_wage = prompt_for_float("Hourly wage ($)", min_value=1)
    if hourly_wage is None:
        return None
    
    # Current GPA
    current_gpa = prompt_for_float("Current GPA", min_value=0, max_value=4.0)
    if current_gpa is None:
        return None
    
    # Study impact factor
    print("\nHow much do work hours affect your studies?")
    impact_options = ["Minimal impact", "Moderate impact", "Significant impact"]
    impact_choice = prompt_for_selection("Impact level", impact_options)
    if impact_choice is None:
        return None
    
    # Convert impact choice to numerical factor
    if impact_choice == "Minimal impact":
        study_impact = 0.02
    elif impact_choice == "Moderate impact":
        study_impact = 0.03
    else:  # Significant impact
        study_impact = 0.05
    
    # Work hour options to compare
    possible_hours = [0, 10, 15, 20, 25, 30, 40]
    
    # Term length
    weeks = prompt_for_int("Number of weeks in the term", min_value=1, max_value=52)
    if weeks is None:
        return None
    
    return {
        "hourly_wage": hourly_wage,
        "current_gpa": current_gpa,
        "study_impact": study_impact,
        "possible_hours": possible_hours,
        "weeks": weeks
    }

def prompt_for_student_loan_params():
    """
    Prompt user for student loan calculation parameters
    
    Returns:
        dict: Student loan parameters
    """
    print(colored_text("\nSTUDENT LOAN CALCULATOR", Colors.BOLD))
    print("Let's analyze your student loan repayment options")
    
    # Loan amount
    loan_amount = prompt_for_float("Total loan amount ($)", min_value=1)
    if loan_amount is None:
        return None
    
    # Interest rate
    interest_rate = prompt_for_float("Annual interest rate (%)", min_value=0, max_value=30)
    if interest_rate is None:
        return None
    
    # Loan term
    loan_term = prompt_for_int("Loan term (years)", min_value=1, max_value=30)
    if loan_term is None:
        return None
    
    # Expected starting salary
    expected_salary = prompt_for_float("Expected annual salary after graduation ($)", min_value=1)
    if expected_salary is None:
        return None
    
    # Repayment method
    repayment_options = ["Standard", "Income-Based"]
    repayment_method = prompt_for_selection("Repayment method", repayment_options)
    if repayment_method is None:
        return None
    
    return {
        "loan_amount": loan_amount,
        "interest_rate": interest_rate,
        "loan_term": loan_term,
        "expected_salary": expected_salary,
        "repayment_method": repayment_method.lower()
    }