#!/usr/bin/env python3
"""
Forza Car Scraper

This script scrapes the list of cars from the Forza Motorsport website (https://forza.net/fmcars)
and extracts the model and year information for each car. The script uses multiple approaches
to find car data on the website, making it robust against changes in the website's structure.

The script outputs the car data in either JSON or CSV format, and can save the data to a file.

Dependencies:
    - requests: For making HTTP requests
    - beautifulsoup4: For parsing HTML
    - re: For regular expressions (standard library)
    - json: For JSON handling (standard library)
    - argparse: For command-line argument parsing (standard library)
    - csv: For CSV output (standard library)

Installation:
    pip install requests beautifulsoup4

Usage:
    python scrape_forza_cars.py [options]

Options:
    --output, -o  Output file path (default: forza_cars.json)
    --format, -f  Output format: json or csv (default: json)
    --pretty, -p  Pretty-print JSON output
    --quiet, -q   Suppress progress messages

Examples:
    # Basic usage (outputs to forza_cars.json)
    python scrape_forza_cars.py

    # Save to a specific file
    python scrape_forza_cars.py --output cars.json

    # Output as CSV
    python scrape_forza_cars.py --format csv --output cars.csv

    # Pretty-print JSON output
    python scrape_forza_cars.py --pretty

    # Suppress progress messages
    python scrape_forza_cars.py --quiet

    # Run directly (if script is executable)
    ./scrape_forza_cars.py
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from typing import List, Dict, Optional, Tuple

def scrape_forza_cars() -> List[Dict[str, any]]:
    """
    Scrape car data from the Forza website.

    Returns:
        List of dictionaries containing car data with 'model' and 'year' fields.
    """
    url = "https://forza.net/fmcars"

    # Add headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://forza.net/',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }

    # Send a GET request to the URL
    print(f"Fetching data from {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=30)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return []

        print("Successfully retrieved the webpage. Parsing content...")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize a list to store car data
    cars = []

    # Try multiple approaches to find car data

    # Approach 1: Look for car cards or grid items - Forza specific selectors
    print("Trying to find car elements in the page...")
    # Try Forza-specific selectors first
    car_elements = soup.select('.car-list-item, .fm-car-item, .car-card, .vehicle-item, .vehicle-card')

    # If no elements found, try more generic selectors
    if not car_elements:
        car_elements = soup.select('.grid-item, .card, .item, article, .list-item')

    if car_elements:
        print(f"Found {len(car_elements)} car elements using card/grid selectors.")
        for car_element in car_elements:
            try:
                # Try different selectors for car name/title - Forza specific first
                car_name_elem = (
                    car_element.select_one('.car-name, .car-title, .vehicle-name, .car-model, .fm-car-title') or 
                    car_element.select_one('h2, h3, h4, .title, .name') or 
                    car_element.find('h2') or 
                    car_element.find('h3') or 
                    car_element.find('h4')
                )

                # If we can't find a specific element, use the text of the entire card
                if not car_name_elem:
                    car_name = car_element.text.strip()
                    # Try to extract only the relevant part (first line or sentence)
                    car_name_parts = car_name.split('\n')
                    if car_name_parts:
                        car_name = car_name_parts[0].strip()
                else:
                    car_name = car_name_elem.text.strip()

                # Look for year and manufacturer separately if available
                year_elem = car_element.select_one('.car-year, .year, .model-year')
                manufacturer_elem = car_element.select_one('.manufacturer, .make, .car-make')

                if year_elem:
                    try:
                        year = int(year_elem.text.strip())
                        # If we have a separate year element, remove year from car_name if present
                        car_name = re.sub(r'\b' + str(year) + r'\b', '', car_name).strip()
                    except ValueError:
                        year = None
                else:
                    year = None

                # If manufacturer is separate, prepend it to the model if not already included
                if manufacturer_elem:
                    manufacturer = manufacturer_elem.text.strip()
                    if manufacturer and manufacturer.lower() not in car_name.lower():
                        car_name = f"{manufacturer} {car_name}"

                # Extract year and model from the car name if year wasn't found separately
                if year is None:
                    year, model = extract_year_and_model(car_name)
                else:
                    model = car_name

                # Clean up the model name
                model = clean_model_name(model)

                if model:  # Only add if we have a model name
                    cars.append({
                        'game': 'Forza Motorsport',
                        'model': model,
                        'year': year
                    })
            except Exception as e:
                print(f"Error processing car element: {e}")

    # Approach 2: Look for tables with car data
    if not cars:
        print("Trying to find car data in tables...")
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            # Skip header row if it exists
            for row in rows[1:] if len(rows) > 1 else rows:
                try:
                    cells = row.find_all('td')
                    if cells and len(cells) >= 2:
                        # Assume first or second cell contains car name
                        car_name = cells[0].text.strip() or cells[1].text.strip()
                        year, model = extract_year_and_model(car_name)

                        cars.append({
                            'game': 'Forza Motorsport',
                            'model': model,
                            'year': year
                        })
                except Exception as e:
                    print(f"Error processing table row: {e}")

    # Approach 3: Look for lists with car data
    if not cars:
        print("Trying to find car data in lists...")
        list_items = soup.select('ul li, ol li')
        for item in list_items:
            try:
                item_text = item.text.strip()
                # Check if this looks like a car name (contains year or common car brands)
                car_brands = ['ford', 'toyota', 'honda', 'bmw', 'audi', 'mercedes', 'porsche', 'ferrari']
                if any(brand in item_text.lower() for brand in car_brands) or re.search(r'\b\d{4}\b', item_text):
                    year, model = extract_year_and_model(item_text)
                    cars.append({
                        'game': 'Forza Motorsport',
                        'model': model,
                        'year': year
                    })
            except Exception as e:
                print(f"Error processing list item: {e}")

    # Approach 4: Try to find car data in JavaScript variables
    if not cars:
        print("Trying to find car data in JavaScript variables...")
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                script_text = script.string

                # Look for various patterns of car data in JavaScript
                patterns = [
                    r'(?:var|let|const|window\.)\s*cars\s*=\s*(\[.*?\]);',
                    r'(?:var|let|const|window\.)\s*vehicles\s*=\s*(\[.*?\]);',
                    r'(?:var|let|const|window\.)\s*carList\s*=\s*(\[.*?\]);',
                    r'"cars"\s*:\s*(\[.*?\])',
                    r'"vehicles"\s*:\s*(\[.*?\])'
                ]

                for pattern in patterns:
                    try:
                        matches = re.search(pattern, script_text, re.DOTALL)
                        if matches:
                            car_data = json.loads(matches.group(1))
                            print(f"Found car data in JavaScript with pattern: {pattern}")
                            for car in car_data:
                                extract_car_info(car, cars)
                            if cars:
                                break
                    except Exception as e:
                        print(f"Failed to parse car data from script with pattern {pattern}: {e}")

    # Approach 5: Check for API endpoints that might contain car data
    if not cars:
        print("Checking for API endpoints in the page...")
        # Look for API URLs in the page
        api_urls = []

        # Check for API URLs in script tags
        for script in soup.find_all('script'):
            if script.string:
                # Look for patterns like "/api/cars", "api/vehicles", etc.
                api_matches = re.findall(r'["\'](/?(api|data)/[^"\']+)["\']', script.string)
                if api_matches:
                    for match in api_matches:
                        api_url = match[0]
                        if 'car' in api_url.lower() or 'vehicle' in api_url.lower():
                            if api_url.startswith('/'):
                                api_url = f"https://forza.net{api_url}"
                            elif not api_url.startswith('http'):
                                api_url = f"https://forza.net/{api_url}"
                            api_urls.append(api_url)

        # Try each potential API URL
        for api_url in api_urls:
            print(f"Trying API URL: {api_url}")
            try:
                api_response = requests.get(api_url, headers=headers, timeout=30)
                if api_response.status_code == 200:
                    try:
                        # Try to parse as JSON
                        api_data = api_response.json()

                        # Look for car data in the response
                        if isinstance(api_data, list):
                            # If it's a list, assume it's a list of cars
                            for car in api_data:
                                if isinstance(car, dict):
                                    extract_car_info(car, cars)
                        elif isinstance(api_data, dict):
                            # If it's a dict, look for lists of cars
                            for key, value in api_data.items():
                                if isinstance(value, list) and ('car' in key.lower() or 'vehicle' in key.lower()):
                                    for car in value:
                                        if isinstance(car, dict):
                                            extract_car_info(car, cars)

                        if cars:
                            print(f"Found {len(cars)} cars from API endpoint.")
                            break
                    except json.JSONDecodeError:
                        print(f"API response is not valid JSON: {api_url}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch API URL {api_url}: {e}")

    # If we still don't have cars, try a more aggressive approach
    if not cars:
        print("Trying more aggressive approach to find car data...")
        # Look for any text that might contain car information
        all_text = soup.get_text()

        # Split by newlines and process each line
        lines = [line.strip() for line in all_text.split('\n') if line.strip()]

        for line in lines:
            # Check if line looks like a car name
            if re.search(r'\b\d{4}\b', line) and len(line) < 100:  # Year and reasonable length
                year, model = extract_year_and_model(line)
                if model and not model.isdigit() and len(model) > 3:  # Basic validation
                    model = clean_model_name(model)
                    if model:
                        cars.append({
                            'game': 'Forza Motorsport',
                            'model': model,
                            'year': year
                        })

    # Remove duplicates based on model and year
    unique_cars = []
    seen = set()
    for car in cars:
        key = (car['model'], car['year'])
        if key not in seen:
            seen.add(key)
            unique_cars.append(car)

    print(f"Found {len(unique_cars)} unique cars in total.")
    return unique_cars

def extract_year_and_model(car_name: str) -> Tuple[Optional[int], str]:
    """
    Extract the year and model from a car name string.

    Args:
        car_name: The full car name string, potentially including year.

    Returns:
        A tuple containing (year, model) where year is an integer or None.
    """
    # Try to match a year at the beginning of the string (e.g., "2020 Ford Mustang")
    year_match = re.match(r'^(\d{4})\s+(.+)$', car_name)

    if year_match:
        year = int(year_match.group(1))
        model = year_match.group(2).strip()
        return year, model

    # If no year at the beginning, try to find it elsewhere in the string
    year_match = re.search(r'\b(\d{4})\b', car_name)
    if year_match:
        year = int(year_match.group(1))
        # Remove the year from the car name to get the model
        model = car_name.replace(year_match.group(0), '').strip()
        return year, model

    # If no year found, return None for year and the original string as model
    return None, car_name

def clean_model_name(model: str) -> str:
    """
    Clean up a car model name by removing extra spaces, special characters, etc.

    Args:
        model: The car model name to clean.

    Returns:
        A cleaned version of the car model name.
    """
    if not model:
        return ""

    # Remove any extra whitespace
    model = ' '.join(model.split())

    # Remove common prefixes/suffixes that aren't part of the model name
    prefixes_to_remove = ['the ', 'new ', 'all-new ']
    for prefix in prefixes_to_remove:
        if model.lower().startswith(prefix):
            model = model[len(prefix):]

    # Remove any trailing special characters
    model = model.rstrip('.,;:-')

    # Remove any text in parentheses if it's just a specification
    model = re.sub(r'\s*\([^)]*\)\s*$', '', model)

    # Remove any text after common separators if it's just a specification
    for separator in [' - ', ' – ', ' | ']:
        if separator in model:
            parts = model.split(separator, 1)
            if len(parts[1].split()) <= 3:  # If the second part is short, it's likely a spec
                model = parts[0]

    return model.strip()

def extract_car_info(car_data: Dict, cars_list: List[Dict]):
    """
    Extract car information from a dictionary and add it to the cars list.

    Args:
        car_data: Dictionary containing car data.
        cars_list: List to append the extracted car information to.
    """
    # Try different possible key names for the car model
    model_keys = ['name', 'model', 'title', 'carName', 'car_name', 'vehicleName', 'vehicle_name']
    model = None
    for key in model_keys:
        if key in car_data and car_data[key]:
            model = car_data[key]
            break

    if not model:
        # If no model found with known keys, try to find any string value that might be a model name
        for key, value in car_data.items():
            if isinstance(value, str) and len(value) > 3 and not key.lower() in ['id', 'url', 'image', 'img']:
                model = value
                break

    # Try different possible key names for the year
    year_keys = ['year', 'modelYear', 'model_year', 'carYear', 'car_year']
    year = None
    for key in year_keys:
        if key in car_data and car_data[key]:
            try:
                year = int(car_data[key])
                break
            except (ValueError, TypeError):
                pass

    # If year is not directly available, try to extract it from the model name
    if not year and model:
        year, model = extract_year_and_model(model)

    # Clean up the model name
    if model:
        model = clean_model_name(model)

    # Only add if we have a valid model
    if model:
        cars_list.append({
            'game': 'Forza Motorsport',
            'model': model,
            'year': year
        })

def main():
    """Main function to run the scraper and output the results."""
    import argparse

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Scrape car data from the Forza website.')
    parser.add_argument('--output', '-o', type=str, default='forza_cars.json',
                        help='Output file path (default: forza_cars.json)')
    parser.add_argument('--format', '-f', choices=['json', 'csv'], default='json',
                        help='Output format (default: json)')
    parser.add_argument('--pretty', '-p', action='store_true',
                        help='Pretty-print JSON output')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Suppress progress messages')

    args = parser.parse_args()

    # Run the scraper
    cars = scrape_forza_cars()

    # Print the number of cars found
    if not args.quiet:
        print(f"Found {len(cars)} cars")

    # Save the results to the specified file
    output_file = args.output

    if args.format == 'json':
        with open(output_file, 'w') as f:
            if args.pretty:
                json.dump(cars, f, indent=2)
            else:
                json.dump(cars, f)
    elif args.format == 'csv':
        import csv
        with open(output_file, 'w', newline='') as f:
            fieldnames = ['game', 'model', 'year']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for car in cars:
                writer.writerow(car)

    if not args.quiet:
        print(f"Car data saved to {output_file}")

    return cars

if __name__ == "__main__":
    main()
