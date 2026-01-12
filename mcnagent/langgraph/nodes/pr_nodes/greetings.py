"""
Greeting message pools for each workflow stage.
Each stage has a pool of ~10 greeting messages to randomly select from.

Usage:
    from .greetings import get_greeting
    
    greeting = get_greeting("greet")  # Returns random greeting for greet stage
"""

import random
from typing import Dict, List


# ============================================================================
# GREETING POOLS BY STAGE
# ============================================================================

GREET_GREETINGS: List[str] = [
    "Greeting placeholder 1",
    "Greeting placeholder 2",
    "Greeting placeholder 3",
    "Greeting placeholder 4",
    "Greeting placeholder 5",
    "Greeting placeholder 6",
    "Greeting placeholder 7",
    "Greeting placeholder 8",
    "Greeting placeholder 9",
    "Greeting placeholder 10",
]

TYPE_GREETINGS: List[str] = [
    "Greeting placeholder 1",
    "Greeting placeholder 2",
    "Greeting placeholder 3",
    "Greeting placeholder 4",
    "Greeting placeholder 5",
    "Greeting placeholder 6",
    "Greeting placeholder 7",
    "Greeting placeholder 8",
    "Greeting placeholder 9",
    "Greeting placeholder 10",
]

BRIEF_GREETINGS: List[str] = [
    "Greeting placeholder 1",
    "Greeting placeholder 2",
    "Greeting placeholder 3",
    "Greeting placeholder 4",
    "Greeting placeholder 5",
    "Greeting placeholder 6",
    "Greeting placeholder 7",
    "Greeting placeholder 8",
    "Greeting placeholder 9",
    "Greeting placeholder 10",
]

SCHEDULE_GREETINGS: List[str] = [
    "Greeting placeholder 1",
    "Greeting placeholder 2",
    "Greeting placeholder 3",
    "Greeting placeholder 4",
    "Greeting placeholder 5",
    "Greeting placeholder 6",
    "Greeting placeholder 7",
    "Greeting placeholder 8",
    "Greeting placeholder 9",
    "Greeting placeholder 10",
]

PRODUCT_GREETINGS: List[str] = [
    "Greeting placeholder 1",
    "Greeting placeholder 2",
    "Greeting placeholder 3",
    "Greeting placeholder 4",
    "Greeting placeholder 5",
    "Greeting placeholder 6",
    "Greeting placeholder 7",
    "Greeting placeholder 8",
    "Greeting placeholder 9",
    "Greeting placeholder 10",
]

ADDRESS_GREETINGS: List[str] = [
    "Greeting placeholder 1",
    "Greeting placeholder 2",
    "Greeting placeholder 3",
    "Greeting placeholder 4",
    "Greeting placeholder 5",
    "Greeting placeholder 6",
    "Greeting placeholder 7",
    "Greeting placeholder 8",
    "Greeting placeholder 9",
    "Greeting placeholder 10",
]

REMINDER_GREETINGS: List[str] = [
    "Greeting placeholder 1",
    "Greeting placeholder 2",
    "Greeting placeholder 3",
    "Greeting placeholder 4",
    "Greeting placeholder 5",
    "Greeting placeholder 6",
    "Greeting placeholder 7",
    "Greeting placeholder 8",
    "Greeting placeholder 9",
    "Greeting placeholder 10",
]

SCRIPT_REMINDER_GREETINGS: List[str] = [
    "Greeting placeholder 1",
    "Greeting placeholder 2",
    "Greeting placeholder 3",
    "Greeting placeholder 4",
    "Greeting placeholder 5",
    "Greeting placeholder 6",
    "Greeting placeholder 7",
    "Greeting placeholder 8",
    "Greeting placeholder 9",
    "Greeting placeholder 10",
]

FINAL_GREETINGS: List[str] = [
    "Greeting placeholder 1",
    "Greeting placeholder 2",
    "Greeting placeholder 3",
    "Greeting placeholder 4",
    "Greeting placeholder 5",
    "Greeting placeholder 6",
    "Greeting placeholder 7",
    "Greeting placeholder 8",
    "Greeting placeholder 9",
    "Greeting placeholder 10",
]


# ============================================================================
# GREETINGS MAP & HELPER
# ============================================================================

GREETINGS_MAP: Dict[str, List[str]] = {
    "greet": GREET_GREETINGS,
    "type": TYPE_GREETINGS,
    "brief": BRIEF_GREETINGS,
    "schedule": SCHEDULE_GREETINGS,
    "product": PRODUCT_GREETINGS,
    "address": ADDRESS_GREETINGS,
    "reminder": REMINDER_GREETINGS,
    "script_reminder": SCRIPT_REMINDER_GREETINGS,
    "final": FINAL_GREETINGS,
}


def get_greeting(stage: str) -> str:
    """
    Get a random greeting for the specified stage.
    
    Args:
        stage: The workflow stage name (e.g., "greet", "schedule", "final")
        
    Returns:
        A randomly selected greeting string for that stage.
        Returns empty string if stage not found.
    """
    greetings = GREETINGS_MAP.get(stage, [])
    if not greetings:
        return ""
    return random.choice(greetings)
