"""
Financial goals service for the Financial Literacy Coach
"""
from src.db.models import Goal
from src.ui.display import (
    clear_screen,
    display_title,
    display_goal_progress,
    display_success,
    display_error,
    display_info
)
from src.ui.prompts import (
    prompt_for_goal_details,
    prompt_for_selection,
    prompt_for_float,
    prompt_for_confirmation
)

def goals_menu():
    """
    Display the goals menu
    """
    # This is a placeholder that will be replaced by the CLI's menu handling
    pass

def set_new_goal(user_id):
    """
    Create a new financial goal
    
    Args:
        user_id: User ID
    """
    clear_screen()
    display_title("SET NEW FINANCIAL GOAL")
    display_info("Setting specific financial goals helps you stay focused and motivated.")
    
    # Get goal details
    title, target_amount, current_amount, deadline = prompt_for_goal_details()
    
    if title is None:
        return
    
    # Create goal
    try:
        goal = Goal(
            user_id=user_id,
            title=title,
            target_amount=target_amount,
            current_amount=current_amount,
            deadline=deadline
        )
        
        goal.save()
        
        clear_screen()
        display_success(f"Goal '{title}' created successfully!")
        display_goal_progress(goal)
        
        # Show goal-specific tips
        display_goal_tips(title, target_amount, deadline)
        
    except Exception as e:
        display_error(f"Error creating goal: {str(e)}")
    
    input("\nPress Enter to continue...")

def view_all_goals(user_id):
    """
    View all financial goals
    
    Args:
        user_id: User ID
    """
    goals = Goal.get_all_by_user_id(user_id)
    
    clear_screen()
    display_title("YOUR FINANCIAL GOALS")
    
    if not goals:
        display_error("You don't have any goals yet. Please create one first.")
        input("\nPress Enter to continue...")
        return
    
    # Display progress for each goal
    for goal in goals:
        display_goal_progress(goal)
    
    # Show summary
    display_goals_summary(goals)
    
    input("\nPress Enter to continue...")

def update_goal_progress(user_id):
    """
    Update progress on a financial goal
    
    Args:
        user_id: User ID
    """
    goals = Goal.get_all_by_user_id(user_id)
    
    clear_screen()
    display_title("UPDATE GOAL PROGRESS")
    
    if not goals:
        display_error("You don't have any goals yet. Please create one first.")
        input("\nPress Enter to continue...")
        return
    
    # Create list of goal titles
    goal_titles = []
    for goal in goals:
        status = ""
        if hasattr(goal, 'status') and goal.status:
            if goal.status == "completed":
                status = " (Completed)"
            elif goal.status == "overdue":
                status = " (Overdue)"
        
        goal_titles.append(f"{goal.title}{status} - ${goal.current_amount:.2f} / ${goal.target_amount:.2f}")
    
    # Let user select a goal to update
    selected_idx = prompt_for_selection("Select a goal to update", goal_titles)
    if selected_idx is None:
        return
    
    selected_goal = goals[goal_titles.index(selected_idx)]
    
    clear_screen()
    display_title(f"UPDATE GOAL: {selected_goal.title}")
    display_goal_progress(selected_goal)
    
    # Get new amount
    new_amount = prompt_for_float(
        f"Current amount saved (${selected_goal.current_amount:.2f})",
        min_value=0
    )
    
    if new_amount is None:
        return
    
    # Update goal
    try:
        selected_goal.current_amount = new_amount
        selected_goal.save()
        
        clear_screen()
        display_success(f"Goal '{selected_goal.title}' updated successfully!")
        display_goal_progress(selected_goal)
        
        # Show achievement message if goal completed
        if new_amount >= selected_goal.target_amount:
            display_goal_achievement(selected_goal.title)
        
    except Exception as e:
        display_error(f"Error updating goal: {str(e)}")
    
    input("\nPress Enter to continue...")

def display_goals_summary(goals):
    """
    Display a summary of all goals
    
    Args:
        goals: List of Goal objects
    """
    if not goals:
        return
    
    display_title("GOALS SUMMARY")
    
    # Calculate totals
    total_target = sum(goal.target_amount for goal in goals)
    total_current = sum(goal.current_amount for goal in goals)
    total_remaining = total_target - total_current
    overall_progress = (total_current / total_target * 100) if total_target > 0 else 0
    
    # Count goals by status
    completed = sum(1 for goal in goals if hasattr(goal, 'status') and goal.status == "completed")
    in_progress = sum(1 for goal in goals if hasattr(goal, 'status') and goal.status == "in_progress")
    overdue = sum(1 for goal in goals if hasattr(goal, 'status') and goal.status == "overdue")
    
    print(f"Total Goals: {len(goals)}")
    print(f"Completed: {completed}")
    print(f"In Progress: {in_progress}")
    print(f"Overdue: {overdue}")
    print(f"Total Target Amount: ${total_target:.2f}")
    print(f"Total Current Amount: ${total_current:.2f}")
    print(f"Total Remaining: ${total_remaining:.2f}")
    print(f"Overall Progress: {overall_progress:.1f}%")

