<img title="DeFiLlama scraper" alt="Header image" src="./header.png">

_Web scraper designed to collect data on various blockchain protocols from the DeFiLlama website. The script extracts the Name, Protocols, and TVL (Total Value Locked) for each blockchain and outputs the data to a CSV file._

## Demo / Example

The script collects and logs data every 5 minutes (adjustable), storing it in `example.csv`.

## Project Modules

<a href='https://pypi.org/project/loguru'><img alt='loguru' src='https://img.shields.io/pypi/v/loguru?label=loguru&color=blue'></a> <a href='https://pypi.org/project/python-dotenv'><img alt='python-dotenv' src='https://img.shields.io/pypi/v/python-dotenv?label=python-dotenv&color=blue'></a> <a href='https://pypi.org/project/selenium'><img alt='selenium' src='https://img.shields.io/pypi/v/selenium?label=selenium&color=blue'></a> <a href='https://pypi.org/project/user_agent'><img alt='user_agent' src='https://img.shields.io/pypi/v/user_agent?label=user_agent&color=blue'></a> 

> Look at the `requirements.txt` file for more details.

## Features

- **Data Extraction**: Scrapes Name, Protocols, and TVL from the DeFiLlama website.
- **Configurable Intervals**: Interval setting for data collection, adjustable via the `.env` file.
- **Proxy Support**: Proxy configuration for secure and stable connections.
- **Logging**: Logs successes and errors for better monitoring and debugging.
- **Error Handling**: Manages network issues and unexpected data corruption.

## Environment Variables

To run this project, you can add the following environment variables (optional):

`DELAY_MINS`
`PROXY_SERVER`

> Look at the .env.sample

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Gubchik123/DeFiLlama-scraper.git
    ```

2. Go to the project directory:

    ```bash
    cd DeFiLlama-scraper
    ```
    
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. OPTIONAL: Create a `.env` file and add the environment variables.

5. Run the script:
    ```bash
    python script.py
    ```