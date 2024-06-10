# Python Selenium Form Filler

## Overview
This project is a Python-based automated form filler using Selenium. It is designed to interact with web forms and automate the process of filling them out based on predefined patterns.

## Features
- **Pattern A**: Fills out the form randomly without considering any specific criteria.
- **Pattern B**: Fills out the form based on the user's nationality and political party preference. It uses a list of known leaders and their political leanings to make selections on certain pages of the form.
- **Pattern C**: Currently under development. Intended for future features.

## Setup Instructions
To set up the form filler on your local machine, follow these steps:

1. **Clone the Repository**

```shell
git clone https://github.com/pialo3434/Google-Form-Filler.git
```

2. **Install Dependencies**
Navigate to the cloned repository's directory and install the required Python packages:

```shell
pip install selenium
```

3. **Configure the Project**
Update the `config.json` file with the appropriate values, such as the path to your WebDriver and the URL of the form you want to fill out.

4. **Run the Main Script**
Execute the `main.py` script to start the form filling process:

```shell
python main.py
```


## How to Use
After setting up the project, you can run the `main.py` script. The script will prompt you to choose a pattern and, if necessary, enter your nationality and political party preference. Follow the on-screen instructions to proceed with the form filling.

## WebDriver Setup

For this project to interact with the Microsoft Edge browser, you need to download the appropriate version of the Edge WebDriver. Here's how you can set it up:

1. **Check Your Browser Version**
   First, check the version of Microsoft Edge you are using by navigating to `edge://settings/help` in your browser.

2. **Download Edge WebDriver**
   Go to the Microsoft Edge Driver page and download the WebDriver version that matches your Edge browser version.

3. **Add WebDriver to Path**
   After downloading, extract the contents of the ZIP file and place the `msedgedriver.exe` in a known directory. You will need to add this directory to your system's PATH environment variable, or specify the path directly in the `config.json` file.

4. **Update Config File**
   Update the `driver_path` in the `config.json` file with the full path to the `msedgedriver.exe` file.

By following these steps, you'll ensure that the Selenium WebDriver can control Microsoft Edge to automate your form filling tasks.


## Downloading the Repository via HTTP
If you prefer to download the repository without using Git, you can do so by navigating to the repository's page on GitHub and clicking the 'Download ZIP' button. Once downloaded, extract the contents and follow the setup instructions above.

## Contributing
Contributions to this project are welcome. Please fork the repository, make your changes, and submit a pull request for review.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Credits
Developed by Paulo Costa.
