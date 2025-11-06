import google.generativeai as genai
import os

# Use variável de ambiente: set GEMINI_API_KEY=sua_chave_aqui
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY não configurada.")
    print("💡 Execute: set GEMINI_API_KEY=sua_chave_aqui")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

print("🔍 Listando modelos disponíveis na sua conta Gemini...")
print("=" * 60)

try:
    models = list(genai.list_models())
    
    print(f"📊 Total de modelos encontrados: {len(models)}")
    print("\n✅ MODELOS COMPATIVEIS COM generateContent:")
    print("-" * 50)
    
    compatible_models = []
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            compatible_models.append(model.name)
            print(f"🎯 {model.name}")
            print(f"   Descrição: {model.description}")
            print(f"   Métodos: {model.supported_generation_methods}")
            print()
    
    print(f"\n📋 RESUMO: {len(compatible_models)} modelos compatíveis")
    for i, model_name in enumerate(compatible_models, 1):
        print(f"   {i}. {model_name}")
        
    if compatible_models:
        print(f"\n💡 SUGESTÃO: Use este modelo -> '{compatible_models[0]}'")
        
except Exception as e:
    print(f"❌ Erro ao listar modelos: {e}")