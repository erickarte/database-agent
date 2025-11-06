# 🗂️ Database Agent - Orquestrador BMAD

Agente especializado em recomendações de arquitetura de banco de dados com integração de IA para o Orquestrador BMAD.

## 🚀 Funcionalidades

- ✅ Análise automática de requisitos para banco de dados
- ✅ Recomendações técnicas detalhadas com IA Gemini
- ✅ Modo simulação inteligente (fallback sem API)
- ✅ Sugestões de arquitetura e fluxo de dados
- ✅ Considerações de performance e escalabilidade
- ✅ Integração via API REST

## 🏗️ Arquitetura

- **Framework**: Flask (Python)
- **IA Integration**: Google Gemini API + Modo Simulação
- **API**: RESTful JSON
- **Porta**: 8004

## 📋 Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## 🛠️ Instalação

```bash
# Clonar repositório
git clone https://github.com/erickarte/database-agent-bmad.git
cd database-agent-bmad

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt