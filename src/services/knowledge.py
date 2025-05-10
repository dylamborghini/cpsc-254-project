"""
Financial knowledge service for the Financial Literacy Coach
"""
import re
from src.config import load_knowledge_base
from src.ui.display import (
    clear_screen,
    display_title,
    display_financial_term,
    display_error,
    display_info
)
from src.ui.prompts import (
    prompt_for_text,
    prompt_for_selection,
    prompt_for_confirmation
)

def knowledge_menu():
    """
    Display the financial knowledge menu
    """
    # This is a placeholder that will be replaced by the CLI's menu handling
    pass

def ask_financial_question():
    """
    Answer a financial question using the knowledge base
    """
    knowledge_base = load_knowledge_base()
    
    if not knowledge_base:
        clear_screen()
        display_error("Financial knowledge base is not available.")
        input("\nPress Enter to continue...")
        return
    
    clear_screen()
    display_title("ASK A FINANCIAL QUESTION")
    display_info("Ask any question about financial concepts, and I'll try to provide an answer relevant to student finances.")
    
    while True:
        question = prompt_for_text("Your question (or 'back' to return)", min_length=5)
        if question is None:
            return
        
        # Process the question
        answer = process_question(question, knowledge_base)
        
        clear_screen()
        display_title("ANSWER")
        print(f"Q: {question}\n")
        print(f"A: {answer}\n")
        
        # Ask if user wants to ask another question
        another = prompt_for_confirmation("Would you like to ask another question?", default='y')
        if another is None or not another:
            break
        
        clear_screen()
        display_title("ASK A FINANCIAL QUESTION")

def browse_financial_terms():
    """
    Browse and search financial terms in the knowledge base
    """
    knowledge_base = load_knowledge_base()
    
    if not knowledge_base:
        clear_screen()
        display_error("Financial knowledge base is not available.")
        input("\nPress Enter to continue...")
        return
    
    clear_screen()
    display_title("FINANCIAL TERMS GLOSSARY")
    
    # Get all terms
    terms = list(knowledge_base.keys())
    terms.sort()  # Alphabetical order
    
    while True:
        # Display options for browsing
        options = [
            "View all terms alphabetically",
            "Search for a specific term",
            "View terms by category"
        ]
        
        choice = prompt_for_selection("How would you like to browse?", options)
        if choice is None:
            return
        
        if choice == "View all terms alphabetically":
            view_all_terms(knowledge_base, terms)
        elif choice == "Search for a specific term":
            search_term(knowledge_base)
        elif choice == "View terms by category":
            view_terms_by_category(knowledge_base, terms)

def view_all_terms(knowledge_base, terms):
    """
    View all financial terms alphabetically
    
    Args:
        knowledge_base: Dictionary of financial terms and definitions
        terms: List of terms in the knowledge base
    """
    clear_screen()
    display_title("ALL FINANCIAL TERMS")
    
    # Display terms in columns
    term_list = []
    for i, term in enumerate(terms, 1):
        term_list.append(f"{i}. {term}")
    
    # Print terms in columns (3 columns)
    column_width = max(len(item) for item in term_list) + 2
    num_terms = len(term_list)
    num_rows = (num_terms + 2) // 3  # Ceiling division for number of rows
    
    for row in range(num_rows):
        row_items = []
        for col in range(3):
            idx = row + col * num_rows
            if idx < num_terms:
                row_items.append(term_list[idx].ljust(column_width))
            else:
                row_items.append("".ljust(column_width))
        print("".join(row_items))
    
    # Let user select a term to view
    print("\nEnter the number of the term you'd like to view, or 'back' to return")
    choice = prompt_for_text("Your choice")
    
    if choice is None:
        return
    
    try:
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(terms):
            term = terms[choice_idx]
            view_term(knowledge_base, term)
        else:
            display_error("Invalid selection. Please try again.")
            input("\nPress Enter to continue...")
    except ValueError:
        display_error("Please enter a valid number or 'back'.")
        input("\nPress Enter to continue...")

