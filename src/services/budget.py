"""
Budget management service for the Financial Literacy Coach
"""
from src.db.models import Budget
from src.ui.display import (
    clear_screen,
    display_title,
    display_budget_summary,
    display_success,
    display_error,
    display_info
)
from src.ui.prompts import (
    prompt_for_budget_income,
    prompt_for_budget_expenses,
    prompt_for_budget_savings,
    prompt_for_float,
    prompt_for_selection,
    prompt_for_confirmation
)
from src.config import BUDGET_THRESHOLDS, EXPENSE_CATEGORIES

def budget_menu(user_id):
    """
    Display the budget management menu
    
    Args:
        user_id: User ID
    """
    # This is a placeholder that will be replaced by the CLI's menu handling
    pass

def create_update_budget(user_id):
    """
    Create or update a budget
    
    Args:
        user_id: User ID
    """
    # Check if user already has a budget
    existing_budget = Budget.get_latest_by_user_id(user_id)
    
    if existing_budget:
        clear_screen()
        display_title("UPDATE BUDGET")
        display_info("You already have a budget. Here's your current budget:")
        display_budget_summary(existing_budget)
        
        update = prompt_for_confirmation("Would you like to update this budget?", default='y')
        if update is None or not update:
            return
    else:
        clear_screen()
        display_title("CREATE NEW BUDGET")
        display_info("Let's create a new budget to help manage your finances.")
    
    # Get income sources
    total_income, income_sources = prompt_for_budget_income()
    if total_income is None:
        return
    
    # Get savings goal
    savings = prompt_for_budget_savings()
    if savings is None:
        return
    
    # Get expenses
    expenses = prompt_for_budget_expenses()
    if expenses is None:
        return
    
    # Create or update budget
    try:
        if existing_budget:
            budget = existing_budget
            budget.income = total_income
            budget.savings = savings
            budget.expenses = expenses
            budget.income_sources = income_sources
        else:
            budget = Budget(
                user_id=user_id,
                income=total_income,
                savings=savings,
                expenses=expenses,
                income_sources=income_sources
            )
        
        budget.save()
        
        clear_screen()
        display_success("Budget saved successfully!")
        display_budget_summary(budget)
        
        # Show recommendations
        recommendations = analyze_budget(budget)
        display_budget_recommendations(recommendations)
        
    except Exception as e:
        display_error(f"Error saving budget: {str(e)}")
    
    input("\nPress Enter to continue...")

def view_budget_summary(user_id):
    """
    View budget summary
    
    Args:
        user_id: User ID
    """
    budget = Budget.get_latest_by_user_id(user_id)
    
    clear_screen()
    display_title("BUDGET SUMMARY")
    
    if not budget:
        display_error("You don't have a budget yet. Please create one first.")
        input("\nPress Enter to continue...")
        return
    
    display_budget_summary(budget)
    input("\nPress Enter to continue...")

def add_expense(user_id):
    """
    Add a new expense to the budget
    
    Args:
        user_id: User ID
    """
    budget = Budget.get_latest_by_user_id(user_id)
    
    clear_screen()
    display_title("ADD EXPENSE")
    
    if not budget:
        display_error("You don't have a budget yet. Please create one first.")
        input("\nPress Enter to continue...")
        return
    
    # Display current budget
    display_budget_summary(budget)
    
    # Get expense category
    category = prompt_for_selection("Select expense category", EXPENSE_CATEGORIES)
    if category is None:
        return
    
    # Get amount
    amount = prompt_for_float(f"Amount for {category} ($)", min_value=0.01)
    if amount is None:
        return
    
    # Add to existing category or create new
    found = False
    for expense in budget.expenses:
        if expense['category'] == category:
            # Ask whether to replace or add
            choice = prompt_for_selection(
                f"You already have an expense for {category}. What would you like to do?",
                ["Add to existing amount", "Replace existing amount"]
            )
            
            if choice is None:
                return
            
            if choice == "Add to existing amount":
                expense['amount'] += amount
            else:
                expense['amount'] = amount
            
            found = True
            break
    
    if not found:
        budget.expenses.append({
            "category": category,
            "amount": amount
        })
    
    # Save updated budget
    budget.save()
    
    clear_screen()
    display_success(f"Expense for {category} updated successfully!")
    display_budget_summary(budget)
    input("\nPress Enter to continue...")

