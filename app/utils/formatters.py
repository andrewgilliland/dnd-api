"""String formatting and text utilities"""


def format_modifier(value: int) -> str:
    """
    Format a numeric modifier with +/- sign.
    
    Args:
        value: Modifier value
    
    Returns:
        Formatted string (e.g., "+3", "-2", "+0")
    
    Example:
        format_modifier(3)   # Returns "+3"
        format_modifier(-2)  # Returns "-2"
    """
    if value >= 0:
        return f"+{value}"
    return str(value)


def pluralize(count: int, singular: str, plural: str | None = None) -> str:
    """
    Return singular or plural form based on count.
    
    Args:
        count: Number of items
        singular: Singular form
        plural: Plural form (defaults to singular + 's')
    
    Returns:
        Appropriate form based on count
    
    Example:
        pluralize(1, "monster")   # Returns "1 monster"
        pluralize(5, "wolf", "wolves")  # Returns "5 wolves"
    """
    if plural is None:
        plural = f"{singular}s"
    
    word = singular if count == 1 else plural
    return f"{count} {word}"


def titlecase(text: str) -> str:
    """
    Convert text to title case, preserving certain words.
    
    Args:
        text: Text to convert
    
    Returns:
        Title-cased text
    """
    # Words to keep lowercase (unless first word)
    lowercase_words = {'a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 'of', 'at', 'by', 'to'}
    
    words = text.split()
    result = []
    
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in lowercase_words:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    
    return ' '.join(result)
