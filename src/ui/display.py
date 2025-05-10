"""
Display functions for the Financial Literacy Coach CLI
"""
import os
import sys
from datetime import datetime
from src.config import ENABLE_COLORS, APP_NAME, VERSION

# ANSI color codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def colored_text(text, color):
    """
    Return colored text if colors are enabled
    """
    if ENABLE_COLORS:
        return f"{color}{text}{Colors.RESET}"
    return text

def display_welcome():
    """
    Display welcome message
    """
    title = f"Welcome to {APP_NAME} v{VERSION}"
    border = "=" * (len(title) + 4)
    
    print(colored_text(border, Colors.BOLD + Colors.BLUE))
    print(colored_text(f"  {title}  ", Colors.BOLD + Colors.BLUE))
    print(colored_text(border, Colors.BOLD + Colors.BLUE))
    print(colored_text("\nYour personal finance guide for university life!", Colors.CYAN))
    print(colored_text("Let's build smart financial habits together.", Colors.CYAN))
    print(f"\nCurrent date: {datetime.now().strftime('%B %d, %Y')}")
    print("\nPress Enter to continue...")
    input()

def display_menu(title, options):
    """
    Display a menu with options
    
    Args:
        title: Menu title
        options: List of menu options
    """
    border = "-" * (len(title) + 4)
    
    print(colored_text(f"\n{title}", Colors.BOLD + Colors.BLUE))
    print(colored_text(border, Colors.BLUE))
    
    for i, option in enumerate(options, 1):
        print(colored_text(f"{i}. {option}", Colors.CYAN if i != len(options) else Colors.YELLOW))
    
    print("\n")

def display_error(message):
    """
    Display an error message
    """
    print(colored_text(f"\nERROR: {message}", Colors.RED))

def display_success(message):
    """
    Display a success message
    """
    print(colored_text(f"\nSUCCESS: {message}", Colors.GREEN))

def display_warning(message):
    """
    Display a warning message
    """
    print(colored_text(f"\nWARNING: {message}", Colors.YELLOW))

def display_info(message):
    """
    Display an info message
    """
    print(colored_text(f"\nINFO: {message}", Colors.CYAN))

def display_title(title):
    """
    Display a section title
    """
    print(colored_text(f"\n{title}", Colors.BOLD + Colors.BLUE))
    print(colored_text("-" * len(title), Colors.BLUE))

def display_budget_summary(budget):
    """
    Display budget summary
    
    Args:
        budget: Budget object with income, expenses, savings
    """
    if not budget:
        display_error("No budget found!")
        return
    
    total_expenses = sum(expense['amount'] for expense in budget.expenses)
    total_income = budget.income
    savings = budget.savings
    remaining = total_income - total_expenses - savings
    
    display_title("BUDGET SUMMARY")
    
    print(f"Total Income:     ${total_income:.2f}")
    print(f"Total Expenses:   ${total_expenses:.2f}")
    print(f"Savings:          ${savings:.2f}")
    print(colored_text(f"Remaining:        ${remaining:.2f}", 
                      Colors.GREEN if remaining >= 0 else Colors.RED))
    
    savings_percent = (savings / total_income * 100) if total_income > 0 else 0
    print(f"Savings Rate:     {savings_percent:.1f}%")
    
    # Display income sources
    if budget.income_sources:
        display_title("INCOME SOURCES")
        for source in budget.income_sources:
            percent = (source['amount'] / total_income * 100) if total_income > 0 else 0
            print(f"{source['source']:<20} ${source['amount']:.2f} ({percent:.1f}%)")
    
    # Display expenses by category
    if budget.expenses:
        display_title("EXPENSES BY CATEGORY")
        for expense in budget.expenses:
            percent = (expense['amount'] / total_income * 100) if total_income > 0 else 0
            print(f"{expense['category']:<20} ${expense['amount']:.2f} ({percent:.1f}%)")

def display_goal_progress(goal):
    """
    Display progress for a single goal
    
    Args:
        goal: Goal object
    """
    progress_percent = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
    remaining = goal.target_amount - goal.current_amount
    
    bar_length = 20
    filled_length = int(progress_percent / 100 * bar_length)
    progress_bar = '█' * filled_length + '░' * (bar_length - filled_length)
    
    # Calculate time information
    time_info = ""
    if goal.deadline:
        try:
            deadline_date = datetime.strptime(goal.deadline, '%Y-%m-%d')
            days_remaining = (deadline_date - datetime.now()).days
            if days_remaining > 0:
                time_info = f"{days_remaining} days remaining"
            else:
                time_info = "Deadline passed"
        except ValueError:
            time_info = "Invalid deadline format"
    
    # Status indicator
    if progress_percent >= 100:
        status = colored_text("COMPLETE", Colors.GREEN)
    elif time_info == "Deadline passed":
        status = colored_text("OVERDUE", Colors.RED)
    else:
        status = colored_text("IN PROGRESS", Colors.YELLOW)
    
    print(f"\n{goal.title}")
    print(f"Target: ${goal.target_amount:.2f}")
    print(f"Current: ${goal.current_amount:.2f} (${remaining:.2f} remaining)")
    print(f"Progress: {progress_bar} {progress_percent:.1f}%")
    if time_info:
        print(f"Time: {time_info}")
    print(f"Status: {status}")

