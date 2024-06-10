from lib.config_loader import load_config
from lib.form_filler import FormFiller
from lib.logger_setup import setup_logger
import time

def main():
    valid_parties = ['PS', 'BLOCO', 'PAN', 'PCP-PEV']
    valid_nationalities = ['Portuguesa', 'Brasileira', 'Americana', 'Ucraniana', 'Russa', 'Angolana', 'Moçambicana', 'Cabo Verdiana', 'Outro']
    while True:
        print("\n1. Start")
        print("2. Credits")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            pattern = input("Enter the pattern (A, B, C): ").upper()
            if pattern in ['A', 'B', 'C']:
                times = int(input(f"How many times do you want to run pattern {pattern}? "))
                delay = int(input("Enter the delay in seconds between each run: "))
                nationality = None
                if pattern in ['B', 'C']:
                    nationality_input = input("Enter your nationality from the list: Portuguesa, Brasileira, Americana, Ucraniana, Russa, Angolana, Moçambicana, Cabo Verdiana, Outro: ")
                    # Convert both user input and list items to uppercase for comparison
                    while nationality_input.upper() not in [n.upper() for n in valid_nationalities]:
                        print("Invalid nationality. Please choose from the following list: Portuguesa, Brasileira, Americana, Ucraniana, Russa, Angolana, Moçambicana, Cabo Verdiana, Outro")
                        nationality_input = input("Enter your nationality: ")
                    # Assign the original case input to nationality
                    nationality = nationality_input
                    if pattern == 'B':
                        party = input("Enter the party you want to vote for (PS, BLOCO, PAN, PCP-PEV): ").upper()
                        while party not in valid_parties:
                            print("Invalid party. Please choose from the following list: PS, BLOCO, PAN, PCP-PEV")
                            party = input("Enter the party you want to vote for: ").upper()
                for i in range(times):
                    print(f"Running pattern {pattern}: {i+1}/{times}")
                    config = load_config()
                    logger = setup_logger()
                    form_filler = FormFiller(config, logger)
                    if pattern in ['B', 'C']:
                        form_filler.fill_form(pattern, party, nationality)  # Pass the original case nationality to the fill_form method
                    else:
                        form_filler.fill_form(pattern)
                    form_filler.driver.quit()  # Ensure the driver is quit after each run
                    if i < times - 1:  # No need to wait after the last form is filled
                        print(f"Waiting for {delay} seconds before the next run...")
                        time.sleep(delay)
                print(f"Completed all runs for pattern {pattern}.")
            else:
                print("Invalid pattern. Please try again.")
        elif choice == '2':
            print("Credits: Paulo Costa")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