def search_term(knowledge_base):
    """
    Search for a specific financial term
    
    Args:
        knowledge_base: Dictionary of financial terms and definitions
    """
    clear_screen()
    display_title("SEARCH FINANCIAL TERMS")
    
    search_query = prompt_for_text("Enter search term")
    if search_query is None:
        return
    
    # Search for matching terms
    matching_terms = []
    for term in knowledge_base:
        # Check main term
        if search_query.lower() in term.lower():
            matching_terms.append(term)
            continue
        
        # Check aliases
        aliases = knowledge_base[term].get("aliases", [])
        for alias in aliases:
            if search_query.lower() in alias.lower():
                matching_terms.append(term)
                break
    
    # Sort matching terms alphabetically
    matching_terms.sort()
    
    if not matching_terms:
        display_error(f"No terms found matching '{search_query}'.")
        input("\nPress Enter to continue...")
        return
    
    clear_screen()
    display_title(f"SEARCH RESULTS FOR '{search_query}'")
    
    # Display matching terms
    selected_term = prompt_for_selection("Select a term to view", matching_terms)
    if selected_term is None:
        return
    
    view_term(knowledge_base, selected_term)

def view_terms_by_category(knowledge_base, terms):
    """
    View financial terms grouped by category
    
    Args:
        knowledge_base: Dictionary of financial terms and definitions
        terms: List of terms in the knowledge base
    """
    # This is a simplified implementation - in a full application,
    # we would have proper term categories in the knowledge base
    
    # Create some basic categories based on term content
    categories = {
        "Budgeting & Savings": ["Budget", "Emergency Fund", "Savings"],
        "Credit & Loans": ["Credit Card", "Credit Score", "Student Loan", "Interest Rate"],
        "Income": ["Work-Study", "Financial Aid", "FAFSA", "Scholarship"],
        "Housing & Living": ["Rent", "Housing", "Meal Plan"],
        "Financial Concepts": ["Compound Interest"]
    }
    
    clear_screen()
    display_title("FINANCIAL TERMS BY CATEGORY")
    
    # Let user select a category
    selected_category = prompt_for_selection("Select a category", list(categories.keys()))
    if selected_category is None:
        return
    
    # Display terms in selected category
    category_terms = categories.get(selected_category, [])
    if not category_terms:
        display_error(f"No terms found in category '{selected_category}'.")
        input("\nPress Enter to continue...")
        return
    
    clear_screen()
    display_title(f"TERMS IN '{selected_category}'")
    
    selected_term = prompt_for_selection("Select a term to view", category_terms)
    if selected_term is None:
        return
    
    view_term(knowledge_base, selected_term)

def view_term(knowledge_base, term):
    """
    View detailed information about a financial term
    
    Args:
        knowledge_base: Dictionary of financial terms and definitions
        term: The term to view
    """
    if term not in knowledge_base:
        display_error(f"Term '{term}' not found in knowledge base.")
        input("\nPress Enter to continue...")
        return
    
    clear_screen()
    term_info = knowledge_base[term]
    display_financial_term(term, term_info)
    
    # Let the user view related terms if any are shown in the definition
    related_terms = find_related_terms(term_info, knowledge_base.keys())
    
    if related_terms:
        print("\nRelated terms found:")
        selected_related = prompt_for_selection("View related term", related_terms)
        
        if selected_related is not None:
            view_term(knowledge_base, selected_related)
    else:
        input("\nPress Enter to continue...")

def find_related_terms(term_info, all_terms):
    """
    Find related terms mentioned in the term's information
    
    Args:
        term_info: Dictionary with term information
        all_terms: List of all terms in knowledge base
    
    Returns:
        list: Related terms
    """
    related = set()
    
    # Combine all text fields to search for mentions of other terms
    all_text = ""
    for field in ["definition", "student_context", "how_to", "student_advice"]:
        if field in term_info:
            all_text += term_info[field] + " "
    
    # Check if other terms are mentioned
    for other_term in all_terms:
        # Avoid finding substrings that aren't actually term mentions
        pattern = r'\b' + re.escape(other_term) + r'\b'
        if re.search(pattern, all_text, re.IGNORECASE):
            related.add(other_term)
    
    # Remove self-references
    if term_info.get("term") in related:
        related.remove(term_info.get("term"))
    
    return list(related)