def display_simulation_result(result, scenario_type):
    """
    Display simulation result
    
    Args:
        result: Dictionary with simulation results
        scenario_type: Type of simulation
    """
    if not result:
        display_error("No simulation result available!")
        return
    
    if scenario_type == "housing":
        display_housing_comparison(result)
    elif scenario_type == "meal_plan":
        display_meal_plan_comparison(result)
    elif scenario_type == "work_hours":
        display_work_study_balance(result)
    elif scenario_type == "student_loan":
        display_student_loan_calculation(result)
    else:
        display_error(f"Unknown simulation type: {scenario_type}")

def display_housing_comparison(result):
    """
    Display housing comparison results
    
    Args:
        result: Dictionary with housing comparison results
    """
    display_title("HOUSING COMPARISON RESULTS")
    
    options = result.get("options", [])
    if not options:
        display_error("No housing options found in the results!")
        return
    
    # Display header
    print(f"{'Option':<15} {'Monthly':<12} {'Utilities':<12} {'Commute':<12} {'Total':<12}")
    print("-" * 65)
    
    # Display options
    for option in options:
        name = option.get("name", "Option")
        monthly = option.get("monthly", {})
        
        print(f"{name:<15} ${monthly.get('rent', 0):<10.2f} ${monthly.get('utilities', 0):<10.2f} ${monthly.get('commute', 0):<10.2f} ${monthly.get('total', 0):<10.2f}")
    
    # Display recommendation
    recommendation = result.get("recommendation")
    if recommendation:
        print(f"\nRecommended Option: {colored_text(recommendation, Colors.GREEN)}")
        
    # Display savings potential
    savings = result.get("savings_potential", 0)
    if savings > 0:
        print(f"Potential Savings: {colored_text(f'${savings:.2f}', Colors.GREEN)} over {result.get('timeframe', 9)} months")

def display_meal_plan_comparison(result):
    """
    Display meal plan comparison results
    
    Args:
        result: Dictionary with meal plan comparison results
    """
    display_title("MEAL PLAN COMPARISON RESULTS")
    
    options = result.get("options", [])
    if not options:
        display_error("No meal options found in the results!")
        return
    
    # Display options
    for option in options:
        name = option.get("name", "Option")
        total_cost = option.get("total_cost", 0)
        cost_per_meal = option.get("cost_per_meal", 0)
        time_investment = option.get("time_investment_hours", 0)
        features = option.get("features", {})
        
        print(f"\n{colored_text(name, Colors.BOLD)}")
        print(f"Total Cost: ${total_cost:.2f}")
        print(f"Cost Per Meal: ${cost_per_meal:.2f}")
        print(f"Time Investment: {time_investment:.1f} hours")
        
        if features:
            print("Features:")
            for key, value in features.items():
                print(f"  - {key.replace('_', ' ').title()}: {value}")
    
    # Display comparison
    comparison = result.get("comparison", {})
    if comparison:
        cost_diff = comparison.get("cost_difference", 0)
        cheaper = comparison.get("cheaper_option", "")
        time_diff = comparison.get("time_difference", 0)
        time_efficient = comparison.get("more_time_efficient", "")
        
        print(f"\n{colored_text('Comparison:', Colors.BOLD)}")
        print(f"Cost Difference: ${cost_diff:.2f} (cheaper: {cheaper})")
        print(f"Time Difference: {time_diff:.1f} hours (more efficient: {time_efficient})")
    
    # Display recommendation
    recommendation = result.get("recommendation")
    reason = result.get("recommendation_reason", "")
    if recommendation:
        print(f"\nRecommended Option: {colored_text(recommendation, Colors.GREEN)}")
        if reason:
            print(f"Reason: {reason}")

def display_work_study_balance(result):
    """
    Display work-study balance results
    
    Args:
        result: Dictionary with work-study balance results
    """
    display_title("WORK-STUDY BALANCE RESULTS")
    
    options = result.get("options", [])
    if not options:
        display_error("No work hour options found in the results!")
        return
    
    # Display header
    print(f"{'Hours':<8} {'Weekly $':<12} {'GPA Impact':<12} {'Personal Hours':<15} {'Warnings'}")
    print("-" * 70)
    
    # Display options with warnings highlighted
    for option in options:
        hours = option.get("weekly_hours", 0)
        financial = option.get("financial", {})
        academic = option.get("academic", {})
        time = option.get("time", {})
        warnings = option.get("warnings", [])
        
        warning_text = ", ".join(warnings) if warnings else "None"
        warning_color = Colors.RED if warnings else Colors.GREEN
        
        print(f"{hours:<8} ${financial.get('weekly_income', 0):<10.2f} {academic.get('gpa_change', 0):<+10.2f} {time.get('personal', 0):<15.1f} {colored_text(warning_text, warning_color)}")
    
    # Display recommendation
    recommendation = result.get("recommendation", 0)
    reasoning = result.get("recommendation_reasoning", "")
    
    print(f"\nRecommended Work Hours: {colored_text(str(recommendation), Colors.GREEN)}")
    if reasoning:
        print(f"Reasoning: {reasoning}")

