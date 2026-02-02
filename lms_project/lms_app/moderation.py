import re

BAD_WORDS = [
    'fuck', 'shit', 'ass', 'bitch', 'damn', 'crap', 'bastard', 'dick', 'cock',
    'pussy', 'whore', 'slut', 'nigger', 'fag', 'retard', 'idiot', 'stupid',
    'hate', 'kill', 'die', 'murder', 'rape', 'porn', 'xxx', 'nude', 'naked',
    'spam', 'scam', 'fraud', 'fake', 'click here', 'free money', 'bitcoin',
    'crypto', 'invest now', 'make money fast', 'get rich', 'lottery', 'winner',
]

def contains_bad_words(text):
    if not text:
        return False
    text_lower = text.lower()
    for word in BAD_WORDS:
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, text_lower):
            return True
    return False

def is_rubbish_content(text):
    if not text:
        return True
    text = text.strip()
    if len(text) < 3:
        return True
    if len(set(text.lower())) < 3:
        return True
    letter_count = sum(1 for c in text if c.isalpha())
    if letter_count < len(text) * 0.3:
        return True
    if len(text) > 10:
        words = text.split()
        if len(words) == 1 and not any(c.isspace() for c in text):
            if len(text) > 50:
                return True
    return False

def validate_content(text):
    if is_rubbish_content(text):
        return False, "Your post appears to be empty or contains only random characters. Please write something meaningful."
    if contains_bad_words(text):
        return False, "Your post contains inappropriate language. Please keep the content respectful and professional."
    return True, None
