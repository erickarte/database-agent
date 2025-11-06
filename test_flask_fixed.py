import requests
import json

print("🧪 Testando Database Agent com Flask...")

# Testar Health Check
try:
    print("\n1. Testando Health Check...")
    response = requests.get("http://localhost:8004/health")
    print(f"✅ Status: {response.status_code}")
    print(f"✅ Resposta: {response.json()}")
except Exception as e:
    print(f"❌ Erro no Health Check: {e}")

# Testar Análise de Banco de Dados
try:
    print("\n2. Testando Análise de Banco de Dados...")
    
    test_data = {
        "project_name": "E-commerce Platform",
        "project_description": "Plataforma de e-commerce com alta escalabilidade",
        "requirements": {
            "data_type": "structured",
            "scalability": "high",
            "consistency": "strong",
            "high_read_throughput": True,
            "data_volume": "large"
        }
    }
    
    response = requests.post(
        "http://localhost:8004/analyze-database",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"✅ Status: {response.status_code}")
    print("✅ Resposta:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    
except Exception as e:
    print(f"❌ Erro na Análise: {e}")

print("\n🎯 Teste completo!")