import requests
import logging
from typing import Dict, Any
import openai
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
        # DEBUG: Mostrar o que está acontecendo
        print(f"\n🔍 DEBUG AIDatabaseAdvisor.__init__()")
        print(f"   api_key passada: {'✅ SIM' if api_key else '❌ NÃO'}")
        
        # Carregar do .env se não foi passada
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        print(f"   self.api_key final: {'✅ SIM (tem chave)' if self.api_key else '❌ NÃO (sem chave)'}")
        
        if self.api_key:
            print(f"   Comprimento da chave: {len(self.api_key)} caracteres")
            # Mostrar início e fim (mascarado)
            if len(self.api_key) > 8:
                print(f"   Chave (mascarada): {self.api_key[:8]}...{self.api_key[-4:]}")
        
        self.use_real_ai = False
        
        # Tentar configurar OpenAI se tiver chave
        if self.api_key:
            try:
                print("   🚀 Tentando configurar OpenAI...")
                openai.api_key = self.api_key
                # Testar a conexão com uma requisição simples
                self._test_openai_connection()
                self.use_real_ai = True
                print("   ✅ OpenAI GPT-4o Mini configurado com sucesso!")
            except Exception as e:
                print(f"   ⚠️  OpenAI não disponível: {e}")
                self.use_real_ai = False
        else:
            print("   ✅ Modo simulação ativado (sem chave OpenAI)")
    
    def _test_openai_connection(self):
        """Testa a conexão com a OpenAI"""
        try:
            print("   🧪 Testando conexão com OpenAI...")
            # Requisição de teste leve
            test_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            print(f"   ✅ Conexão OpenAI OK: {test_response.choices[0].message.content}")
            # ⚠️ NÃO retorne nada aqui
        except openai.AuthenticationError as e:
            print(f"   ❌ Erro de autenticação OpenAI: {e}")
            raise Exception(f"Falha na autenticação: {e}")
        except Exception as e:
            print(f"   ❌ Outro erro OpenAI: {e}")
            raise Exception(f"Falha ao conectar com OpenAI: {e}")
    
    def get_ai_recommendation(self, project_data: Dict[str, Any]) -> str:
        """Fornece análise de IA - OpenAI se disponível, simulada caso contrário"""
        
        if self.use_real_ai:
            return self._get_openai_recommendation(project_data)
        else:
            return self._get_simulated_ai_recommendation(project_data)
    
    def _get_openai_recommendation(self, project_data: Dict[str, Any]) -> str:
        """Usa OpenAI GPT-4o Mini para análise real"""
        
        try:
            prompt = f"""
            Como arquiteto de banco de dados sênior com 15 anos de experiência, analise este projeto em detalhes:

            **PROJETO**: {project_data.get('project_name', 'Não especificado')}
            **DESCRIÇÃO**: {project_data.get('project_description', 'Não fornecida')}
            **REQUISITOS TÉCNICOS**: {json.dumps(project_data.get('requirements', {}), indent=2)}

            Forneça uma análise técnica completa e acionável cobrindo:

            ## 1. ARQUITETURA RECOMENDADA
            - Abordagem principal (Relacional, NoSQL, Híbrida, Poliglota)
            - Justificativa técnica para a escolha

            ## 2. TECNOLOGIAS ESPECÍFICAS  
            - Bancos de dados recomendados (com versões específicas se aplicável)
            - Ferramentas complementares (cache, ORM, migrações)

            ## 3. PADRÕES ARQUITETURAIS
            - Padrões de design a implementar
            - Estratégia de replicação e sharding
            - Considerações de consistência

            ## 4. PLANO DE ESCALABILIDADE
            - Como escalar verticalmente e horizontalmente
            - Pontos de atenção em alto volume
            - Estratégia de backup e recovery

            ## 5. ANÁLISE DE RISCOS
            - Possíveis problemas e mitigação
            - Custos envolvidos
            - Curva de aprendizado da equipe

            Seja extremamente técnico, prático e específico. Inclua nomes de tecnologias concretas.
            Formate a resposta de forma clara com tópicos e bullet points.
            """
            
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "Você é um arquiteto de banco de dados sênior especializado em recomendações técnicas. Seja detalhado, específico e prático."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7,
                top_p=0.9
            )
            
            analysis = response.choices[0].message.content
            return f"🤖 ANÁLISE OPENAI GPT-4o MINI:\n\n{analysis}"
        
        except openai.AuthenticationError:
            error_msg = "❌ Erro de autenticação OpenAI. Verifique sua API_KEY no arquivo .env"
            print(error_msg)
            return f"{error_msg}\n\nUsando modo simulação:\n{self._get_simulated_ai_recommendation(project_data)}"
        
        except openai.RateLimitError:
            error_msg = "⚠️  Limite de taxa excedido na OpenAI. Usando modo simulação."
            print(error_msg)
            return self._get_simulated_ai_recommendation(project_data)
        
        except Exception as e:
            error_msg = f"❌ Erro na OpenAI: {str(e)[:100]}... Usando modo simulação."
            print(error_msg)
            return self._get_simulated_ai_recommendation(project_data)
    
    def _get_simulated_ai_recommendation(self, project_data: Dict[str, Any]) -> str:
        """Análise simulada inteligente baseada em regras"""
        
        req = project_data.get('requirements', {})
        project_name = project_data.get('project_name', 'Projeto')
        
        # Análise inteligente baseada em múltiplos fatores
        recommendations = self._analyze_requirements(req)
        
        return f"""
🤖 ANÁLISE DE ARQUITETURA DE BANCO DE DADOS (MODO SIMULAÇÃO)

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
🔧 MODO: Simulação (Configure OPENAI_API_KEY no arquivo .env para análise com IA real)
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
        high_availability = requirements.get('high_availability', False)
        
        # Determinar arquitetura principal
        if data_type == 'structured' and consistency == 'strong':
            primary_db = "PostgreSQL 15+"
            primary_reason = "Dados estruturados com necessidade de transações ACID e consistência forte"
        elif data_type == 'document':
            primary_db = "MongoDB 7.0+"
            primary_reason = "Dados semi-estruturados com flexibilidade de schema e alta escalabilidade"
        elif real_time and read_throughput:
            primary_db = "PostgreSQL + Redis"
            primary_reason = "Combinação de consistência forte (PostgreSQL) com performance em tempo real (Redis)"
        elif data_volume == 'massive' and write_throughput:
            primary_db = "Cassandra ou ScyllaDB"
            primary_reason = "Otimizado para escrita massiva e alta disponibilidade"
        else:
            primary_db = "PostgreSQL"
            primary_reason = "Banco versátil e robusto para maioria dos casos de uso"
        
        # Estratégia de cache
        if read_throughput:
            cache_strategy = "Redis Cluster para cache distribuído e sessões"
        elif real_time:
            cache_strategy = "Redis para cache em memória com pub/sub"
        else:
            cache_strategy = "Cache em aplicação com expiração controlada"
        
        # Estratégia de escalabilidade
        if scalability == 'very_high':
            scale_strategy = "Arquitetura multi-região com sharding automático e failover"
        elif scalability == 'high':
            scale_strategy = "Sharding horizontal + Read replicas + Load balancing"
        elif high_availability:
            scale_strategy = "Replicação síncrona com auto-failover"
        else:
            scale_strategy = "Replicação assíncrona para backup e recuperação"
        
        # Estratégia de backup
        if data_volume in ['large', 'massive']:
            backup_strategy = "Backup incremental + Snapshots + Replicação cross-region"
        elif high_availability:
            backup_strategy = "Backup contínuo com ponto de recuperação (PITR)"
        else:
            backup_strategy = "Backup diário completo + logs de transação"
        
        return {
            'primary': f"{primary_db}\n📋 {primary_reason}",
            'architecture': f"""
