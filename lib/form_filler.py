import os
import random
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.alert import Alert

class FormFiller:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Edge(service=Service(config['driver_path'], log_path=os.devnull), options=options)


    def fill_form(self, pattern, party=None, nationality=None):
        if pattern == 'A':
            self.fill_form_randomly()
        elif pattern == 'B':
            self.fill_form_b(party, nationality)
        elif pattern == 'C':
            print("Still developing...")
        else:
            print("Invalid pattern. Please try again.")










    def fill_form_b(self, party, nationality):
        self.driver.get(self.config['form_url'])
        page_counter = 1  # Initialize page counter

        # Define leader classification based on political preference
        right_leaders = ['Donald Trump', 'Luís Montenegro', 'Nuno Melo', 'Rui Rocha', 'André Ventura']
        left_leaders = ['Joe Biden', 'Paulo Raimundo', 'Mariana Mortágua', 'Inês Sousa Real', 'Pedro Nuno Santos', 'Rui Tavares']

        while True:
            # Wait for the questions on the current page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jsmodel="CP1oW"]'))
            )

            # Get all the questions on the current page
            questions = self.driver.find_elements(By.CSS_SELECTOR, 'div[jsmodel="CP1oW"]')

            for question in questions:
                # Check if the question has radio groups
                radiogroups = question.find_elements(By.CSS_SELECTOR, 'div[role="radiogroup"]')
                for radiogroup in radiogroups:
                    # Find all radio buttons in the current radiogroup
                    radio_buttons = radiogroup.find_elements(By.CSS_SELECTOR, 'div.Od2TWd')
                    if radio_buttons:
                        # Initialize leader_name as "Unknown Leader" before the if conditions
                        leader_name = "Unknown Leader"
                        # Section 5: Determine the leader's political preference
                        if page_counter == 5:
                            leader_name_element = radiogroup.find_element(By.CSS_SELECTOR, 'div.OIC90c')
                            leader_name = leader_name_element.text if leader_name_element else leader_name
                            if leader_name in right_leaders:
                                # Right leaders: Choose from options 1 to 4
                                selected_option = random.choice(radio_buttons[:4])
                            elif leader_name in left_leaders:
                                # Left leaders: Choose from options 5 to 7
                                selected_option = random.choice(radio_buttons[4:7])
                            else:
                                # Default case if leader is not listed
                                selected_option = random.choice(radio_buttons)
                        elif page_counter == 1:
                            # Section 1: Choose from options 1 to 3
                            selected_option = random.choice(radio_buttons[:3])
                        else:
                            # Sections 2, 3, 4: Choose from options 1 to 4
                            selected_option = random.choice(radio_buttons[:4])
                        selected_option.click()
                        self.logger.info(f'Page {page_counter}, Leader: {leader_name}, Selected Option: {selected_option.get_attribute("aria-label")}')

                        # Section 6: Specific handling for nationality and party
                        if page_counter == 6:
                            # Handle the second question for nationality
                            if question == questions[1]:  # Assuming the second question is at index 1
                                for button in radio_buttons:
                                    nationality_text_element = button.find_element(By.CSS_SELECTOR, 'div.OIC90c')
                                    nationality_text = nationality_text_element.text if nationality_text_element else ""
                                    if nationality_text.upper() == nationality.upper():
                                        button.click()
                                        break
                            # Handle the last question for party
                            elif question == questions[-1]:  # Assuming the last question is at the last index
                                for button in radio_buttons:
                                    party_text_element = button.find_element(By.CSS_SELECTOR, 'div.OIC90c')
                                    party_text = party_text_element.text if party_text_element else ""
                                    if party_text.upper() == party.upper():
                                        button.click()
                                        break
                            else:
                                # For other questions in section 6, choose randomly
                                random.choice(radio_buttons).click()

            # Check if the "Next" button is present to move to the next page
            try:
                if page_counter == 6:
                    time.sleep(30)
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'div[jsname="OCpkoe"]')
                next_button.click()
                page_counter += 1  # Increment page counter
                if page_counter > 6:  # Stop after filling out section 5
                    break
            except NoSuchElementException:
                # No more pages to navigate, break the loop
                break
            except UnexpectedAlertPresentException:
                # Handle the unexpected alert
                alert = Alert(self.driver)
                alert.accept()

        self.driver.quit()












    def fill_form_randomly(self):
        self.driver.get(self.config['form_url'])

        while True:
            # Wait for the questions on the current page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[jsmodel="CP1oW"]'))
            )

            # Get all the questions on the current page
            questions = self.driver.find_elements(By.CSS_SELECTOR, 'div[jsmodel="CP1oW"]')

            for question in questions:
                # Check if the question has radio groups
                radiogroups = question.find_elements(By.CSS_SELECTOR, 'div[role="radiogroup"]')
                for radiogroup in radiogroups:
                    # Find all radio buttons in the current radiogroup
                    radio_buttons = radiogroup.find_elements(By.CSS_SELECTOR, 'div.Od2TWd')
                    if radio_buttons:
                        # Select a random radio button
                        selected_option = random.choice(radio_buttons)
                        selected_option.click()
                        self.logger.info(f'{question.text}, Selected Option: {selected_option.get_attribute("aria-label")}')
                        continue

            # Check if the "Submit" button is present
            try:
                submit_button = self.driver.find_element(By.CSS_SELECTOR, 'div[jsname="M2UYVd"]')
                
                submit_button.click()

                # Check if the form was submitted successfully
                success_message = self.driver.find_element(By.CSS_SELECTOR, 'div.vHW8K')
                if success_message.text == 'A sua resposta foi registada.':
                    self.logger.info('Form submitted successfully.')
                    break
            except NoSuchElementException:
                # The "Submit" button is not present, so click the "Next" button to go to the next page
                time.sleep(1)
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'div[jsname="OCpkoe"]')
                next_button.click()
                continue
            except UnexpectedAlertPresentException:
                # Handle the unexpected alert
                alert = Alert(self.driver)
                alert.accept()

        self.driver.quit()
