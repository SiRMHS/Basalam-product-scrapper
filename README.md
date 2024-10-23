# Basalam Product Details Fetcher

## Description
This Python script collects product details from the Basalam API. It takes a search keyword and the number of products to fetch, then retrieves detailed information about each product including pricing, photos, attributes, and categories. The collected data is saved into an Excel file for further use.

## Features
- Collects product IDs based on search keywords.
- Fetches detailed information for each product using their ID.
- Extracts various attributes, including product photos, categories, descriptions, ratings, and more.
- Saves the collected data into an Excel file with a timestamp.

## Requirements
- Python 3.6+
- Libraries:
  - `requests`
  - `pandas`
  - `jdatetime`
  - `openpyxl`

To install the required libraries, run:
```sh
pip install requests pandas jdatetime openpyxl
```

## Usage
1. Run the script:
   ```sh
   python script.py
   ```
2. Enter the word to search for products when prompted.
3. Enter the number of products you want to fetch details for.

The script will generate an Excel file with the product details.

## Example
```sh
enter word for search : لباس
enter number of products : 50
```
The output will be saved as an Excel file named `basalam_products_<current_date_and_time>.xlsx`.

## Notes
- The script includes a delay between each product request to avoid being rate-limited by the API.
- Make sure you have internet access when running the script.

## License
This project is licensed under the MIT License.

