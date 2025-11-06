from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify
import logging
import json
from typing import Dict, Any, List
from provider import DatabaseProvider, DatabasePatterns, AIDatabaseAdvisor

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class DatabaseProvider:
    def __init__(self):
        self.orchestrator_url = "http://localhost:3000"
    
    def validate_project_data(self, data: Dict[str, Any]) -> bool:
        """Valida dados básicos do projeto"""
        required_fields = ["project_name", "project_description", "requirements"]
        return all(field in data for field in required_fields)
    
    def get_database_recommendations(self, requirements: Dict[str, Any]) -> List[str]:
        """Gera recomendações baseadas nos requisitos"""
        recommendations = []
        
        # Analisar volume de dados
        data_volume = requirements.get("data_volume", "small")
        if data_volume == "large":
            recommendations.append("Considere usar sharding ou partitioning")
        
        # Analisar consistência
        consistency_requirements = requirements.get("consistency", "eventual")
        if consistency_requirements == "strong":
            recommendations.append("Priorize bancos relacionais para consistência forte")
        
        return recommendations

class DatabasePatterns:
    """Padrões de banco de dados comuns"""
    
    @staticmethod
    def get_relational_pattern():
        return {
            "type": "relational",
            "description": "Para dados estruturados com relacionamentos complexos",
            "examples": ["PostgreSQL", "MySQL", "SQL Server"],
            "use_cases": ["Sistemas transacionais", "Dados com ACID", "Relacionamentos complexos"]
        }
    
    @staticmethod
    def get_document_pattern():
        return {
            "type": "document",
            "description": "Para dados semi-estruturados em formato de documentos",
            "examples": ["MongoDB", "Couchbase", "Firestore"],
            "use_cases": ["Catálogos de produtos", "Conteúdo gerado por usuários", "Dados hierárquicos"]
        }
    
    @staticmethod
    def get_key_value_pattern():
        return {
            "type": "key_value",
            "description": "Para acesso rápido via chave",
            "examples": ["Redis", "DynamoDB", "Memcached"],
            "use_cases": ["Cache", "Sessões de usuário", "Configurações"]
        }

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        "status": "healthy", 
        "agent": "database_agent",
        "framework": "flask"
    })

@app.route('/analyze-database', methods=['POST'])
def analyze_database():
    """
    Endpoint principal para análise de banco de dados
    """
    try:
        # Obter dados da requisição
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "Dados JSON necessários"}), 400
        
        # Validar dados
        provider = DatabaseProvider()
        if not provider.validate_project_data(data):
            return jsonify({"success": False, "error": "Dados do projeto inválidos"}), 400
        
        # 🔥 NOVO: Obter recomendação de IA
        ai_advisor = AIDatabaseAdvisor()
        ai_recommendation = ai_advisor.get_ai_recommendation(data)
        
        # Gerar recomendações tradicionais
        recommendations = _generate_database_recommendations(data)
        
        # Gerar sugestões de arquitetura
        architecture_suggestions = _generate_architecture_suggestions(data, recommendations)
        
        # Definir fluxo de dados
        data_flow = _define_data_flow(data.get('requirements', {}))
        
        # Considerações importantes
        considerations = _generate_considerations(data)
        
        response = {
            "success": True,
            "recommendations": recommendations,
            "architecture_suggestions": architecture_suggestions,
            "data_flow": data_flow,
            "considerations": considerations,
            "ai_analysis": ai_recommendation,  # 🔥 NOVO campo
            "agent_type": "database_agent"
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Erro no agente de banco de dados: {e}")
        return jsonify({"success": False, "error": f"Erro interno: {str(e)}"}), 500

def _generate_database_recommendations(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Gera recomendações de banco de dados baseadas nos requisitos"""
    recommendations = []
    requirements = data.get('requirements', {})
    
    # Análise baseada no tipo de dados
    data_type = requirements.get("data_type", "mixed")
    scalability = requirements.get("scalability", "medium")
    consistency = requirements.get("consistency", "eventual")
    
    # Recomendação principal baseada no tipo de dados
    if data_type in ["structured", "transactional"]:
        recommendations.append({
            "database_type": "Relacional",
            "recommendation": "Use banco de dados relacional para consistência ACID",
            "justification": "Dados estruturados com relacionamentos complexos exigem transações ACID",
            "confidence_score": 0.9,
            "technologies": ["PostgreSQL", "MySQL", "SQL Server"],
            "patterns": [DatabasePatterns.get_relational_pattern()]
        })
    
    if data_type in ["document", "semi-structured"]:
        recommendations.append({
            "database_type": "Document",
            "recommendation": "Banco de dados de documentos para flexibilidade de schema",
            "justification": "Dados semi-estruturados se beneficiam de schemas flexíveis",
            "confidence_score": 0.8,
            "technologies": ["MongoDB", "Couchbase", "Firestore"],
            "patterns": [DatabasePatterns.get_document_pattern()]
        })
    
    # Recomendação para cache se necessário
    if requirements.get("high_read_throughput", False):
        recommendations.append({
            "database_type": "Key-Value",
            "recommendation": "Implemente cache com banco chave-valor",
            "justification": "Alta taxa de leitura beneficia-se de cache em memória",
            "confidence_score": 0.7,
            "technologies": ["Redis", "Memcached", "DynamoDB"],
            "patterns": [DatabasePatterns.get_key_value_pattern()]
        })
    
    return recommendations

def _generate_architecture_suggestions(data: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Gera sugestões de arquitetura baseadas nas recomendações"""
    primary_db = next((rec for rec in recommendations if rec["database_type"] != "Key-Value"), None)
    
    return {
        "primary_database": primary_db["database_type"] if primary_db else "Relacional",
        "caching_strategy": "Redis" if any(rec["database_type"] == "Key-Value" for rec in recommendations) else "None",
        "replication": "Ativar" if data.get('requirements', {}).get("high_availability", False) else "Opcional",
        "backup_strategy": "Automático diário",
        "migration_approach": "Versionamento de schema"
    }

def _define_data_flow(requirements: Dict[str, Any]) -> List[str]:
    """Define o fluxo de dados recomendado"""
    flow = ["Client Request → API Gateway → Business Logic"]
    
    if requirements.get("high_read_throughput", False):
        flow.append("Business Logic → Cache Layer → Database")
        flow.append("Cache Miss → Database → Update Cache")
    else:
        flow.append("Business Logic → Database")
    
    flow.append("Database → Response → Client")
    return flow

def _generate_considerations(data: Dict[str, Any]) -> List[str]:
    """Gera considerações importantes"""
    considerations = []
    requirements = data.get('requirements', {})
    
    if requirements.get("data_volume") == "large":
        considerations.append("Considere partitioning ou sharding para grandes volumes")
    
    if requirements.get("compliance_requirements"):
        considerations.append("Verifique requisitos de compliance (GDPR, LGPD, etc.)")
    
    if requirements.get("real_time_analytics"):
        considerations.append("Considere database separado para analytics (OLAP)")
    
    considerations.append("Implemente backup e recovery procedures")
    considerations.append("Monitore performance e configure alertas")
    
    return considerations

if __name__ == '__main__':
    logger.info("🚀 Iniciando Database Agent com Flask...")
    app.run(
        host='0.0.0.0',
        port=8004,
        debug=True
    )