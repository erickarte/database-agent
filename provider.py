import requests
import logging
from typing import Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseProvider:
    def __init__(self):
        self.orchestrator_url = "http://localhost:3000"
    
    def call_orchestrator(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Faz chamada para o orquestrador"""
        try:
            response = requests.post(
                f"{self.orchestrator_url}/{endpoint}",
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao chamar orquestrador: {e}")
            return {"error": str(e)}
    
    def validate_project_data(self, data: Dict[str, Any]) -> bool:
        """Valida dados básicos do projeto"""
        required_fields = ["project_name", "project_description", "requirements"]
        return all(field in data for field in required_fields)
    
    def get_database_recommendations(self, requirements: Dict[str, Any]) -> list:
        """Gera recomendações baseadas nos requisitos"""
        recommendations = []
        
        data_volume = requirements.get("data_volume", "small")
        if data_volume == "large":
            recommendations.append("Considere usar sharding ou partitioning")
        
        consistency_requirements = requirements.get("consistency", "eventual")
        if consistency_requirements == "strong":
            recommendations.append("Priorize bancos relacionais para consistência forte")
        
        return recommendations