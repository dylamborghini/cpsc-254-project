"""
Financial simulation service for the Financial Literacy Coach
"""
import json
from src.db.models import Simulation
from src.ui.display import (
    clear_screen,
    display_title,
    display_simulation_result,
    display_success,
    display_error,
    display_info
)
from src.ui.prompts import (
    prompt_for_housing_comparison_params,
    prompt_for_meal_plan_params,
    prompt_for_work_study_params,
    prompt_for_student_loan_params,
    prompt_for_confirmation,
    prompt_for_selection
)

def simulator_menu():
    """
    Display the financial simulator menu
    """
    # This is a placeholder that will be replaced by the CLI's menu handling
    pass

def run_housing_comparison(user_id):
    """
    Run housing cost comparison simulation
    
    Args:
        user_id: User ID
    """
    clear_screen()
    display_title("HOUSING COST COMPARISON")
    display_info("Compare different housing options to find the most cost-effective choice.")
    
    # Get simulation parameters
    params = prompt_for_housing_comparison_params()
    if params is None:
        return
    
    # Run simulation
    result = simulate_housing(params)
    
    # Save simulation
    try:
        simulation = Simulation(
            user_id=user_id,
            scenario_type="housing",
            parameters=params,
            result=result
        )
        simulation.save()
    except Exception as e:
        display_error(f"Failed to save simulation: {str(e)}")
    
    # Display results
    clear_screen()
    display_title("HOUSING COMPARISON RESULTS")
    display_simulation_result(result, "housing")
    
    # Ask if user wants to explore another housing scenario
    another = prompt_for_confirmation("Would you like to compare different housing options?", default='n')
    if another:
        run_housing_comparison(user_id)
    else:
        input("\nPress Enter to continue...")

def run_meal_plan_calculator(user_id):
    """
    Run meal plan calculator simulation
    
    Args:
        user_id: User ID
    """
    clear_screen()
    display_title("MEAL PLAN CALCULATOR")
    display_info("Compare the cost of a meal plan to preparing your own meals.")
    
    # Get simulation parameters
    params = prompt_for_meal_plan_params()
    if params is None:
        return
    
    # Run simulation
    result = simulate_meal_plan(params)
    
    # Save simulation
    try:
        simulation = Simulation(
            user_id=user_id,
            scenario_type="meal_plan",
            parameters=params,
            result=result
        )
        simulation.save()
    except Exception as e:
        display_error(f"Failed to save simulation: {str(e)}")
    
    # Display results
    clear_screen()
    display_title("MEAL PLAN COMPARISON RESULTS")
    display_simulation_result(result, "meal_plan")
    
    # Ask if user wants to explore another meal plan scenario
    another = prompt_for_confirmation("Would you like to compare different meal plan scenarios?", default='n')
    if another:
        run_meal_plan_calculator(user_id)
    else:
        input("\nPress Enter to continue...")

def run_work_study_simulator(user_id):
    """
    Run work-study balance simulator
    
    Args:
        user_id: User ID
    """
    clear_screen()
    display_title("WORK-STUDY BALANCE SIMULATOR")
    display_info("Analyze how different work hours affect your income and academic performance.")
    
    # Get simulation parameters
    params = prompt_for_work_study_params()
    if params is None:
        return
    
    # Run simulation
    result = simulate_work_hours(params)
    
    # Save simulation
    try:
        simulation = Simulation(
            user_id=user_id,
            scenario_type="work_hours",
            parameters=params,
            result=result
        )
        simulation.save()
    except Exception as e:
        display_error(f"Failed to save simulation: {str(e)}")
    
    # Display results
    clear_screen()
    display_title("WORK-STUDY BALANCE RESULTS")
    display_simulation_result(result, "work_hours")
    
    # Ask if user wants to explore another work-study scenario
    another = prompt_for_confirmation("Would you like to analyze a different work-study scenario?", default='n')
    if another:
        run_work_study_simulator(user_id)
    else:
        input("\nPress Enter to continue...")

def run_student_loan_calculator(user_id):
    """
    Run student loan calculator
    
    Args:
        user_id: User ID
    """
    clear_screen()
    display_title("STUDENT LOAN CALCULATOR")
    display_info("Calculate student loan repayment options and financial impact.")
    
    # Get simulation parameters
    params = prompt_for_student_loan_params()
    if params is None:
        return
    
    # Run simulation
    result = simulate_student_loan(params)
    
    # Save simulation
    try:
        simulation = Simulation(
            user_id=user_id,
            scenario_type="student_loan",
            parameters=params,
            result=result
        )
        simulation.save()
    except Exception as e:
        display_error(f"Failed to save simulation: {str(e)}")
    
    # Display results
    clear_screen()
    display_title("STUDENT LOAN CALCULATION RESULTS")
    display_simulation_result(result, "student_loan")
    
    # Ask if user wants to explore another loan scenario
    another = prompt_for_confirmation("Would you like to analyze a different loan scenario?", default='n')
    if another:
        run_student_loan_calculator(user_id)
    else:
        input("\nPress Enter to continue...")