def view_expense_history(user_id):
    """
    View expense history
    
    Args:
        user_id: User ID
    """
    # In a full application, we would store historical expense data
    # For this prototype, we'll just show the current budget's expenses
    
    budget = Budget.get_latest_by_user_id(user_id)
    
    clear_screen()
    display_title("EXPENSE HISTORY")
    
    if not budget:
        display_error("You don't have a budget yet. Please create one first.")
        input("\nPress Enter to continue...")
        return
    
    if not budget.expenses:
        display_info("You don't have any expenses recorded yet.")
        input("\nPress Enter to continue...")
        return
    
    # Sort expenses by amount (descending)
    sorted_expenses = sorted(budget.expenses, key=lambda x: x['amount'], reverse=True)
    
    print(f"{'Category':<20} {'Amount':<15} {'% of Income':<15}")
    print("-" * 50)
    
    for expense in sorted_expenses:
        category = expense['category']
        amount = expense['amount']
        percent = (amount / budget.income * 100) if budget.income > 0 else 0
        
        print(f"{category:<20} ${amount:<13.2f} {percent:<13.1f}%")
    
    print("-" * 50)
    total = sum(expense['amount'] for expense in sorted_expenses)
    total_percent = (total / budget.income * 100) if budget.income > 0 else 0
    print(f"{'TOTAL':<20} ${total:<13.2f} {total_percent:<13.1f}%")
    
    input("\nPress Enter to continue...")

def get_budget_recommendations(user_id):
    """
    Get budget recommendations
    
    Args:
        user_id: User ID
    """
    budget = Budget.get_latest_by_user_id(user_id)
    
    clear_screen()
    display_title("BUDGET RECOMMENDATIONS")
    
    if not budget:
        display_error("You don't have a budget yet. Please create one first.")
        input("\nPress Enter to continue...")
        return
    
    recommendations = analyze_budget(budget)
    display_budget_recommendations(recommendations)
    
    input("\nPress Enter to continue...")

def analyze_budget(budget):
    """
    Analyze a budget and generate recommendations
    
    Args:
        budget: Budget object
    
    Returns:
        dict: Budget analysis and recommendations
    """
    if not budget:
        return {
            "balance": False,
            "recommendations": [
                {
                    "type": "error",
                    "message": "No budget data available for analysis.",
                    "priority": "high"
                }
            ]
        }
    
    # Calculate totals
    total_expenses = sum(expense['amount'] for expense in budget.expenses)
    total_income = budget.income
    savings = budget.savings
    
    # Calculate remaining funds
    remaining = total_income - total_expenses - savings
    
    # Calculate savings ratio
    savings_ratio = (savings / total_income * 100) if total_income > 0 else 0
    
    # Group expenses by category
    grouped_expenses = {}
    for expense in budget.expenses:
        category = expense['category']
        amount = expense['amount']
        
        # Map to general categories for analysis
        general_category = map_to_general_category(category)
        
        if general_category in grouped_expenses:
            grouped_expenses[general_category] += amount
        else:
            grouped_expenses[general_category] = amount
    
    # Calculate expense ratios
    expense_ratios = {}
    for category, amount in grouped_expenses.items():
        ratio = (amount / total_income * 100) if total_income > 0 else 0
        expense_ratios[category] = ratio
    
    # Identify concerns (categories exceeding thresholds)
    concerns = []
    for category, ratio in expense_ratios.items():
        threshold = BUDGET_THRESHOLDS.get(category, 10)  # Default to 10%
        if ratio > threshold:
            concerns.append({
                "category": category,
                "current": ratio,
                "threshold": threshold,
                "excess": ratio - threshold,
                "amount": grouped_expenses[category],
                "saving_potential": (ratio - threshold) * total_income / 100
            })
    
    # Check savings
    if savings_ratio < BUDGET_THRESHOLDS.get("Savings", 10):
        concerns.append({
            "category": "Savings",
            "current": savings_ratio,
            "threshold": BUDGET_THRESHOLDS.get("Savings", 10),
            "excess": 0,
            "amount": savings,
            "saving_potential": 0
        })
    
    # Generate recommendations
    recommendations = []
    
    # Handle overall budget balance
    if remaining < 0:
        recommendations.append({
            "type": "warning",
            "message": f"Your expenses exceed your income by ${abs(remaining):.2f}. You need to reduce expenses or increase income.",
            "priority": "high"
        })
    elif remaining == 0:
        recommendations.append({
            "type": "info",
            "message": "Your budget is balanced exactly with no extra buffer. Consider reducing some expenses to provide flexibility.",
            "priority": "medium"
        })
    else:
        recommendations.append({
            "type": "success",
            "message": f"You have ${remaining:.2f} remaining after expenses and savings. Consider allocating this to additional savings or debt payment.",
            "priority": "low"
        })
    
    # Handle savings rate
    if savings_ratio < 5:
        recommendations.append({
            "type": "warning",
            "message": f"Your savings rate is only {savings_ratio:.1f}%. Aim for at least 10% of income saved for emergencies and future needs.",
            "priority": "high"
        })
    elif savings_ratio < 10:
        recommendations.append({
            "type": "info",
            "message": f"Your savings rate is {savings_ratio:.1f}%. Consider increasing to at least 10% to build financial security.",
            "priority": "medium"
        })
    else:
        recommendations.append({
            "type": "success",
            "message": f"Great job! Your savings rate is {savings_ratio:.1f}%, which meets or exceeds the recommended 10%.",
            "priority": "low"
        })
    
    # Handle expense concerns
    for concern in concerns:
        if concern["category"] != "Savings":  # Savings already handled above
            recommendations.append({
                "type": "warning",
                "message": f"Your spending on {concern['category']} is {concern['current']:.1f}% of your income, which exceeds the recommended {concern['threshold']}%. Reducing this could save you ${concern['saving_potential']:.2f} per month.",
                "priority": "medium"
            })
    
    # Add student-specific recommendations
    recommendations.append({
        "type": "tip",
        "message": "Look for student discounts on textbooks, software, and entertainment to reduce expenses.",
        "priority": "low"
    })
    
    recommendations.append({
        "type": "tip",
        "message": "Consider using campus facilities (gym, library, etc.) instead of paying for external services.",
        "priority": "low"
    })
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings": savings,
        "remaining": remaining,
        "savings_ratio": savings_ratio,
        "expense_ratios": expense_ratios,
        "grouped_expenses": grouped_expenses,
        "concerns": concerns,
        "balance": remaining >= 0,
        "recommendations": recommendations
    }

