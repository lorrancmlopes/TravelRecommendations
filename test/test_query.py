import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_query_yields_10_results():
    response = client.get("/query?query=Castle")
    json_response = response.json()
    
    assert response.status_code == 200
    assert len(json_response["results"]) == 10
    assert json_response["message"] == "OK"
    
    print("test_query_yields_10_results: PASSED")

def test_query_yields_few_results():
    response = client.get("/query?query=Disneyland")
    json_response = response.json()
    
    assert response.status_code == 200
    assert 1 < len(json_response["results"]) < 10
    assert json_response["message"] == "OK"
    
    print("test_query_yields_few_results: PASSED")


def test_query_yields_non_obvious_results():
    response = client.get("/query?query=Oktoberfest")
    json_response = response.json()
    
    assert response.status_code == 200
    assert len(json_response["results"]) > 0
    assert json_response["message"] == "OK"
    
    # Verify non-obvious results
    results = json_response["results"]
    titles = [result["title"] for result in results]
    assert "Munich" in titles

    print("test_query_yields_non_obvious_results: PASSED")

if __name__ == "__main__":
    test_query_yields_10_results()
    test_query_yields_few_results()
    test_query_yields_non_obvious_results()
