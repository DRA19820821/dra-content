# 🚀 Marketing AI System

> **Versão 1.0.1** | Usando as versões mais recentes de LangGraph 1.0.3, Claude Sonnet 4.5, GPT-5 e Gemini 2.5 Plus (Nov 2025)

Sistema inteligente de geração de conteúdos de marketing digital para produtos Hotmart, utilizando **LangGraph** e múltiplos provedores de LLM com sistema de criação-revisão iterativo.

## 📋 Visão Geral

> **⚡ ATUALIZADO**: Este projeto usa as **versões mais recentes** de todos os pacotes e modelos disponíveis em Novembro 2025. Veja [UPDATE_NOTES.md](UPDATE_NOTES.md) para detalhes completos das atualizações.

O Marketing AI System automatiza a criação de conteúdos persuasivos para produtos educacionais, implementando um fluxo de trabalho com agentes de IA que criam, revisam e refinam os conteúdos até atingirem qualidade superior (nota ≥ 8/10).

### 🎯 Conteúdos Gerados

1. **Tipo de Material** - Classificação automática (Baralhos Anki, Mapas Mentais, Músicas, Podcasts)
2. **Descrição Hotmart** - Texto atrativo até 1.800 caracteres
3. **Artigo Blog** - HTML completo com narrativa de venda
4. **Legenda Instagram** - Texto curto e envolvente
5. **Imagem Vertical** - 1080x1920px (stories/reels)
6. **Imagem Quadrada** - 1080x1080px (feed)
7. **Nome Criativo** - Máximo 5 palavras impactantes
8. **Descrição Página de Vendas** - Máximo 25 palavras
9. **Item Extra** - Customizável conforme necessidade

## 🏗️ Arquitetura

### Stack Tecnológica

- **Backend**: FastAPI + Python 3.11+
- **Agentes**: LangGraph 1.0.3 para orquestração de IA
- **Frontend**: HTML5 + CSS3 + JavaScript (Vanilla)
- **Validação**: Pydantic para resposta estruturada
- **Real-time**: WebSocket para logs ao vivo

### Provedores de LLM Suportados

**Para Texto:**
- Anthropic (Claude Sonnet 4.5) ✅ Recomendado
- OpenAI (GPT-5)
- Google (Gemini 2.5 Plus)
- DeepSeek (v3)
- Grok (2.0)
- Qwen (QwQ-32B-Preview)

**Para Imagens:**
- OpenAI (GPT Image 1) ✅ Recomendado
- Google (Imagen 3 - Nano Banana)

### Fluxo de Agentes (LangGraph)

```
┌─────────────┐
│   Início    │
└──────┬──────┘
       │
       v
┌──────────────────┐
│ Agente Criador   │ ← Gera conteúdos estruturados
│ (LLM com         │   usando Pydantic
│  Pydantic)       │
└──────┬───────────┘
       │
       v
┌──────────────────┐
│ Agente Revisor   │ ← Avalia qualidade (0-10)
│ (Critérios       │   • Clareza (2pts)
│  Claros)         │   • Persuasão (2pts)
└──────┬───────────┘   • Criatividade (2pts)
       │               • Adequação (2pts)
       v               • Conversão (2pts)
    [nota >= 8?]
       │
   ┌───┴───┐
   │ Sim   │ Não
   │       └──> [iteração < max?]
   │                │
   v            ┌───┴───┐
[Salvar]        │ Sim   │ Não
                │       │
                v       v
         [Refinar com  [Salvar com
          feedback]    flag pendente]
```

## 🚀 Instalação

### 1. Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Contas e API keys dos provedores desejados

### 2. Clonar e Instalar

```bash
# Clone o repositório
cd marketing-ai-system

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar API Keys

```bash
# Copiar template de variáveis de ambiente
cp .env.example .env

# Editar .env e adicionar suas API keys
# Exemplo:
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AI...
```

### 4. Executar

```bash
# Iniciar servidor
python app.py

# Ou com uvicorn diretamente
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Acesse: **http://localhost:8000**

## 📖 Como Usar

### Interface Web

1. **Selecione os Provedores**
   - Escolha o LLM para geração de texto
   - Escolha o provedor para geração de imagens

2. **Preencha os Dados do Produto**
   - **Radical**: Identificador alfanumérico (ex: `dAdm`, `dConst`)
   - **Insumos**: Informações base do produto
   - **Iterações Máximas**: Número de ciclos de melhoria (1-10)

3. **Selecione Conteúdos**
   - Marque/desmarque os checkboxes conforme necessário
   - Para "Item Extra", ative e descreva o que deseja

4. **Gerar**
   - Clique em "Gerar Conteúdos"
   - Acompanhe o progresso em tempo real nos logs
   - Visualize os resultados nas diferentes abas

5. **Download**
   - Baixe o JSON com todos os conteúdos
   - Baixe as imagens geradas individualmente

## 📂 Estrutura de Arquivos

