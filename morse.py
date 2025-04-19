from constants import TEXT_TO_MORSE, MORSE_TO_TEXT

def text_to_morse(text):
    """Convert text to Morse code with error handling"""
    morse_code = []
    unsupported_chars = []
    
    for char in text.upper():
        if char in TEXT_TO_MORSE:
            morse_code.append(TEXT_TO_MORSE[char])
        elif char == ' ':
            morse_code.append('/')
        else:
            unsupported_chars.append(char)
    
    warning_msg = f" [Unsupported: {', '.join(set(unsupported_chars))}]" if unsupported_chars else ""
    return ' '.join(morse_code) + warning_msg

def morse_to_text(morse):
    """Convert Morse to text with error handling"""
    text = []
    invalid_sequences = []
    
    for word in morse.strip().split('/'):
        translated_word = []
        for char in word.split():
            if char in MORSE_TO_TEXT:
                translated_word.append(MORSE_TO_TEXT[char])
            else:
                invalid_sequences.append(char)
                translated_word.append('?')
        if translated_word:
            text.append(''.join(translated_word))
    
    warning_msg = f" [Invalid Morse: {', '.join(set(invalid_sequences))}]" if invalid_sequences else ""
    return ' '.join(text) + warning_msg