def display_student_loan_calculation(result):
    """
    Display student loan calculation results
    
    Args:
        result: Dictionary with student loan calculation results
    """
    display_title("STUDENT LOAN CALCULATION RESULTS")
    
    loan_details = result.get("loan_details", {})
    standard = result.get("standard_repayment", {})
    ibr = result.get("income_based_repayment", {})
    affordability = result.get("affordability", {})
    
    # Display loan details
    print(colored_text("Loan Details:", Colors.BOLD))
    print(f"Principal Amount: ${loan_details.get('principal', 0):.2f}")
    print(f"Interest Rate: {loan_details.get('interest_rate', 0):.2f}%")
    print(f"Loan Term: {loan_details.get('term_years', 0)} years")
    
    # Display standard repayment
    print(f"\n{colored_text('Standard Repayment Plan:', Colors.BOLD)}")
    print(f"Monthly Payment: ${standard.get('monthly_payment', 0):.2f}")
    print(f"Total Payments: {standard.get('total_payments', 0)} months ({standard.get('total_payments', 0)/12:.1f} years)")
    print(f"Total Repaid: ${standard.get('total_repaid', 0):.2f}")
    print(f"Total Interest: ${standard.get('total_interest', 0):.2f}")
    
    # Display income-based repayment
    print(f"\n{colored_text('Income-Based Repayment Plan:', Colors.BOLD)}")
    print(f"Monthly Payment: ${ibr.get('monthly_payment', 0):.2f}")
    
    estimated_months = ibr.get('estimated_months', 0)
    if isinstance(estimated_months, str):
        print(f"Estimated Time to Repay: {estimated_months}")
    else:
        print(f"Estimated Time to Repay: {estimated_months:.1f} months ({estimated_months/12:.1f} years)")
    
    total_repaid = ibr.get('total_repaid', 0)
    if isinstance(total_repaid, str):
        print(f"Total Repaid: {total_repaid}")
    else:
        print(f"Total Repaid: ${total_repaid:.2f}")
    
    # Display affordability metrics
    print(f"\n{colored_text('Affordability Analysis:', Colors.BOLD)}")
    
    percent_income = affordability.get('percent_of_expected_income', 0)
    print(f"Percent of Expected Income: {percent_income:.1f}%")
    
    risk_level = affordability.get('risk_level', 'Unknown')
    risk_color = Colors.GREEN if risk_level == 'Low' else Colors.YELLOW if risk_level == 'Medium' else Colors.RED
    print(f"Risk Level: {colored_text(risk_level, risk_color)}")
    
    # Display recommendation
    recommendation = result.get('recommendation')
    reasoning = result.get('recommendation_reasoning', '')
    
    if recommendation:
        print(f"\nRecommended Repayment Plan: {colored_text(recommendation.title(), Colors.GREEN)}")
        if reasoning:
            print(f"Reasoning: {reasoning}")

def display_financial_term(term, info):
    """
    Display information about a financial term
    
    Args:
        term: The term name
        info: Dictionary with term information
    """
    display_title(term.upper())
    
    # Display definition
    print(colored_text("Definition:", Colors.BOLD))
    print(info.get("definition", "No definition available."))
    
    # Display student context if available
    student_context = info.get("student_context")
    if student_context:
        print(f"\n{colored_text('Student Context:', Colors.BOLD)}")
        print(student_context)
    
    # Display how-to if available
    how_to = info.get("how_to")
    if how_to:
        print(f"\n{colored_text('How To:', Colors.BOLD)}")
        print(how_to)
    
    # Display student advice if available
    advice = info.get("student_advice")
    if advice:
        print(f"\n{colored_text('Student Advice:', Colors.BOLD)}")
        print(advice)
    
    # Display formula if available
    formula = info.get("formula")
    if formula:
        print(f"\n{colored_text('Formula:', Colors.BOLD)}")
        print(formula)
    
    # Display calculation example if available
    example = info.get("calculation_example")
    if example:
        print(f"\n{colored_text('Example:', Colors.BOLD)}")
        print(example)
    
    # Display aliases if available
    aliases = info.get("aliases", [])
    if aliases:
        print(f"\n{colored_text('Also Known As:', Colors.BOLD)}")
        print(", ".join(aliases))