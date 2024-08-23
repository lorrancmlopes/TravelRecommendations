import asyncio
import random
import time
import re
from typing import List, Dict
import httpx
from bs4 import BeautifulSoup
import json
import pandas as pd  # Add pandas for tabular output

# Rotate user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
]

# The message to remove from the descriptions
AI_GENERATED_MESSAGE = (
    "This attraction description was created by AI, using information and phrases commonly found in reviews users submitted to Tripadvisor. Tripadvisor did not create and is not responsible for this description. Please read full traveler reviews for more details and information. If you believe something in this AI-generated description is inaccurate, pleaseshare your feedback."
)

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

async def run_scraper():
    random_user_agent = random.choice(USER_AGENTS)
    headers = {
        "User-Agent": random_user_agent,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    }

    async with httpx.AsyncClient(headers=headers, timeout=httpx.Timeout(30.0)) as client:
        results = []
        
        with open('links.txt', 'r') as file:
            lines = file.readlines()
        
        for line in lines:
            # Extract country code and name from each line
            match = re.match(r'https://www.tripadvisor.com/Tourism-(g\d+)-(.*?)-Vacations.html', line.strip())
            if match:
                code = match.group(1)
                name = match.group(2)
                name = name.replace('-', '_')  # Replace hyphens with underscores for the country key
                print(f"Scraping {name} attractions...")
                
                url = f"https://www.tripadvisor.com/Attractions-{code}-Activities-{name}.html"
                attractions = await scrape_attractions(url, client)
                
                if attractions:
                    # Concatenate attraction names and descriptions into a single string
                    attraction_text = ' '.join([f"{attr['name']}: {attr['description']}" for attr in attractions])
                    results.append({"Country": name, "Attractions": attraction_text})
                
                # Random delay to avoid getting blocked
                time.sleep(random.uniform(2, 5))
        
        # Convert results to a DataFrame
        df = pd.DataFrame(results)
        
        # Save results to a CSV file (or any other format you prefer)
        df.to_csv('attractions.csv', index=False)
        
        print("Scraping complete. Data saved to 'attractions.csv'.")
        
        # Display the table
        print(df)

if __name__ == "__main__":
    asyncio.run(run_scraper())