def view_saved_simulations(user_id):
    """
    View previously saved simulations
    
    Args:
        user_id: User ID
    """
    simulations = Simulation.get_by_user_id(user_id)
    
    clear_screen()
    display_title("SAVED SIMULATIONS")
    
    if not simulations:
        display_error("You don't have any saved simulations yet.")
        input("\nPress Enter to continue...")
        return
    
    # Create list of simulation descriptions
    sim_descriptions = []
    for sim in simulations:
        scenario_type = sim.scenario_type.replace("_", " ").title()
        date = sim.created_at if hasattr(sim, 'created_at') else "Unknown date"
        sim_descriptions.append(f"{scenario_type} - {date}")
    
    # Let user select a simulation to view
    selected_idx = prompt_for_selection("Select a simulation to view", sim_descriptions)
    if selected_idx is None:
        return
    
    selected_sim = simulations[sim_descriptions.index(selected_idx)]
    
    clear_screen()
    display_title(f"SIMULATION: {selected_sim.scenario_type.replace('_', ' ').title()}")
    display_simulation_result(selected_sim.result, selected_sim.scenario_type)
    
    input("\nPress Enter to continue...")

def simulate_housing(params):
    """
    Simulate and compare different housing options
    
    Args:
        params: Dictionary of housing comparison parameters
    
    Returns:
        dict: Simulation results
    """
    options = params.get("options", [])
    timeframe = params.get("timeframe", 9)  # Default to academic year
    
    results = []
    
    for option in options:
        name = option.get("name", "Option")
        monthly_rent = option.get("cost", 0)
        monthly_utilities = option.get("utilities", 0)
        monthly_commute = option.get("commute_cost", 0)
        
        # Calculate total monthly cost
        monthly_total = monthly_rent + monthly_utilities + monthly_commute
        
        # Calculate totals for the timeframe
        timeframe_rent = monthly_rent * timeframe
        timeframe_utilities = monthly_utilities * timeframe
        timeframe_commute = monthly_commute * timeframe
        timeframe_total = monthly_total * timeframe
        
        # Additional factors
        has_roommates = option.get("roommates", 0) > 0
        distance_to_campus = option.get("distance", 0)  # miles
        furnished = option.get("furnished", False)
        
        # Calculate time cost (commute time)
        monthly_commute_hours = option.get("commute_time", 0) * 30  # hours per month
        timeframe_commute_hours = monthly_commute_hours * timeframe
        
        # Quality of life factors (scale 1-100)
        privacy_rating = 100 if not has_roommates else max(100 - option.get("roommates", 0) * 15, 40)
        convenience_rating = max(100 - (distance_to_campus * 5), 20)
        overall_rating = (privacy_rating + convenience_rating) / 2
        
        results.append({
            "name": name,
            "monthly": {
                "rent": monthly_rent,
                "utilities": monthly_utilities,
                "commute": monthly_commute,
                "total": monthly_total
            },
            "timeframe": {
                "rent": timeframe_rent,
                "utilities": timeframe_utilities,
                "commute": timeframe_commute,
                "total": timeframe_total,
                "commute_hours": timeframe_commute_hours
            },
            "ratings": {
                "privacy": privacy_rating,
                "convenience": convenience_rating,
                "overall": overall_rating
            },
            "features": {
                "has_roommates": has_roommates,
                "distance_to_campus": distance_to_campus,
                "furnished": furnished
            }
        })
    
    # Sort by total cost
    results.sort(key=lambda x: x["timeframe"]["total"])
    
    # Determine the best value option
    # Simple metric: lowest cost per overall rating point
    for option in results:
        if option["ratings"]["overall"] > 0:
            option["value_score"] = option["timeframe"]["total"] / option["ratings"]["overall"]
        else:
            option["value_score"] = float('inf')
    
    best_value = min(results, key=lambda x: x["value_score"])
    
    return {
        "scenario": "housing",
        "options": results,
        "timeframe": timeframe,
        "recommendation": results[0]["name"],  # Cheapest option
        "best_value": best_value["name"],  # Best value option
        "savings_potential": results[-1]["timeframe"]["total"] - results[0]["timeframe"]["total"] if len(results) > 1 else 0
    }