def display_budget_recommendations(analysis):
    """
    Display budget recommendations
    
    Args:
        analysis: Budget analysis results
    """
    if not analysis or not analysis.get("recommendations"):
        display_error("No recommendations available.")
        return
    
    display_title("RECOMMENDATIONS")
    
    # Display high priority recommendations first
    priorities = ["high", "medium", "low"]
    for priority in priorities:
        shown_priority_header = False
        
        for rec in analysis.get("recommendations", []):
            if rec.get("priority") == priority:
                if not shown_priority_header:
                    if priority == "high":
                        print("\nImportant Actions:")
                    elif priority == "medium":
                        print("\nConsider These Changes:")
                    else:
                        print("\nHelpful Tips:")
                    shown_priority_header = True
                
                rec_type = rec.get("type", "info")
                message = rec.get("message", "")
                
                if rec_type == "warning":
                    display_error(message)
                elif rec_type == "success":
                    display_success(message)
                elif rec_type == "info":
                    display_info(message)
                else:
                    print(f"• {message}")

def map_to_general_category(category):
    """
    Map specific expense categories to general categories used in thresholds
    
    Args:
        category: Specific expense category
    
    Returns:
        str: General category for thresholds
    """
    category_mapping = {
        "Housing": "Housing",
        "Rent": "Housing",
        "Mortgage": "Housing",
        "Dorm": "Housing",
        
        "Groceries": "Food",
        "Dining Out": "Food",
        "Meal Plan": "Food",
        
        "Textbooks": "Education",
        "School Supplies": "Education",
        "Tuition": "Education",
        
        "Bus": "Transportation",
        "Car Payment": "Transportation",
        "Gas": "Transportation",
        "Parking": "Transportation",
        "Transportation": "Transportation",
        
        "Entertainment": "Entertainment",
        "Streaming": "Entertainment",
        "Movies": "Entertainment",
        "Games": "Entertainment",
        
        "Clothing": "Other",
        "Personal Care": "Other",
        "Phone & Internet": "Other",
        "Insurance": "Other",
        "Subscriptions": "Other",
        "Health & Wellness": "Other",
        "Miscellaneous": "Other",
        "Loan Payments": "Other"
    }
    
    return category_mapping.get(category, "Other")