def process_question(question, knowledge_base):
    """
    Process a financial question and provide an answer
    
    Args:
        question: User's question
        knowledge_base: Dictionary of financial terms and definitions
    
    Returns:
        str: Answer to the question
    """
    # Convert question to lowercase for matching
    question_lower = question.lower()
    
    # Define common question patterns
    definition_patterns = [
        r'what is (?:a |an |the )?([a-z\s]+)\??',
        r'define (?:a |an |the )?([a-z\s]+)',
        r'explain (?:a |an |the )?([a-z\s]+)',
        r'tell me about (?:a |an |the )?([a-z\s]+)'
    ]
    
    comparison_patterns = [
        r'(?:what is|what\'s) the difference between ([a-z\s]+) and ([a-z\s]+)',
        r'compare ([a-z\s]+) (?:to|and|with) ([a-z\s]+)',
        r'([a-z\s]+) vs\.? ([a-z\s]+)'
    ]
    
    how_to_patterns = [
        r'how do I ([a-z\s]+)',
        r'how to ([a-z\s]+)',
        r'how can I ([a-z\s]+)',
        r'ways to ([a-z\s]+)'
    ]
    
    recommendation_patterns = [
        r'should I ([a-z\s]+)',
        r'is it (?:good|better|best|wise|advisable) to ([a-z\s]+)',
        r'what\'s the best way to ([a-z\s]+)'
    ]
    
    calculation_patterns = [
        r'how (?:much|many) ([a-z\s]+)',
        r'calculate ([a-z\s]+)',
        r'what percentage ([a-z\s]+)'
    ]
    
    # Try to match definition patterns
    for pattern in definition_patterns:
        match = re.search(pattern, question_lower)
        if match:
            term = match.group(1).strip()
            return answer_definition_question(term, knowledge_base)
    
    # Try to match comparison patterns
    for pattern in comparison_patterns:
        match = re.search(pattern, question_lower)
        if match:
            term1 = match.group(1).strip()
            term2 = match.group(2).strip()
            return answer_comparison_question(term1, term2, knowledge_base)
    
    # Try to match how-to patterns
    for pattern in how_to_patterns:
        match = re.search(pattern, question_lower)
        if match:
            action = match.group(1).strip()
            return answer_how_to_question(action, knowledge_base)
    
    # Try to match recommendation patterns
    for pattern in recommendation_patterns:
        match = re.search(pattern, question_lower)
        if match:
            action = match.group(1).strip()
            return answer_recommendation_question(action, knowledge_base)
    
    # Try to match calculation patterns
    for pattern in calculation_patterns:
        match = re.search(pattern, question_lower)
        if match:
            calculation = match.group(1).strip()
            return answer_calculation_question(calculation, knowledge_base)
    
    # If no patterns match, do a general search for relevant terms
    return answer_general_question(question, knowledge_base)

def answer_definition_question(term, knowledge_base):
    """
    Answer a definition question
    
    Args:
        term: Term to define
        knowledge_base: Knowledge base dictionary
    
    Returns:
        str: Answer
    """
    # Look for exact match
    if term in knowledge_base:
        info = knowledge_base[term]
        answer = info["definition"]
        
        # Add student context if available
        if "student_context" in info:
            answer += f"\n\n{info['student_context']}"
        
        return answer
    
    # Look for partial matches
    matches = []
    for kb_term in knowledge_base:
        if term in kb_term.lower():
            matches.append(kb_term)
        else:
            # Check aliases
            aliases = knowledge_base[kb_term].get("aliases", [])
            for alias in aliases:
                if term in alias.lower():
                    matches.append(kb_term)
                    break
    
    if matches:
        if len(matches) == 1:
            # One match found
            info = knowledge_base[matches[0]]
            answer = f"I found information about {matches[0]}:\n\n"
            answer += info["definition"]
            
            # Add student context if available
            if "student_context" in info:
                answer += f"\n\n{info['student_context']}"
            
            return answer
        else:
            # Multiple matches found
            answer = f"I found multiple terms related to '{term}':\n"
            for match in matches:
                answer += f"- {match}\n"
            answer += "\nPlease ask about a specific term for more information."
            return answer
    
    # No matches found
    return f"I don't have specific information about '{term}'. Please try another financial term or check the term glossary."

