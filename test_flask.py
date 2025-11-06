import requests

# Testar health check
response = requests.get("http://localhost:8004/health")
print("Health Check:", response.json())

# Testar análise
test_data = {
    "project_name": "E-commerce Test",
    "project_description": "Sistema de e-commerce",
    "requirements": {
        "data_type": "structured",
        "scalability": "high",
        "consistency": "strong"
    }
}

response = requests.post("http://localhost:8004/analyze-database", json=test_data)
print("Análise:", response.json())