def display_goal_tips(title, target_amount, deadline):
    """
    Display tips specific to the goal type
    
    Args:
        title: Goal title
        target_amount: Target amount
        deadline: Goal deadline
    """
    display_title("GOAL TIPS")
    
    # Calculate monthly savings needed if deadline exists
    monthly_tip = ""
    if deadline:
        import datetime
        deadline_date = datetime.datetime.strptime(deadline, "%Y-%m-%d")
        today = datetime.datetime.now()
        months_remaining = (deadline_date.year - today.year) * 12 + deadline_date.month - today.month
        
        if months_remaining > 0:
            monthly_amount = target_amount / months_remaining
            monthly_tip = f"To reach your goal by the deadline, aim to save ${monthly_amount:.2f} each month."
    
    # General tips
    print("• Break your goal into smaller milestones to make it more manageable.")
    print("• Consider setting up automatic transfers to a dedicated savings account.")
    print("• Review your progress regularly and adjust your strategy if needed.")
    
    # Goal-specific tips
    if "emergency" in title.lower():
        print("• Start with a mini emergency fund of $500-$1,000 before building to 3-6 months of expenses.")
        print("• Keep emergency funds in an easily accessible account like a high-yield savings account.")
    elif "textbook" in title.lower():
        print("• Look for used textbooks, rentals, or digital versions to reduce costs.")
        print("• Consider sharing textbooks with classmates when possible.")
    elif "computer" in title.lower():
        print("• Check if your school offers student discounts on technology purchases.")
        print("• Consider timing your purchase during back-to-school sales periods.")
    elif "study abroad" in title.lower():
        print("• Research scholarships specifically for study abroad programs.")
        print("• Factor in all costs including flights, insurance, and local transportation.")
        print("• Consider opening a bank account that doesn't charge foreign transaction fees.")
    elif "car" in title.lower():
        print("• Consider reliable used cars that have lower depreciation.")
        print("• Factor in ongoing costs like insurance, maintenance, and gas.")
        print("• Look into student discounts on auto insurance.")
    elif "spring break" in title.lower() or "travel" in title.lower():
        print("• Book travel and accommodations early for the best prices.")
        print("• Consider traveling with a group to share costs.")
        print("• Look for student travel discounts and packages.")
    elif "graduation" in title.lower():
        print("• Start saving early for post-graduation expenses like interview clothes and moving costs.")
        print("• Factor in potential gap time between graduation and your first job.")
    
    # Show monthly savings tip if applicable
    if monthly_tip:
        print(f"\n{monthly_tip}")

def display_goal_achievement(goal_title):
    """
    Display a congratulatory message for achieving a goal
    
    Args:
        goal_title: Title of the achieved goal
    """
    display_title("GOAL ACHIEVED!")
    print(f"Congratulations on reaching your goal: {goal_title}!")
    print("\nThis is a significant financial achievement that demonstrates your:")
    print("• Ability to set and reach financial targets")
    print("• Discipline in saving regularly")
    print("• Commitment to your financial well-being")
    
    print("\nWhat to do next:")
    print("• Celebrate your achievement (in a budget-friendly way)")
    print("• Set a new goal to maintain your financial momentum")
    print("• Consider increasing your emergency fund or retirement savings")

def delete_goal(user_id):
    """
    Delete a financial goal.
    """
    goals = Goal.get_all_by_user_id(user_id)
    clear_screen()
    display_title("DELETE FINANCIAL GOAL")

    if not goals:
        display_error("You don't have any goals to delete.")
        input("\nPress Enter to continue...")
        return

    options = [
        f"{g.title} — ${g.current_amount:.2f}/${g.target_amount:.2f}"
        for g in goals
    ]
    selected = prompt_for_selection("Select a goal to delete", options)
    if selected is None:
        return

    goal = goals[options.index(selected)]
    confirm = prompt_for_confirmation(
        f"Are you sure you want to delete '{goal.title}'?",
        default='n'
    )
    if not confirm:
        return

    try:
        goal.delete()
        clear_screen()
        display_success(f"Goal '{goal.title}' deleted successfully!")
    except Exception as e:
        display_error(f"Error deleting goal: {e}")

    input("\nPress Enter to continue...")
