"""
Configuration for AI Research Assistant
Loads environment variables and provides settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===========================================
# API KEYS
# ===========================================
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ===========================================
# MODEL SETTINGS
# ===========================================
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # Best for agents
# Alternative: "claude-3-5-haiku-20241022" (faster, cheaper)

# ===========================================
# AGENT SETTINGS
# ===========================================
MAX_ITERATIONS = 12  # Maximum agent loop iterations
MAX_SEARCH_RESULTS = 5  # Results per search query

# ===========================================
# VALIDATION
# ===========================================
def validate_config():
    """Validate that all required environment variables are set"""
    errors = []

    if not ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY is not set")

    if not TAVILY_API_KEY:
        errors.append("TAVILY_API_KEY is not set")

    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")

    return True


if __name__ == "__main__":
    # Test configuration
    try:
        validate_config()
        print("Configuration is valid!")
        print(f"Model: {CLAUDE_MODEL}")
    except ValueError as e:
        print(f"Error: {e}")
