# Travel Recommendation System

## Overview

I developed this Travel Recommendation System as part of the C5.1 Supervised Project Activity. The system provides travel recommendations through an API based on attractions from various cities worldwide. It uses TF-IDF vectorization to match user queries with relevant city attractions.

## Theme and Relevance

The theme of this project is highly relevant in today's world where travel planning has become increasingly digital. Travelers seek information on top attractions when deciding where to go, and this API helps streamline that process by providing recommendations based on city-specific attractions. Whether you're looking for cultural landmarks, amusement parks, or historic sites, this recommendation system offers quick and relevant information for travel planning.

## Unique Dataset

My dataset is unique because I created it by combining data from the [World Cities Dataset](https://www.kaggle.com/datasets/viswanathanc/world-cities-datasets) with web scraping techniques to obtain city-specific codes from Tripadvisor, which are not available elsewhere. These codes were used to scrape the top attractions and their descriptions for each city directly from Tripadvisor. Unlike many open or common datasets, this dataset was built from scratch, ensuring that it is both exclusive and tailored to this recommendation system.

## Data Collection Process

My dataset is built from scratch using the following steps:
1. I began with the [World Cities Dataset](https://www.kaggle.com/datasets/viswanathanc/world-cities-datasets) to obtain a list of city names.
2. Using Selenium, I searched Google for Tripadvisor links associated with each city and extracted the unique city codes embedded in these URLs.
3. With the city codes, I programmatically accessed Tripadvisor to scrape the top attractions and their descriptions for each city, ensuring the data is current and tailored specifically for my needs.


## Key Features

- **Unique Dataset**: This dataset is not simply taken from Kaggle or another open repository. It includes city names, corresponding Tripadvisor codes, and the top attractions with descriptions, obtained using custom web scraping.
- **API Implementation**: The server is built using FastAPI and serves recommendations based on a GET request to the `/query` endpoint.
- **TF-IDF Vectorization**: The query processing and document matching are done using TF-IDF vectorization to ensure relevant results.

## Using it

- If you are connected to [Insper](https://www.insper.edu.br/en/home)'s WiFi network, use these links below:
### Example Requests

1. **Test that yields 10 results**:
    
    http://10.103.0.28:8080/query?query=Castle
   
   - Searching for "Castle" returns up to 10 cities with notable castles.

2. **Test that yields less than 10 results**:
    
    http://10.103.0.28:8080/query?query=Disneyland
    
   - Searching for "Disneyland" returns fewer than 10 results, focusing on cities with Disneyland attractions.

3. **Test that yields something non-obvious**:
    
    http://10.103.0.28:8080/query?query=Oktoberfest
    
   - For this test, I used the query "Oktoberfest" with the expectation of receiving results related to Munich, Germany, which is world-famous for its Oktoberfest celebration. However, the first result returned was for the city of Blumenau, Brazil.
Blumenau is a city in Brazil that was heavily influenced by German immigration, and it hosts one of the largest Oktoberfest celebrations outside of Germany. The relevance score for Blumenau was higher than for Munich, which was unexpected. This non-obvious result highlights how the dataset and the TF-IDF model consider the significance of Oktoberfest in Blumenau, possibly due to the high concentration of relevant keywords in the city's description.
This result is curious because it showcases the cultural impact of German immigration in Brazil, where Blumenau's Oktoberfest has grown to rival the original event in Munich in terms of authenticity and scale. The fact that Blumenau appeared first demonstrates the model's ability to surface relevant yet less obvious connections between a query and its results.




## Local Installation

To set up the project locally, follow these steps:

1. Clone this repository:
    ```bash
    git clone https://github.com/lorrancmlopes/TravelRecommendations/
    ```
2. Create a virtual environment:
    ```bash
    python -m venv env
    ```
3. Activate the virtual environment:
    - On Windows:
      ```bash
      .\env\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source env/bin/activate
      ```
4. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
5. Ensure that you have ChromeDriver installed and accessible for the Selenium scraper to work.

## Running the Server

1. Make sure you are at `app` directory:
    ```bash
    cd app
    ```
2. Run the FastAPI server:
    ```bash
    uvicorn main:app --reload
    ```
3. Access your API at the URL provided in the terminal

## Usage

### API Endpoint

- **GET /query**

  - **Query Parameters**:
    - `query`: A string representing the search query.
  
  - **Response**:
    - A JSON object containing up to ten relevant documents for the search, formatted as follows:
      ```json
      {
        "results": [
          {
            "title": "City Name",
            "content": "Top attractions and descriptions",
            "relevance": 0.3
          },
          ...
        ],
        "message": "OK"
      }
      ```
      
## Testing

You can run the provided tests to validate the functionality of the API:

```bash
python tests/test_api.py
```

The tests include:
- `test_query_yields_10_results`: Ensures that a query returns exactly 10 results.
- `test_query_yields_few_results`: Ensures that a query returns more than 1 but fewer than 10 results.
- `test_query_yields_non_obvious_results`: Ensures that a query returns non-obvious results (e.g., Munich for Oktoberfest).


## Running the Project with Docker

```bash
docker build -t travelrecommendations
docker run -d -p 9876:8888 travelrecommendations
```

<br>
@2024, Insper. 9° Semester,  Computer Engineering.
<br>

_Natural Language Processing Discipline_
