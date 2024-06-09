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


    def fill_form(self, pattern):
        if pattern == 'A':
            self.fill_form_randomly()
        elif pattern in ['B', 'C']:
            print("Still developing...")
        else:
            print("Invalid pattern. Please try again.")

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
                time.sleep(1)

                # Check if the form was submitted successfully
                success_message = self.driver.find_element(By.CSS_SELECTOR, 'div.vHW8K')
                if success_message.text == 'A sua resposta foi registada.':
                    self.logger.info('Form submitted successfully.')
                    break
            except NoSuchElementException:
                # The "Submit" button is not present, so click the "Next" button to go to the next page
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'div[jsname="OCpkoe"]')
                next_button.click()
                continue
            except UnexpectedAlertPresentException:
                # Handle the unexpected alert
                alert = Alert(self.driver)
                alert.accept()

        # Wait for user input before closing the browser
        #input("Press any key to close the browser...")
        self.driver.quit()
