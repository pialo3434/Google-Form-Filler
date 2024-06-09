from lib.config_loader import load_config
from lib.form_filler import FormFiller
from lib.logger_setup import setup_logger
import time

def main():
    while True:
        print("\n1. Start")
        print("2. Credits")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            pattern = input("Enter the pattern (A, B, C): ").upper()
            if pattern == 'A':
                times = int(input("How many times do you want to run pattern A? "))
                delay = int(input("Enter the delay in seconds between each run: "))
                for i in range(times):
                    print(f"Running pattern A: {i+1}/{times}")
                    config = load_config()
                    logger = setup_logger()
                    form_filler = FormFiller(config, logger)
                    form_filler.fill_form(pattern)
                    form_filler.driver.quit()  # Ensure the driver is quit after each run
                    if i < times - 1:  # No need to wait after the last form is filled
                        print(f"Waiting for {delay} seconds before the next run...")
                        time.sleep(delay)
                print("Completed all runs.")
            else:
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
