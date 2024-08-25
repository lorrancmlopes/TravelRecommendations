# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import re
# import time

# # Read cities from CSV
# cities_df = pd.read_csv('../data/worldcities.csv')
# #cities_df = cities_df.head(10)  # For testing purposes

# # Initialize WebDriver (ensure you have ChromeDriver installed)
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)

# # Initialize an empty list to store the results
# results = []

# # Open the file in append mode
# with open('../data/city_codesV3.csv', 'a') as file:
#     # Loop through each city
#     total_cities = len(cities_df)
#     for index, row in cities_df.iterrows():
#         city = row['city']
#         country = row['country']

#         # Construct the search query URL
#         search_query = f'{city}+{country}+tripadvisor'
#         url = f'https://www.google.com/search?q={search_query}&ie=utf-8&oe=utf-8&num=10'

#         # Navigate to the Google search page
#         driver.get(url)

#         # Allow time for the page to load (adjust time if necessary)
#         time.sleep(1)

#         # Get all search result links
#         all_links = driver.find_elements(By.XPATH, '//a')

#         code_found = False
#         for link_tag in all_links:
#             link = link_tag.get_attribute('href')

#             # Check if link is not None and is from Tripadvisor
#             if link and 'tripadvisor' in link:
#                 # Extract the code using regex
#                 code_match = re.search(r'-g(\d+)-', link)
#                 if code_match:
#                     code = code_match.group(1)
#                     # Store the city and code in the results list
#                     results.append([city, code])
#                     print(f'Found code for {city}, {country}: {code}')
#                     code_found = True
#                     break

#         # If no code was found, add a placeholder
#         if not code_found:
#             results.append([city, 'Code not found'])

#         # Write the result to the file
#         file.write(f'{city},{code}, {link}\n')

#         # Print progress
#         #print(f'Processed {index + 1}/{total_cities}: {city}, {country}')

# # Convert the results to a DataFrame
# results_df = pd.DataFrame(results, columns=['City', 'Code'])

# # Save the results to a CSV file
# results_df.to_csv('../data/city_codesV3.csv', index=False, mode='a', header=False)

# print("Finished extracting city codes.")

# # Close the browser
# driver.quit()



import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
import asyncio
import random
from typing import List, Dict
import httpx
from bs4 import BeautifulSoup

# Rotate user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
]

# The message to remove from the descriptions
AI_GENERATED_MESSAGE = (
    "This attraction description was created by AI, using information and phrases commonly found in reviews users submitted to Tripadvisor. Tripadvisor did not create and is not responsible for this description. Please read full traveler reviews for more details and information. If you believe something in this AI-generated description is inaccurate, pleaseshare your feedback."
)

# Initialize WebDriver (ensure you have ChromeDriver installed)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Function to scrape attractions after getting the city code
async def scrape_attractions(url: str, client: httpx.AsyncClient) -> List[Dict[str, str]]:
    """Scrape attractions from the given URL."""
    try:
        response = await client.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        attractions = []
        
        # Find all divs with the specific data-automation attribute
        attraction_divs = soup.find_all("div", attrs={"data-automation": "topAttractionsProductCard"})
        
        if len(attraction_divs) != 12:
            print(f"Warning: Expected 12 attractions but found {len(attraction_divs)}")
        
        for div in attraction_divs:
            # Find the attraction name inside the span
            name_tag = div.find("span")
            name = name_tag.get_text(strip=True) if name_tag else "No name found"
            
            # Find the description inside the div with class name "vxjUl"
            description_div = div.find("div", class_="vxjUl")
            description = description_div.get_text(strip=True) if description_div else "No description found"
            
            # Remove the AI-generated message from the description
            if description.endswith(AI_GENERATED_MESSAGE):
                description = description.replace(AI_GENERATED_MESSAGE, "").strip()
            
            # Adjust descriptions starting with "By..."
            if description.startswith("By"):
                # Use a regular expression to find the last capital letter and keep the substring from there
                match = re.search(r'[A-Z][^A-Z]*$', description)
                if match:
                    description = match.group(0)
            
            attractions.append({"name": name[3:], "description": description})
        
        return attractions

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return []

async def run_scraper(city: str, code: str, city_name: str):
    random_user_agent = random.choice(USER_AGENTS)
    headers = {
        "User-Agent": random_user_agent,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }

    async with httpx.AsyncClient(headers=headers, timeout=httpx.Timeout(30.0)) as client:
        results = []
        
        if code != 'Code not found':
            print(f"Scraping {city} attractions...")
            
            # Construct the URL using the city code and city name
            url = f"https://www.tripadvisor.com/Attractions-{code}-Activities-{city_name}.html"
            attractions = await scrape_attractions(url, client)
            
            if attractions:
                # Concatenate attraction names and descriptions into a single string
                attraction_text = ' '.join([f"{attr['name']}: {attr['description']}" for attr in attractions])
                results.append({"City": city, "Attractions": attraction_text})
            
            # Convert results to a DataFrame
            df = pd.DataFrame(results)
            
            # Save results to a CSV file
            df.to_csv('attractions_cities2.csv', index=False, mode='a', header=False)
            
            print(f"Scraping for {city} complete. Data saved.")

def scrape_city_codes_and_run_scraper(cities_df):
    # Loop through each city
    total_cities = len(cities_df)
    for index, row in cities_df.iterrows():
        city = row['city']
        country = row['country']

        # Construct the search query URL
        search_query = f'{city}+{country}+tripadvisor'
        url = f'https://www.google.com/search?q={search_query}&ie=utf-8&oe=utf-8&num=10'

        # Navigate to the Google search page
        driver.get(url)

        # Allow time for the page to load (adjust time if necessary)
        time.sleep(1)

        # Get all search result links
        all_links = driver.find_elements(By.XPATH, '//a')

        code_found = False
        for link_tag in all_links:
            link = link_tag.get_attribute('href')

            # Check if link is not None and is from Tripadvisor
            if link and 'tripadvisor' in link:
                # Extract the code and city name from the link
                code_match = re.search(r'-(g\d+)-(.*?)-Vacations.html', link)
                if code_match:
                    code = code_match.group(1)
                    city_name = code_match.group(2)
                    # Full city code and name for constructing the URL
                    print(f'Found code for {city}, {country}: {code}-{city_name}')
                    
                    # Run the scraper for this city immediately
                    asyncio.run(run_scraper(city, code, city_name))
                    code_found = True
                    break

        # If no code was found, print a message
        if not code_found:
            print(f'No code found for {city}, {country}')
            asyncio.run(run_scraper(city, 'Code not found', ''))

        # Print progress
        print(f'Processed {index + 1}/{total_cities}: {city}, {country}')

if __name__ == "__main__":
    # Read the cities from CSV
    cities_df = pd.read_csv('../data/worldcities.csv')
    #cities_df = cities_df.head(10)  # For testing purposes
    # start from line 639
    cities_df = cities_df.iloc[1316:]

    # Scrape city codes and immediately run the scraper for each
    scrape_city_codes_and_run_scraper(cities_df)

    # Close the browser
    driver.quit()
