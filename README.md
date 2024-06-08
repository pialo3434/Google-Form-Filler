# Form Filler

This project is a Python script that automates the process of filling out forms. It uses Selenium WebDriver to interact with the form elements on a webpage.

## How it Works

The script navigates to the form URL specified in the configuration file. It then iterates over each question on the form. If the question has radio buttons or checkboxes, the script selects a random option. After filling out all the questions on a page, the script clicks the "Next" button to go to the next page. This process continues until the script reaches the final page, at which point it clicks the "Submit" button to submit the form.

## Setup

1. **Clone the repository**: Clone this repository to your local machine using `git clone <repo_url>`.

2. **Install dependencies**: This project requires Python and Selenium WebDriver. You can install Selenium WebDriver using pip: `pip install selenium`.

3. **Configure the script**: Open the `config.json` file and update the `form_url` and `driver_path` values. `form_url` is the URL of the form you want to fill out, and `driver_path` is the path to your WebDriver executable.

4. **Run the script**: You can run the script using the command `python main.py`.

Please note that this script is intended for educational purposes only. Do not use it to spam or submit false information on forms.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the terms of the MIT license.
