#!/usr/bin/env python3
"""
Financial Literacy Coach
A CLI application to help university students develop financial literacy skills
"""
import os
import sys
import time
from src.db.database import init_db
from src.ui.cli import run_cli
from src.ui.display import display_welcome, clear_screen

def main():
    """
    Main application entry point
    """
    try:
        # Initialize database
        init_db()
        
        # Display welcome message
        clear_screen()
        display_welcome()
        time.sleep(1)
        
        # Start the CLI interface
        run_cli()
    
    except KeyboardInterrupt:
        clear_screen()
        print("\nThank you for using the Financial Literacy Coach!")
        print("Exiting the application...")
        sys.exit(0)
    
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        print("Please try restarting the application.")
        sys.exit(1)

if __name__ == "__main__":
    main()