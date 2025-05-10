# Financial Literacy Coach

A command-line application designed to help university students develop practical financial literacy skills through personalized budgeting tools, an interactive knowledge base, goal-setting features, and financial decision simulators.

## Features

### 1. Personalized Budgeting Module
- Income and expense tracking with student-specific categories
- Spending pattern analysis
- Personalized saving recommendations

### 2. Financial Knowledge Assistant
- Natural language Q&A for financial concepts
- Student-focused explanations
- Curated glossary of financial terms

### 3. Goal Planning Tool
- Short and medium-term financial goal setting
- Progress tracking and visualization
- Strategy recommendations

### 4. Financial Decision Simulator
- Housing cost comparison calculator
- Meal plan vs. grocery shopping analyzer
- Work-study balance simulator
- Student loan repayment calculator

## Installation

### Prerequisites
- Python 3.8 or higher

### Steps
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/financial-literacy-coach.git
   cd financial-literacy-coach
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package:
   ```
   pip install -e .
   ```

## Usage

### Start the application
```
financial-coach
```
or
```
python -m src.main
```

### Application Flow
1. Log in with your username (or create a new account)
2. Navigate the main menu:
   - Budget Manager
   - Financial Knowledge Assistant
   - Goal Tracker
   - Financial Simulator

## Technical Details

### Architecture
- Command-line interface using Python's built-in libraries
- SQLite database for data persistence
- Modular design with separate components for database, services, and UI

### Directory Structure
```
financial-literacy-coach/
├── src/
│   ├── main.py               # Main application entry point
│   ├── config.py             # Configuration settings
│   ├── db/
│   │   ├── models.py         # Database models
│   │   └── database.py       # Database connection and operations
│   ├── services/
│   │   ├── budget.py         # Budget analysis 
│   │   ├── knowledge.py      # Question answering
│   │   ├── goals.py          # Goal tracking
│   │   └── simulator.py      # Financial simulation
│   ├── ui/
│   │   ├── cli.py            # CLI command definitions
│   │   ├── prompts.py        # User input prompts
│   │   └── display.py        # Formatting and display functions
│   └── resources/
│       └── financial_terms.json  # Knowledge base
├── data/
│   └── app.db                # SQLite database file
├── setup.py                  # Package setup
└── README.md                 # Project documentation
```

## Project Implementation

### AI Components
1. **Intent Classification**: Categorize financial questions to appropriate knowledge areas
2. **Pattern Recognition**: Identify spending patterns and suggest optimizations
3. **Recommendation Engine**: Provide personalized financial advice based on user profile
4. **Simple Predictive Modeling**: Project savings based on current habits

### Data Management
- User profiles and preferences
- Budget history and analysis
- Financial goals and progress
- Simulation results

## Development

### Running Tests
```
python -m unittest discover tests
```
