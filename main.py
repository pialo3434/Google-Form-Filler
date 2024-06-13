from lib.config_loader import load_config
from lib.form_filler import FormFiller
from lib.logger_setup import setup_logger
import time

def main():
    valid_parties = ['PS', 'BLOCO', 'PAN', 'PCP-PEV', 'Chega', 'AD = PSD+CDS']  # Added 'AD = PSD+CDS'
    valid_nationalities = ['Portuguesa', 'Brasileira', 'Americana', 'Ucraniana', 'Russa', 'Angolana', 'Moçambicana', 'Cabo Verdiana', 'Outro']
    academic_backgrounds = ['Sem escolaridade', 'Básico (até 11º completo)', 'Secundário (12º completo)', 'Ensino Superior completo']
    
    while True:
        print("\n1. Start")
        print("2. Credits")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            pattern = input("Enter the pattern (A - Random, B - PS, C - Chega, D - AD = PSD+CDS): ").upper()  # Updated prompt
            if pattern in ['A', 'B', 'C', 'D']:  
                times = int(input(f"How many times do you want to run pattern {pattern}? "))
                delay = int(input("Enter the delay in seconds between each run: "))
                nationality = None
                party = None
                academic_background = None
                
                if pattern in ['B', 'C', 'D']:  
                    print("Select your nationality:")
                    for i, option in enumerate(valid_nationalities, 1):
                        print(f"{i}. {option}")
                    nationality_choice = int(input("Enter the number corresponding to your nationality: "))
                    while nationality_choice < 1 or nationality_choice > len(valid_nationalities):
                        print("Invalid choice. Please select a number between 1 and " + str(len(valid_nationalities)))
                        nationality_choice = int(input("Enter the number corresponding to your nationality: "))
                    nationality = valid_nationalities[nationality_choice - 1]
                    
                    print("Select the party you want to vote for:")
                    for i, option in enumerate(valid_parties, 1):
                        print(f"{i}. {option}")
                    party_choice = int(input("Enter the number corresponding to the party: "))
                    while party_choice < 1 or party_choice > len(valid_parties):
                        print("Invalid choice. Please select a number between 1 and " + str(len(valid_parties)))
                        party_choice = int(input("Enter the number corresponding to the party: "))
                    party = valid_parties[party_choice - 1]
                    
                    print("Select your academic background:")
                    for i, option in enumerate(academic_backgrounds, 1):
                        print(f"{i}. {option}")
                    academic_choice = int(input("Enter the number corresponding to your academic background: "))
                    while academic_choice < 1 or academic_choice > len(academic_backgrounds):
                        print("Invalid choice. Please select a number between 1 and " + str(len(academic_backgrounds)))
                        academic_choice = int(input("Enter the number corresponding to your academic background: "))
                    academic_background = academic_backgrounds[academic_choice - 1]
                
                for i in range(times):
                    print(f"Running pattern {pattern}: {i+1}/{times}")
                    config = load_config()
                    logger = setup_logger()
                    form_filler = FormFiller(config, logger)
                    if pattern in ['B', 'C', 'D']:  
                        form_filler.fill_form(pattern, party, nationality, academic_background)  # Pass the additional academic_background parameter
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
