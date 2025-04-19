from morse import text_to_morse, morse_to_text

def get_user_choice():
    """Get and validate user mode choice"""
    while True:
        print("\nMorse Code Translator")
        print("1. Text → Morse")
        print("2. Morse → Text")
        print("3. Exit")
        choice = input("Choose (1/2/3): ").strip()
        if choice in ('1', '2', '3'):
            return choice
        print("Invalid choice. Please try again.")

def main():
    while True:
        choice = get_user_choice()
        
        if choice == '1':
            text = input("Enter text to translate:\n> ")
            print("Morse Code:\n" + text_to_morse(text))
        elif choice == '2':
            morse = input("Enter Morse code (separate letters with spaces, words with '/'):\n> ")
            print("Translated Text:\n" + morse_to_text(morse))
        else:
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()