def simulate_meal_plan(params):
    """
    Simulate and compare meal plan vs. grocery shopping
    
    Args:
        params: Dictionary of meal plan comparison parameters
    
    Returns:
        dict: Simulation results
    """
    meal_plan_cost = params.get("meal_plan_cost", 0)
    meals_per_week = params.get("meals_per_week", 0)
    grocery_budget = params.get("grocery_budget", 0)
    dining_out_budget = params.get("dining_out_budget", 0)
    weeks = params.get("weeks", 15)  # Default to semester
    
    # Calculate meal plan metrics
    if meals_per_week > 0:  
        cost_per_meal_plan_meal = meal_plan_cost / (meals_per_week * weeks)
    else:
        cost_per_meal_plan_meal = 0
        
    total_meal_plan_cost = meal_plan_cost
    
    # Calculate self-prepared meals metrics
    weekly_self_prepared_cost = grocery_budget + dining_out_budget
    total_self_prepared_cost = weekly_self_prepared_cost * weeks
    
    # Estimate number of meals per week when self-preparing
    estimated_meals_per_week = 21  # 3 meals a day
    
    if estimated_meals_per_week > 0:
        cost_per_self_prepared_meal = weekly_self_prepared_cost / estimated_meals_per_week
    else:
        cost_per_self_prepared_meal = 0
    
    # Calculate time costs (approximate)
    grocery_shopping_hours = 2 * weeks  # 2 hours per week
    cooking_hours = 7 * weeks  # 1 hour per day
    cleaning_hours = 3.5 * weeks  # 30 minutes per day
    total_self_prepared_hours = grocery_shopping_hours + cooking_hours + cleaning_hours
    
    # Meal plan time is minimal (just walking to dining hall)
    meal_plan_hours = 0.5 * meals_per_week * weeks  # 30 minutes per meal for walking/waiting
    
    # Determine which option is more cost-effective
    cost_difference = total_meal_plan_cost - total_self_prepared_cost
    is_meal_plan_cheaper = cost_difference < 0
    
    return {
        "scenario": "meal_plan",
        "options": [
            {
                "name": "Meal Plan",
                "total_cost": total_meal_plan_cost,
                "cost_per_meal": cost_per_meal_plan_meal,
                "time_investment_hours": meal_plan_hours,
                "features": {
                    "convenience": "High",
                    "variety": "Medium",
                    "nutritional_control": "Low"
                }
            },
            {
                "name": "Self-Prepared",
                "total_cost": total_self_prepared_cost,
                "cost_per_meal": cost_per_self_prepared_meal,
                "time_investment_hours": total_self_prepared_hours,
                "features": {
                    "convenience": "Low",
                    "variety": "High",
                    "nutritional_control": "High"
                }
            }
        ],
        "comparison": {
            "cost_difference": abs(cost_difference),
            "cheaper_option": "Meal Plan" if is_meal_plan_cheaper else "Self-Prepared",
            "time_difference": abs(total_self_prepared_hours - meal_plan_hours),
            "more_time_efficient": "Meal Plan" if meal_plan_hours < total_self_prepared_hours else "Self-Prepared"
        },
        "recommendation": "Meal Plan" if is_meal_plan_cheaper and meal_plan_hours < total_self_prepared_hours else "Self-Prepared",
        "recommendation_reason": "Based on both cost and time efficiency" if (is_meal_plan_cheaper and meal_plan_hours < total_self_prepared_hours) or (not is_meal_plan_cheaper and meal_plan_hours >= total_self_prepared_hours) else "Trade-off between cost and time"
    }

def simulate_work_hours(params):
    """
    Simulate the impact of working hours on studies and finances
    
    Args:
        params: Dictionary of work-study balance parameters
    
    Returns:
        dict: Simulation results
    """
    hourly_wage = params.get("hourly_wage", 15)
    possible_hours = params.get("possible_hours", [0, 10, 20, 30, 40])
    study_impact = params.get("study_impact", 0.03)  # GPA impact per 10 hours worked
    current_gpa = params.get("current_gpa", 3.5)
    weeks_per_semester = params.get("weeks", 15)
    
    results = []
    
    for hours in possible_hours:
        # Financial calculations
        weekly_income = hours * hourly_wage
        semester_income = weekly_income * weeks_per_semester
        annual_income = semester_income * 2  # Assuming two semesters
        
        # Academic impact (simplified model)
        # Assumes studying productivity decreases with more work hours
        gpa_impact = -(study_impact * (hours / 10))
        projected_gpa = max(0, min(4.0, current_gpa + gpa_impact))
        
        # Time breakdown (weekly)
        class_hours = 15  # Typical full-time credit load
        study_hours = 30  # Recommended 2 hours of study per class hour
        work_hours = hours
        sleep_hours = 56  # 8 hours daily
        personal_hours = 168 - class_hours - study_hours - work_hours - sleep_hours
        
        # Warning flags
        warnings = []
        if personal_hours < 20:
            warnings.append("Limited personal time may affect well-being")
        if study_hours * 0.8 < work_hours:  # If work exceeds 80% of study time
            warnings.append("Work hours may significantly impact academic performance")
        if sleep_hours / 7 < 7:  # Less than 7 hours of sleep per night
            warnings.append("Insufficient sleep may affect health and academic performance")
        
        results.append({
            "weekly_hours": hours,
            "financial": {
                "weekly_income": weekly_income,
                "semester_income": semester_income,
                "annual_income": annual_income
            },
            "academic": {
                "projected_gpa": projected_gpa,
                "gpa_change": gpa_impact
            },
            "time": {
                "class": class_hours,
                "study": study_hours,
                "work": work_hours,
                "sleep": sleep_hours,
                "personal": personal_hours
            },
            "warnings": warnings
        })
    
    # Find optimal balance (simple heuristic: maximize income while keeping projected GPA above 3.0)
    viable_options = [opt for opt in results if opt["academic"]["projected_gpa"] >= 3.0 and opt["time"]["personal"] >= 20]
    
    if viable_options:
        recommended = max(viable_options, key=lambda x: x["financial"]["semester_income"])
    else:
        # Fallback to option with highest GPA if no viable options
        recommended = max(results, key=lambda x: x["academic"]["projected_gpa"])
    
    return {
        "scenario": "work_hours",
        "options": results,
        "recommendation": recommended["weekly_hours"],
        "recommendation_reasoning": "Balances income potential while maintaining academic performance and well-being"
    }