def answer_comparison_question(term1, term2, knowledge_base):
    """
    Answer a comparison question between two terms
    
    Args:
        term1: First term
        term2: Second term
        knowledge_base: Knowledge base dictionary
    
    Returns:
        str: Answer
    """
    # Find best matches for each term
    term1_match = find_best_match(term1, knowledge_base)
    term2_match = find_best_match(term2, knowledge_base)
    
    if not term1_match or not term2_match:
        missing = term1 if not term1_match else term2
        return f"I don't have information about '{missing}' to make a comparison."
    
    # Get information for both terms
    info1 = knowledge_base[term1_match]
    info2 = knowledge_base[term2_match]
    
    # Check if there's a direct comparison available
    if "comparison" in info1 and term2_match in info1["comparison"]:
        return f"{term1_match} vs. {term2_match}:\n\n{info1['comparison'][term2_match]}"
    elif "comparison" in info2 and term1_match in info2["comparison"]:
        return f"{term1_match} vs. {term2_match}:\n\n{info2['comparison'][term1_match]}"
    
    # Generate a comparison from definitions
    answer = f"Comparing {term1_match} and {term2_match}:\n\n"
    answer += f"{term1_match}: {info1['definition']}\n\n"
    answer += f"{term2_match}: {info2['definition']}\n\n"
    
    # Add a generic comparison statement
    answer += "Key differences: These financial concepts serve different purposes in personal finance and should be understood in their specific contexts."
    
    return answer

def answer_how_to_question(action, knowledge_base):
    """
    Answer a how-to question
    
    Args:
        action: Action the user wants to know how to do
        knowledge_base: Knowledge base dictionary
    
    Returns:
        str: Answer
    """
    # Look for terms related to the action
    related_terms = []
    for term, info in knowledge_base.items():
        if action in term.lower() or any(action in alias.lower() for alias in info.get("aliases", [])):
            related_terms.append((term, info))
    
    if not related_terms:
        return f"I don't have specific information about how to {action}. Please try asking about a specific financial term."
    
    # Find the term with how-to information
    for term, info in related_terms:
        if "how_to" in info:
            answer = f"How to {action} ({term}):\n\n{info['how_to']}"
            
            # Add student advice if available
            if "student_advice" in info:
                answer += f"\n\nAdvice for students:\n{info['student_advice']}"
            
            return answer
    
    # No how-to information found
    term, info = related_terms[0]  # Use the first related term
    answer = f"Information about {term}:\n\n{info['definition']}"
    
    # Add student context if available
    if "student_context" in info:
        answer += f"\n\n{info['student_context']}"
    
    return answer

def answer_recommendation_question(action, knowledge_base):
    """
    Answer a recommendation question
    
    Args:
        action: Action the user is asking for recommendations about
        knowledge_base: Knowledge base dictionary
    
    Returns:
        str: Answer
    """
    # Similar to how-to, but focus on student advice
    related_terms = []
    for term, info in knowledge_base.items():
        if action in term.lower() or any(action in alias.lower() for alias in info.get("aliases", [])):
            related_terms.append((term, info))
    
    if not related_terms:
        return f"I don't have specific recommendations about {action}. Please try asking about a specific financial term."
    
    # Find the term with student advice
    for term, info in related_terms:
        if "student_advice" in info:
            return f"Regarding {action} ({term}):\n\n{info['student_advice']}"
    
    # No specific advice found
    term, info = related_terms[0]  # Use the first related term
    return f"Information about {term} that may help:\n\n{info.get('student_context', info['definition'])}"

