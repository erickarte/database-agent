import pytest
import asyncio
from fastapi.testclient import TestClient
from database_agent import app, ProjectRequest

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_analyze_database_success():
    test_data = {
        "project_name": "Test Project",
        "project_description": "A test project for database analysis",
        "requirements": {
            "data_type": "structured",
            "scalability": "high",
            "consistency": "strong",
            "high_read_throughput": True
        }
    }
    
    response = client.post("/analyze-database", json=test_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] == True
    assert "recommendations" in data
    assert "architecture_suggestions" in data
    assert data["agent_type"] == "database_agent"

def test_analyze_database_invalid_data():
    test_data = {
        "project_name": "Test Project"
        # Missing required fields
    }
    
    response = client.post("/analyze-database", json=test_data)
    assert response.status_code == 400