import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import glob

# Function to scrape the security id from the BSE website
def get_security_id(scripcd):
    url = f"https://m.bseindia.com/StockReach.aspx?scripcd={scripcd}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        security_id_tag = soup.find(id="tdCShortName")
        if security_id_tag:
            return security_id_tag.text
    return None

# Function to process a single CSV file
def process_file(file_path, output_folder):
    # Load the CSV file, skipping the first 5 lines to ignore metadata
    df = pd.read_csv(file_path, skiprows=5)

    # Iterate over each row to update the 'Symbol with Comma for External Upload' column
    for index, row in df.iterrows():
        symbol = str(row['Symbol'])
        if pd.notnull(symbol) and symbol.isdigit():
            security_id = get_security_id(symbol)
            if security_id:
                df.at[index, 'Symbol with Comma for External Upload'] = security_id + ","

    # Generate the output file path and save the updated DataFrame
    output_file_path = os.path.join(output_folder, os.path.basename(file_path))
    df.to_csv(output_file_path, index=False)
    print(f"Updated CSV file has been saved to {output_file_path}")

# Main function to process all CSV files in a folder
def process_all_files(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of all CSV files in the input folder
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))

    # Process each CSV file
    for csv_file in csv_files:
        print(f"Processing file: {csv_file}")
        process_file(csv_file, output_folder)

if __name__ == "__main__":
    # Define the input and output folders
    input_folder = 'path_to_your_input_folder'  # Replace with your input folder path (e.g., sectoral data downloaded from StockEdge)
    output_folder = 'path_to_your_output_folder'  # Replace with your output folder path

    # Process all files in the input folder
    process_all_files(input_folder, output_folder)
