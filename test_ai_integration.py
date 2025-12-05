import requests
import json
import os
from dotenv import load_dotenv  # Adicione esta linha

print("🧪 Testando Database Agent com OpenAI...")

# 🔥 Carregar .env primeiro
load_dotenv()

# A chave deve estar no arquivo .env
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    # Mostrar chave mascarada para segurança
    masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
    print(f"✅ OPENAI_API_KEY detectada no .env (chave: {masked_key})")
else:
    print("⚠️  OPENAI_API_KEY não configurada no .env. Usando modo simulação.")

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
        timeout=60
    )
    
    print(f"✅ Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n🎯 RESPOSTA DO AGENTE:")
        print("=" * 60)
        
        print("\n📊 RECOMENDAÇÕES TRADICIONAIS:")
        for rec in result.get('recommendations', []):
            print(f"  • {rec.get('database_type', 'N/A')}: {rec.get('recommendation', 'N/A')}")
            if 'technologies' in rec:
                print(f"    🛠️  Tecnologias: {', '.join(rec['technologies'])}")
        
        print(f"\n🏗️  ARQUITETURA:")
        arch = result.get('architecture_suggestions', {})
        for key, value in arch.items():
            print(f"  • {key}: {value}")
        
        print(f"\n🔄 FLUXO DE DADOS:")
        for flow in result.get('data_flow', []):
            print(f"  • {flow}")
        
        print(f"\n⚠️  CONSIDERAÇÕES:")
        for consideration in result.get('considerations', []):
            print(f"  • {consideration}")
        
        print(f"\n🤖 ANÁLISE DA IA:")
        print("=" * 60)
        ai_analysis = result.get('ai_analysis', 'Nenhuma análise de IA retornada')
        
        # Verificar se é análise da OpenAI ou simulação
        if "OPENAI GPT-4o MINI" in ai_analysis:
            print("🔮 Modo: OpenAI GPT-4o Mini")
        elif "MODO SIMULAÇÃO" in ai_analysis:
            print("🔧 Modo: Simulação Inteligente")
        
        # Mostrar análise completa (ou truncada se muito longa)
        if len(ai_analysis) > 1000:
            print(ai_analysis[:800] + "\n\n... [continuação truncada para visualização] ...\n" + ai_analysis[-200:])
        else:
            print(ai_analysis)
        
        # Informações adicionais
        print(f"\n📋 MÉTRICAS:")
        print(f"  • Sucesso: {result.get('success', False)}")
        print(f"  • Tipo do Agente: {result.get('agent_type', 'N/A')}")
        
    else:
        print(f"❌ Erro: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("❌ Não foi possível conectar ao servidor. Certifique-se de que o Database Agent está rodando.")
    print("   💡 Execute: python database_agent.py")
    
except Exception as e:
    print(f"❌ Erro na requisição: {e}")