def answer_calculation_question(calculation, knowledge_base):
    """
    Answer a calculation question
    
    Args:
        calculation: What the user wants to calculate
        knowledge_base: Knowledge base dictionary
    
    Returns:
        str: Answer
    """
    # Look for terms related to the calculation
    related_terms = []
    for term, info in knowledge_base.items():
        if calculation in term.lower() or any(calculation in alias.lower() for alias in info.get("aliases", [])):
            related_terms.append((term, info))
    
    if not related_terms:
        return f"I don't have specific calculation information about {calculation}. Please try asking about a specific financial term."
    
    # Find the term with formula information
    for term, info in related_terms:
        if "formula" in info:
            answer = f"For calculating {term}:\n\n{info['formula']}"
            
            # Add example if available
            if "calculation_example" in info:
                answer += f"\n\n{info['calculation_example']}"
            
            return answer
    
    # No formula information found
    term, info = related_terms[0]  # Use the first related term
    return f"Information about {term} that may help:\n\n{info['definition']}"

def answer_general_question(question, knowledge_base):
    """
    Answer a general question by finding relevant terms
    
    Args:
        question: User's question
        knowledge_base: Knowledge base dictionary
    
    Returns:
        str: Answer
    """
    # Extract keywords from the question
    words = re.findall(r'\b[a-z]{3,}\b', question.lower())
    
    # Count relevance of each term
    term_relevance = {}
    for term, info in knowledge_base.items():
        relevance = 0
        
        # Check term name
        for word in words:
            if word in term.lower():
                relevance += 3
        
        # Check aliases
        for alias in info.get("aliases", []):
            for word in words:
                if word in alias.lower():
                    relevance += 2
        
        # Check definition
        definition = info["definition"].lower()
        for word in words:
            if word in definition:
                relevance += 1
        
        if relevance > 0:
            term_relevance[term] = relevance
    
    # Sort by relevance
    relevant_terms = sorted(term_relevance.keys(), key=lambda x: term_relevance[x], reverse=True)
    
    if not relevant_terms:
        return "I don't have enough information to answer that question. Please try asking about specific financial terms or concepts."
    
    # Use the most relevant term
    best_term = relevant_terms[0]
    info = knowledge_base[best_term]
    
    answer = f"Based on your question, you might be interested in information about {best_term}:\n\n"
    answer += info["definition"]
    
    # Add student context if available
    if "student_context" in info:
        answer += f"\n\n{info['student_context']}"
    
    # Mention other relevant terms
    if len(relevant_terms) > 1:
        answer += f"\n\nYou might also be interested in: {', '.join(relevant_terms[1:3])}"
    
    return answer

def find_best_match(term, knowledge_base):
    """
    Find the best matching term in the knowledge base
    
    Args:
        term: Search term
        knowledge_base: Knowledge base dictionary
    
    Returns:
        str: Best matching term or None if no match
    """
    # Check for exact match
    if term in knowledge_base:
        return term
    
    # Check for case-insensitive match
    for kb_term in knowledge_base:
        if term.lower() == kb_term.lower():
            return kb_term
    
    # Check for term in aliases
    for kb_term, info in knowledge_base.items():
        aliases = info.get("aliases", [])
        for alias in aliases:
            if term.lower() == alias.lower():
                return kb_term
    
    # Check if term is contained in a knowledge base term
    for kb_term in knowledge_base:
        if term.lower() in kb_term.lower():
            return kb_term
    
    # Check if term is contained in aliases
    for kb_term, info in knowledge_base.items():
        aliases = info.get("aliases", [])
        for alias in aliases:
            if term.lower() in alias.lower():
                return kb_term
    
    # No match found
    return None