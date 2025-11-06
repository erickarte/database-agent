import requests
import json
import os

print("🧪 Testando Database Agent com IA Gemini...")

# A chave deve ser configurada como variável de ambiente
# Exemplo: set GEMINI_API_KEY=sua_chave_aqui
if not os.getenv("GEMINI_API_KEY"):
    print("⚠️  GEMINI_API_KEY não configurada. Usando modo simulação.")

test_data = {
    "project_name": "Rede Social para Desenvolvedores",
    "project_description": "Plataforma social com posts, comentários, likes, mensagens em tempo real e perfis de usuário. Esperamos 100k usuários no primeiro ano.",
    "requirements": {
        "data_type": "mixed",
        "scalability": "very_high", 
        "consistency": "strong",
        "high_read_throughput": True,
        "high_write_throughput": True,
        "real_time": True,
        "data_volume": "massive",
        "concurrent_users": 5000
    }
}

print("📤 Enviando dados para análise...")

try:
    response = requests.post(
        "http://localhost:8004/analyze-database",
        json=test_data,
        headers={"Content-Type": "application/json"},
        timeout=60  # A IA pode demorar um pouco
    )
    
    print(f"✅ Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n🎯 RESPOSTA DO AGENTE:")
        print("=" * 50)
        
        print("\n📊 RECOMENDAÇÕES TRADICIONAIS:")
        for rec in result.get('recommendations', []):
            print(f"  • {rec['database_type']}: {rec['recommendation']}")
            print(f"    Tecnologias: {', '.join(rec['technologies'])}")
        
        print(f"\n🏗️  ARQUITETURA: {result.get('architecture_suggestions', {})}")
        
        print(f"\n🔄 FLUXO DE DADOS:")
        for flow in result.get('data_flow', []):
            print(f"  • {flow}")
        
        print(f"\n⚠️  CONSIDERAÇÕES:")
        for consideration in result.get('considerations', []):
            print(f"  • {consideration}")
        
        print(f"\n🤖 ANÁLISE DA IA GEMINI:")
        print("=" * 50)
        ai_analysis = result.get('ai_analysis', 'Nenhuma análise de IA retornada')
        print(ai_analysis)
        
    else:
        print(f"❌ Erro: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Erro na requisição: {e}")