• Banco Primário: {primary_db}
• Cache: {cache_strategy}
• Replicação: {'Ativa com auto-failover' if high_availability else 'Opcional'}
• Backup: {backup_strategy}
• Monitoramento: Prometheus + Grafana para métricas em tempo real
            """,
            'performance': f"""
• Leitura: {'Cache distribuído + Read replicas + Query optimization' if read_throughput else 'Indexação adequada + Query tuning'}
• Escrita: {'Batch operations + Async processing' if write_throughput else 'Transações otimizadas'}
• Latência: {'Sub-milisegundo com cache Redis' if real_time else 'Otimizações padrão (<100ms)'}
• Throughput: {'Horizontal scaling' if scalability in ['high', 'very_high'] else 'Vertical scaling'}
            """,
            'security': """
• Criptografia: AES-256 em repouso, TLS 1.3 em trânsito
• Autenticação: JWT + OAuth2 + MFA (Multi-Factor Authentication)
• Autorização: RBAC (Role-Based Access Control) granular
• Audit: Log completo de todas as operações com retenção de 1 ano
• Compliance: GDPR, LGPD, HIPAA (conforme necessário)
            """,
            'scalability': f"""
• Estratégia: {scale_strategy}
• Monitoramento: Métricas customizadas + Alertas proativos
• Auto-scaling: {'Configurado com thresholds dinâmicos' if scalability in ['high', 'very_high'] else 'Manual com monitoramento'}
• Particionamento: {'Por tenant/data/região' if data_volume in ['large', 'massive'] else 'Não necessário inicialmente'}
• Capacity Planning: Previsão baseada em growth metrics
            """,
            'next_steps': """
1. ✅ Prototipar com banco local (Docker Compose)
2. ✅ Definir schema inicial com versionamento (Liquibase/Flyway)
3. ✅ Configurar ambiente de dev/test/prod
4. ✅ Implementar estratégia de migração (blue-green deployment)
5. ✅ Estabelecer métricas de monitoramento (SLIs/SLOs)
6. ✅ Documentar procedures de backup/recovery
7. ✅ Planejar disaster recovery multi-region
            """
        }