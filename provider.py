import requests
import logging
from typing import Dict, Any
import google.generativeai as genai
import os
import json

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

class AIDatabaseAdvisor:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.use_real_ai = False
        self.real_ai_model = None
        
        # Tentar configurar IA real se tiver chave
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.real_ai_model = genai.GenerativeModel('models/gemini-2.0-flash-001')
                self.use_real_ai = True
                print("✅ IA Real (Gemini) configurada com sucesso!")
            except Exception as e:
                print(f"⚠️  IA Real não disponível: {e}. Usando modo simulação.")
        else:
            print("✅ Modo simulação ativado (configure GEMINI_API_KEY para IA real)")
    
    def get_ai_recommendation(self, project_data: Dict[str, Any]) -> str:
        """Fornece análise de IA - real se disponível, simulada caso contrário"""
        
        if self.use_real_ai and self.real_ai_model:
            return self._get_real_ai_recommendation(project_data)
        else:
            return self._get_simulated_ai_recommendation(project_data)
    
    def _get_real_ai_recommendation(self, project_data: Dict[str, Any]) -> str:
        """Usa Gemini API para análise real"""
        try:
            prompt = f"""
            Como arquiteto de banco de dados sênior, analise:

            PROJETO: {project_data.get('project_name')}
            DESCRIÇÃO: {project_data.get('project_description')}
            REQUISITOS: {json.dumps(project_data.get('requirements', {}), indent=2)}

            Forneça recomendações técnicas detalhadas sobre arquitetura de banco de dados.
            """
            
            response = self.real_ai_model.generate_content(prompt)
            return f"🤖 ANÁLISE GEMINI AI:\n\n{response.text}"
            
        except Exception as e:
            # Se der erro na IA real, cai para simulação
            print(f"❌ Erro na IA real: {e}. Usando simulação.")
            return self._get_simulated_ai_recommendation(project_data)
    
    def _get_simulated_ai_recommendation(self, project_data: Dict[str, Any]) -> str:
        """Análise simulada inteligente baseada em regras"""
        
        req = project_data.get('requirements', {})
        project_name = project_data.get('project_name', 'Projeto')
        
        # Análise inteligente baseada em múltiplos fatores
        recommendations = self._analyze_requirements(req)
        
        return f"""
🤖 ANÁLISE DE ARQUITETURA DE BANCO DE DADOS

📊 PROJETO: {project_name}
📝 DESCRIÇÃO: {project_data.get('project_description', 'Não fornecida')}

🎯 RECOMENDAÇÃO PRINCIPAL:
{recommendations['primary']}

🏗️ ARQUITETURA DETALHADA:
{recommendations['architecture']}

⚡ ESTRATÉGIAS DE PERFORMANCE:
{recommendations['performance']}

🔒 CONSIDERAÇÕES DE SEGURANÇA:
{recommendations['security']}

📈 PLANO DE ESCALABILIDADE:
{recommendations['scalability']}

💡 PRÓXIMOS PASSOS:
{recommendations['next_steps']}

---
🔧 MODO: Simulação (Configure GEMINI_API_KEY para análise com IA real)
"""
    
    def _analyze_requirements(self, requirements: Dict[str, Any]) -> Dict[str, str]:
        """Analisa requisitos e gera recomendações inteligentes"""
        
        # Lógica de recomendação baseada em múltiplos fatores
        data_type = requirements.get('data_type', 'mixed')
        scalability = requirements.get('scalability', 'medium')
        consistency = requirements.get('consistency', 'eventual')
        read_throughput = requirements.get('high_read_throughput', False)
        write_throughput = requirements.get('high_write_throughput', False)
        real_time = requirements.get('real_time', False)
        data_volume = requirements.get('data_volume', 'small')
        
        # Determinar arquitetura principal
        if data_type == 'structured' and consistency == 'strong':
            primary_db = "PostgreSQL"
            primary_reason = "Dados estruturados com necessidade de transações ACID"
        elif data_type == 'document':
            primary_db = "MongoDB" 
            primary_reason = "Dados semi-estruturados com flexibilidade de schema"
        elif real_time and read_throughput:
            primary_db = "PostgreSQL + Redis"
            primary_reason = "Combinação de consistência forte com performance em tempo real"
        else:
            primary_db = "PostgreSQL"
            primary_reason = "Banco versátil para maioria dos casos de uso"
        
        # Estratégia de cache
        cache_strategy = "Redis para cache e sessões" if read_throughput else "Cache em aplicação"
        
        # Estratégia de escalabilidade
        if scalability == 'high':
            scale_strategy = "Sharding horizontal + Replicação de leitura"
        elif scalability == 'very_high':
            scale_strategy = "Arquitetura multi-região com failover automático"
        else:
            scale_strategy = "Replicação síncrona para alta disponibilidade"
        
        return {
            'primary': f"{primary_db} - {primary_reason}",
            'architecture': f"""
• Banco Primário: {primary_db}
• Cache: {cache_strategy}
• Replicação: {'Ativa' if requirements.get('high_availability') else 'Opcional'}
• Backup: Estratégia automática com retenção de 30 dias
            """,
            'performance': f"""
• Leitura: {'Cache distribuído + Read replicas' if read_throughput else 'Otimizações de query'}
• Escrita: {'Write-ahead logging + Batch operations' if write_throughput else 'Transações otimizadas'}
• Latência: {'Sub-milisegundo com cache' if real_time else 'Otimizações padrão'}
            """,
            'security': """
• Criptografia: Dados em repouso e em trânsito
• Autenticação: Mecanismo nativo do banco
• Audit: Log de todas as operações sensíveis
• Backup: Criptografado e off-site
            """,
            'scalability': f"""
• Estratégia: {scale_strategy}
• Monitoramento: Métricas em tempo real
• Auto-scaling: {'Configurado' if scalability in ['high', 'very_high'] else 'Manual'}
• Particionamento: {'Por data/região' if data_volume == 'large' else 'Não necessário inicialmente'}
            """,
            'next_steps': """
1. Prototipar com banco local
2. Definir schema inicial
3. Configurar ambiente de desenvolvimento  
4. Implementar estratégia de migração
5. Estabelecer métricas de monitoramento
            """
        }