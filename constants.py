# Morse Code Mappings
# Letters A-Z
TEXT_TO_MORSE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    
    # Numbers 0-9
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
    
    # Space character (word separator)
    ' ': '/'
}

# Reverse mapping (Morse to Text)
MORSE_TO_TEXT = {value: key for key, value in TEXT_TO_MORSE.items()}

# # TEST CODE (remove after verification)
# if __name__ == "__main__":
#     print("Testing TEXT_TO_MORSE:")
#     print(f"A -> {TEXT_TO_MORSE['A']}")  # Should print: A -> .-
#     print(f"5 -> {TEXT_TO_MORSE['5']}")  # Should print: 5 -> .....
#     print(f"Space -> '{TEXT_TO_MORSE[' ']}'")  # Should print: Space -> '/'
    
#     print("\nTesting MORSE_TO_TEXT:")
#     print(f".- -> {MORSE_TO_TEXT['.-']}")  # Should print: .- -> A
#     print(f"..... -> {MORSE_TO_TEXT['.....']}")  # Should print: ..... -> 5
#     print(f"/ -> '{MORSE_TO_TEXT['/']}'")  # Should print: / -> ' '