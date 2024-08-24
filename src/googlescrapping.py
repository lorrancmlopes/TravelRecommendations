import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

# Read cities from CSV
cities_df = pd.read_csv('../data/worldcities.csv')
cities_df = cities_df.head(10)

# Define headers for the HTTP request
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

# Initialize an empty list to store the results
results = []

# Loop through each city
total_cities = len(cities_df)
for index, row in cities_df.iterrows():
    city = row['city']
    country = row['country']
    
    # Construct the search query URL
    search_query = f'"{city}+{country}+tripadvisor"'
    url = f'https://www.google.com/search?q={search_query}&ie=utf-8&oe=utf-8&num=10'
    
    # Send the HTTP request
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    
    # Find the first search result link
    allData = soup.find("div", {"class": "g"})
    
    if allData:
        link = allData.find('a').get('href')
        
        # Extract the code using regex
        code_match = re.search(r'-g(\d+)-', link)
        if code_match:
            code = code_match.group(1)
            # Store the city and code in the results list
            results.append([city, code])
        else:
            results.append([city, 'Code not found'])
    else:
        results.append([city, 'No results found'])

    # Print progress
    print(f'Processed {index + 1}/{total_cities}: {city}, {country}')
    
# Convert the results to a DataFrame
results_df = pd.DataFrame(results, columns=['City', 'Code'])

# Save the results to a CSV file
results_df.to_csv('../data/city_codes.csv', index=False)

print("Finished extracting city codes.")
