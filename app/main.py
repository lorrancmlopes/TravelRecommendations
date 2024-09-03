from fastapi import FastAPI, Query
import uvicorn
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Load the dataset
df = pd.read_csv('../data/cleaned_dataset.csv')  

# Vectorize the descriptions using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Attractions'])  

# Define the main route
@app.get("/")
def main_route():
    return {"message": "Welcome! Please make your search requests at the route /query"}

# Define the query endpoint
@app.get("/query")
def query_route(query: str = Query(..., description="Search query")):
    # Vectorize the query using the same vectorizer used for the dataset
    query_vec = tfidf_vectorizer.transform([query])
    
    # Compute cosine similarity between the query and the dataset
    cosine_sim = cosine_similarity(query_vec, tfidf_matrix)
    
    # Get all similarity scores
    similarity_scores = list(enumerate(cosine_sim[0]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    results = []
    for idx, score in similarity_scores:
        if score > 0.0:
            result = {
                "title": df.iloc[idx]['City'],  
                "content": df.iloc[idx]['Attractions'],  
                "relevance": score
            }
            results.append(result)
        if len(results) == 10:  # Stop after getting 10 results
            break
    
    return {"results": results, "message": "OK"}

# Run the API
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