def simulate_student_loan(params):
    """
    Simulate student loan repayment and total cost
    
    Args:
        params: Dictionary of student loan parameters
    
    Returns:
        dict: Simulation results
    """
    loan_amount = params.get("loan_amount", 20000)
    interest_rate = params.get("interest_rate", 5.0) / 100  # Convert to decimal
    loan_term = params.get("loan_term", 10)
    repayment_method = params.get("repayment_method", "standard")
    expected_salary = params.get("expected_salary", 50000)
    
    # Calculate standard repayment
    monthly_rate = interest_rate / 12
    total_payments = loan_term * 12
    
    # Standard monthly payment formula: P * r * (1+r)^n / ((1+r)^n - 1)
    if monthly_rate > 0:
        monthly_payment = loan_amount * monthly_rate * (1 + monthly_rate) ** total_payments / ((1 + monthly_rate) ** total_payments - 1)
    else:
        monthly_payment = loan_amount / total_payments
    
    total_repayment = monthly_payment * total_payments
    total_interest = total_repayment - loan_amount
    
    # Calculate income-based repayment (simplified)
    monthly_salary = expected_salary / 12
    ibr_payment = monthly_salary * 0.1  # Assume 10% of income
    
    if ibr_payment < monthly_payment:
        # If IBR payment is lower, loan will take longer to repay
        if ibr_payment > monthly_rate * loan_amount:  # Paying more than interest
            ibr_months = loan_amount / (ibr_payment - (monthly_rate * loan_amount))
            ibr_total = ibr_payment * ibr_months
        else:
            # If not covering interest, loan grows indefinitely (simplification)
            ibr_months = float('inf')
            ibr_total = float('inf')
    else:
        # If IBR payment is higher than standard, use standard timeline
        ibr_months = total_payments
        ibr_total = ibr_payment * total_payments
    
    # Calculate payment as percentage of expected income
    percent_of_income = (monthly_payment / monthly_salary) * 100
    
    # Calculate loan to income ratio
    loan_to_income_ratio = loan_amount / expected_salary
    
    # Risk assessment
    risk_level = "Low"
    if percent_of_income > 15:
        risk_level = "High"
    elif percent_of_income > 10:
        risk_level = "Medium"
    
    return {
        "scenario": "student_loan",
        "loan_details": {
            "principal": loan_amount,
            "interest_rate": interest_rate * 100,  # Convert back to percentage
            "term_years": loan_term
        },
        "standard_repayment": {
            "monthly_payment": monthly_payment,
            "total_payments": total_payments,
            "total_repaid": total_repayment,
            "total_interest": total_interest
        },
        "income_based_repayment": {
            "monthly_payment": ibr_payment,
            "estimated_months": ibr_months if ibr_months != float('inf') else "Will not fully repay",
            "total_repaid": ibr_total if ibr_total != float('inf') else "Will not fully repay"
        },
        "affordability": {
            "percent_of_expected_income": percent_of_income,
            "loan_to_income_ratio": loan_to_income_ratio,
            "risk_level": risk_level
        },
        "recommendation": repayment_method if repayment_method == "income_based" and ibr_payment < monthly_payment else "standard",
        "recommendation_reasoning": "Income-based repayment results in lower monthly payments but may increase total interest paid over time" if ibr_payment < monthly_payment else "Standard repayment minimizes total interest paid"
    }