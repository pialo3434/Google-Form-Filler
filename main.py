from lib.config_loader import load_config
from lib.form_filler import FormFiller
from lib.logger_setup import setup_logger

def main():
    while True:
        print("\n1. Start")
        print("2. Credits")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            pattern = input("Enter the pattern (A, B, C): ").upper()
            config = load_config()
            logger = setup_logger()
            form_filler = FormFiller(config, logger)
            form_filler.fill_form(pattern)
        elif choice == '2':
            print("Credits: Paulo Costa")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
