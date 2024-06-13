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


    def fill_form(self, pattern, party=None, nationality=None, academic_background = None):
        if pattern == 'A':
            self.fill_form_randomly()
        elif pattern == 'B':
            self.fill_form_b(party, nationality)
        elif pattern == 'C':
            self.fill_form_c(party, nationality, academic_background)
        else:
            print("Invalid pattern. Please try again.")


    def fill_form_b(self, party, nationality):
            #checking if values are correct
            print(party, nationality)
            
            self.driver.get(self.config['form_url'])
            page_counter = 1  # Initialize page counter

            # Define leader classification based on political preference
            right_leaders = ['Donald Trump', 'Luís Montenegro', 'Nuno Melo', 'Rui Rocha', 'André Ventura']
            left_leaders = ['Joe Biden', 'Paulo Raimundo', 'Mariana Mortágua', 'Inês Sousa Real', 'Pedro Nuno Santos', 'Rui Tavares']

            options_q2 = [
            'Portuguesa', 'Brasileira', 'Americana', 'Ucraniana', 'Russa',
            'Angolana', 'Moçambicana', 'Cabo Verdiana', 'Outro'
           ]
            options_q5 = [
                'PS', 'AD = PSD+CDS', 'PAN', 'Iniciativa Liberal', 'Bloco Esquerda',
                'Chega', 'Livre', 'ADN', 'PCP-PEV', 'Outros'
            ]

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

                # Check if the "Next" button is present to move to the next page
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, 'div[jsname="OCpkoe"]')
                    next_button.click()
                    page_counter += 1  # Increment page counter

                    # Page 6: Select specific radio buttons based on the order
                    if page_counter == 6:
                        # Re-locate the questions on page 6 to avoid stale elements
                        questions = self.driver.find_elements(By.CSS_SELECTOR, 'div[jsmodel="CP1oW"]')
                        question_counter = 0  # Initialize a counter to keep track of the question number
                        for question in questions:
                            question_counter += 1  # Increment the question counter
                            question_text_element = question.find_element(By.CSS_SELECTOR, 'span.M7eMe')
                            question_text = question_text_element.text if question_text_element else "No question text found"
                           

                            # Find the radiogroup within the current question
                            radiogroup = question.find_element(By.CSS_SELECTOR, 'div[role="radiogroup"]')
                            # Find all radio buttons within the current radiogroup
                            radio_buttons = radiogroup.find_elements(By.CSS_SELECTOR, 'div.Od2TWd')

                            # Determine which radio button to select based on the question number
                            if question_counter == 2:
                                # Find the index of the nationality option that matches the parameter
                                option_index = options_q2.index(nationality)
                                # Select the radio button that matches the index
                                radio_buttons[option_index].click()
                            elif question_counter == 5:
                                # Find the index of the party option that matches the parameter
                                option_index = options_q5.index(party)
                                # Select the radio button that matches the index
                                radio_buttons[option_index].click()
                            else:
                                # For all other questions, select a random radio button
                                selected_option = random.choice(radio_buttons)
                                selected_option.click()

                        # Wait for 8 seconds before submitting the form
                        time.sleep(1)

                        # Locate all buttons with the role 'button'
                        buttons = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')

                        # Click the second button, assuming the first is for going back and the second is to submit
                        if len(buttons) > 1:
                            submit_button = buttons[1]  # The second button
                            submit_button.click()
                            time.sleep(1)  # Wait for 1 second after clicking

                        break  # Exit after processing page 6

                except UnexpectedAlertPresentException:
                    # Handle any unexpected alerts
                    alert = Alert(self.driver)
                    alert.accept()



















    def fill_form_c(self, party, nationality, academic_background):
        #checking if values are correct
        print(party, nationality, academic_background)
        
        self.driver.get(self.config['form_url'])
        page_counter = 1  # Initialize page counter

        # Define leader classification based on political preference
        right_leaders = ['Donald Trump', 'Luís Montenegro', 'Nuno Melo', 'Rui Rocha', 'André Ventura']
        left_leaders = ['Joe Biden', 'Paulo Raimundo', 'Mariana Mortágua', 'Inês Sousa Real', 'Pedro Nuno Santos', 'Rui Tavares']

        options_q2 = [
        'Portuguesa', 'Brasileira', 'Americana', 'Ucraniana', 'Russa',
        'Angolana', 'Moçambicana', 'Cabo Verdiana', 'Outro'
        ]
        options_q5 = [
            'PS', 'AD = PSD+CDS', 'PAN', 'Iniciativa Liberal', 'Bloco Esquerda',
            'Chega', 'Livre', 'ADN', 'PCP-PEV', 'Outros'
        ]
        options_q4 = [
            'Sem escolaridade', 'Básico (até 11º completo)', 'Secundário (12º completo)', 'Ensino Superior completo'
        ]

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
                                # Right leaders: Choose from options 5 to 7
                                selected_option = random.choice(radio_buttons[4:7])
                            elif leader_name in left_leaders:
                                # Left leaders: Choose from options 1 to 4
                                selected_option = random.choice(radio_buttons[:4])
                            else:
                                # Default case if leader is not listed
                                selected_option = random.choice(radio_buttons)
                        else:
                            # Sections 1, 2, 3, 4: Choose from options 4 to 7
                            selected_option = random.choice(radio_buttons[3:7])
                        selected_option.click()
                        self.logger.info(f'Page {page_counter}, Leader: {leader_name}, Selected Option: {selected_option.get_attribute("aria-label")}')

            # Check if the "Next" button is present to move to the next page
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'div[jsname="OCpkoe"]')
                next_button.click()
                page_counter += 1  # Increment page counter

                # Page 6: Select specific radio buttons based on the order
                if page_counter == 6:
                    # Re-locate the questions on page 6 to avoid stale elements
                    questions = self.driver.find_elements(By.CSS_SELECTOR, 'div[jsmodel="CP1oW"]')
                    question_counter = 0  # Initialize a counter to keep track of the question number
                    for question in questions:
                        question_counter += 1  # Increment the question counter
                        question_text_element = question.find_element(By.CSS_SELECTOR, 'span.M7eMe')
                        question_text = question_text_element.text if question_text_element else "No question text found"
                    

                        # Find the radiogroup within the current question
                        radiogroup = question.find_element(By.CSS_SELECTOR, 'div[role="radiogroup"]')
                        # Find all radio buttons within the current radiogroup
                        radio_buttons = radiogroup.find_elements(By.CSS_SELECTOR, 'div.Od2TWd')

                        # Determine which radio button to select based on the question number
                        if question_counter == 2:
                            # Find the index of the nationality option that matches the parameter
                            option_index = options_q2.index(nationality)
                            # Select the radio button that matches the index
                            radio_buttons[option_index].click()
                        elif question_counter == 5:
                            # Find the index of the party option that matches the parameter
                            option_index = options_q5.index(party)
                            # Select the radio button that matches the index
                            radio_buttons[option_index].click()
                        elif question_counter == 4:
                            # Find the index of the academic background option that matches the parameter
                            option_index = options_q4.index(academic_background)
                            # Select the radio button that matches the index
                            radio_buttons[option_index].click()
                        else:
                            # For all other questions, select a random radio button
                            selected_option = random.choice(radio_buttons)
                            selected_option.click()

                    # Wait for 1 second before submitting the form
                    time.sleep(10)

                    # Locate all buttons with the role 'button'
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, 'div[role="button"]')

                    # Click the second button, assuming the first is for going back and the second is to submit
                    if len(buttons) > 1:
                        submit_button = buttons[1]  # The second button
                        submit_button.click()
                        time.sleep(1)  # Wait for 1 second after clicking

                    break  # Exit after processing page 6

            except UnexpectedAlertPresentException:
                # Handle any unexpected alerts
                alert = Alert(self.driver)
                alert.accept()























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

        