```
marketing-ai-system/
├── app.py                 # Backend FastAPI
├── agents.py              # Sistema de agentes LangGraph
├── models.py              # Modelos Pydantic
├── requirements.txt       # Dependências
├── .env.example          # Template de configuração
├── README.md             # Documentação
│
├── templates/
│   └── index.html        # Interface principal
│
├── static/
│   ├── style.css         # Estilos modernos
│   └── script.js         # Lógica frontend + WebSocket
│
└── outputs/              # Resultados gerados
    └── YYYYMMDD_HHMMSS_ID/
        ├── conteudo.json
        └── imagens/
            ├── *_Vert_*.png
            └── *_Quad_*.png
```

## 🔧 Configurações Avançadas

### Customizar Prompts dos Agentes

Edite o arquivo `agents.py`:

```python
def _construir_prompt_criador(self, state: AgentState) -> str:
    """Personalize o prompt do agente criador aqui"""
    
def _construir_prompt_revisor(self, conteudo: ConteudoGerado, config: ConfigGerador) -> str:
    """Personalize os critérios de avaliação aqui"""
```

### Adicionar Novos Provedores de LLM

No método `_get_llm` em `agents.py`:

```python
elif provider == "novo_provider":
    return ChatOpenAI(
        base_url="https://api.novo-provider.com",
        model="modelo-especifico",
        api_key=os.getenv("NOVO_PROVIDER_API_KEY")
    )
```

### Ajustar Critérios de Qualidade

Modifique a nota mínima de aprovação:

```python
# Em agents.py, método deve_continuar
if avaliacao and avaliacao.nota >= 8:  # Altere este valor
    return "finalizar"
```

## 📊 Formato de Saída (JSON)

```json
{
  "data_geracao": "2025-11-10 20:30:00",
  "id_conteudos": "a1b2c3d4e5",
  "tipo_material": "Mapas Mentais",
  "desc_hotmart": "Descrição completa...",
  "artigo": "<article>...</article>",
  "legenda": "Legenda do Instagram...",
  "nome_imagem_vert": "dAdm_MapasMentais_Vert_20251110.png",
  "nome_imagem_quad": "dAdm_MapasMentais_Quad_20251110.png",
  "nome_criativo": "Mapas que Aprovam",
  "desc_pv": "Descrição página de vendas...",
  "extra": null,
  "nota_conteudo": 8.6,
  "iteracoes_realizadas": 2,
  "qualidade_pendente": false
}
```

## 🎨 Personalização da Interface

### Cores e Tema

Edite `static/style.css`, seção `:root`:

```css
:root {
    --primary: #6366f1;      /* Cor principal */
    --success: #10b981;      /* Verde de sucesso */
    --error: #ef4444;        /* Vermelho de erro */
    /* ... outras variáveis ... */
}
```

## 🐛 Troubleshooting

### Erro de Conexão WebSocket

- Verifique se o servidor está rodando
- Certifique-se que não há firewall bloqueando
- Recarregue a página

### Erro "API Key não encontrada"

- Verifique se o arquivo `.env` existe
- Confirme que as keys estão corretas
- Reinicie o servidor após alterar `.env`

### Geração de Imagens Falha

- Verifique se a API key do OpenAI está configurada
- Confirme que você tem créditos suficientes
- Tente desmarcar a geração de imagens para testar apenas texto

### Nota sempre baixa (< 8)

- Forneça insumos mais detalhados e estruturados
- Aumente o número máximo de iterações
- Experimente outro provedor de LLM

## 📝 Exemplos de Uso

### Exemplo 1: Baralhos Anki para Direito Administrativo

**Radical**: `dAdm`

**Insumos**:
```
Baralhos Anki de Direito Administrativo para concursos públicos.
Contém 500+ flashcards com questões de provas anteriores.
Metodologia de repetição espaçada científica.
Público: concurseiros que buscam memorização eficiente.
Diferenciais: Questões comentadas, estatísticas de desempenho, app mobile.
```

### Exemplo 2: Mapas Mentais para OAB

**Radical**: `dOAB`

**Insumos**:
```
Mapas Mentais completos para todas as matérias da OAB.
Design colorido e visual para facilitar memorização.
Segue edital atualizado 2025.
Público: estudantes de Direito que preferem aprendizado visual.
Formato: PDF de alta qualidade + versão para impressão.
```

## 🤝 Contribuindo

Sugestões de melhorias:

1. **Multi-idioma**: Adicionar suporte para outros idiomas
2. **Templates**: Sistema de templates por nicho
3. **Histórico**: Salvar histórico de gerações
4. **A/B Testing**: Gerar múltiplas versões para teste
5. **Integração**: Publicar diretamente em plataformas

## 📄 Licença

Este projeto está sob licença MIT. Veja arquivo LICENSE para mais detalhes.

## 👨‍💻 Autor

**Academia do Raciocínio**
- Website: [academiadoraciocinio.com.br](https://academiadoraciocinio.com.br)
- Especializado em materiais educacionais para concursos públicos

## 🙏 Agradecimentos

- LangChain/LangGraph pela framework de agentes
- Anthropic, OpenAI, Google pela API de LLM
- Comunidade open-source

---

**Versão**: 1.0.0  
**Data**: Novembro 2025  
**Status**: ✅ Produção
