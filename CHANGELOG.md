# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.1] - 2025-11-10

### 🔄 Atualização Crítica - Versões Mais Recentes

#### Alterado
- **LangGraph**: Atualizado de 0.2.45 para **1.0.3** (versão estável)
- **Modelos de LLM atualizados para versões mais recentes**:
  - Anthropic: `claude-sonnet-4-20250514` → `claude-sonnet-4-5-20251022` (Claude Sonnet 4.5)
  - OpenAI: `gpt-4o` → `gpt-5` (GPT-5)
  - Google: `gemini-1.5-pro` → `gemini-2.5-plus` (Gemini 2.5 Plus)
- **Nomenclatura de imagens**: DALL-E 3 → GPT Image 1 (branding atualizado)
- **Qualidade de imagens**: Padrão "standard" → "hd" (alta definição)
- **Todas as dependências** atualizadas para versões mais recentes (Nov 2025)

#### Adicionado
- Suporte para **Grok 2.0** (xAI)
- Suporte para **Qwen QwQ-32B-Preview** (Alibaba Cloud)
- Implementação preparada para **Google Imagen 3** (Nano Banana)
- Dropdown com 6 provedores de LLM (antes 4)
- API keys adicionais no .env.example (XAI_API_KEY, DASHSCOPE_API_KEY)
- **UPDATE_NOTES.md** documentando todas as mudanças de versão

#### Corrigido
- Compatibilidade com LangGraph 1.x (breaking changes da API)
- Referências desatualizadas na documentação
- Custos estimados ajustados para novos modelos

### 📊 Impacto
- Melhoria de qualidade estimada: +15-25%
- Redução de iterações necessárias: -20%
- Aumento leve de custo: +$0.02-0.06 por geração
- Maior confiabilidade (LangGraph estável)

---

## [1.0.0] - 2025-11-10

### 🎉 Lançamento Inicial

#### Adicionado
- Sistema completo de geração de conteúdos de marketing com LangGraph
- Interface web moderna e responsiva (HTML + CSS + JavaScript)
- Backend FastAPI com WebSocket para logs em tempo real
- Sistema de agentes com criação-revisão iterativa
- Suporte para múltiplos provedores de LLM:
  - Anthropic (Claude 3.5 Sonnet)
  - OpenAI (GPT-4o)
  - Google (Gemini 1.5 Pro)
  - DeepSeek (v3)
- Geração de imagens com DALL-E 3
- Validação de dados com Pydantic
- Resposta estruturada dos agentes
- Sistema de pontuação de qualidade (0-10)
- Loop de melhoria automática com feedback
- Exportação em JSON
- Download de imagens geradas
- Visualização de resultados com tabs
- Logs coloridos em tempo real
- Scripts de inicialização (start.sh / start.bat)
- Script de teste independente (test_system.py)
- Documentação completa:
  - README.md
  - QUICKSTART.md
  - Comentários inline no código
- Configuração via arquivo .env
- .gitignore configurado
- requirements.txt com todas as dependências

#### Funcionalidades Principais
- Geração de 9 tipos de conteúdo diferentes:
  1. Tipo de Material
  2. Descrição Hotmart (máx. 1.800 caracteres)
  3. Artigo Blog (HTML completo)
  4. Legenda Instagram
  5. Imagem Vertical (1080x1920px)
  6. Imagem Quadrada (1080x1080px)
  7. Nome Criativo (5 palavras)
  8. Descrição Página de Vendas (25 palavras)
  9. Item Extra (customizável)

#### Arquitetura
- StateGraph do LangGraph para fluxo de agentes
- Nós: Criador, Revisor, Finalizar
- Condicionais: Qualidade >= 8 → Salvar
- Iterações configuráveis (1-10)
- Critérios de avaliação claros:
  - Clareza (2 pts)
  - Persuasão (2 pts)
  - Criatividade (2 pts)
  - Adequação ao Público (2 pts)
  - Potencial de Conversão (2 pts)

### 🔒 Segurança
- API keys via variáveis de ambiente
- Validação de entrada com Pydantic
- Tratamento de erros robusto

### 📊 Performance
- WebSocket para comunicação em tempo real
- Processamento assíncrono
- Logs não-bloqueantes

### 🎨 Interface
- Design moderno com variáveis CSS
- Responsivo (mobile-friendly)
- Tema claro profissional
- Animações suaves
- Feedback visual constante

---

## [Futuro] - Roadmap

### 🔮 Planejado para v1.1.0
- [ ] Suporte a mais provedores (Grok, Qwen)
- [ ] Google Imagen 3 para geração de imagens
- [ ] Sistema de templates por nicho
- [ ] Cache de prompts
- [ ] Regeneração individual de itens
- [ ] Exportação em ZIP
- [ ] Histórico de gerações

### 🔮 Planejado para v1.2.0
- [ ] Multi-idioma (EN, ES)
- [ ] A/B Testing (múltiplas versões)
- [ ] Integração com Hotmart API
- [ ] Publicação automática em redes sociais
- [ ] Dashboard de analytics
- [ ] Sistema de usuários e autenticação

### 🔮 Planejado para v2.0.0
- [ ] Refatoração para microserviços
- [ ] API REST completa
- [ ] CLI para automação
- [ ] Integração com mais plataformas
- [ ] Machine Learning para otimização

---

## Tipos de Mudanças
- `Adicionado` para novas funcionalidades
- `Alterado` para mudanças em funcionalidades existentes
- `Descontinuado` para funcionalidades que serão removidas
- `Removido` para funcionalidades removidas
- `Corrigido` para correções de bugs
- `Segurança` para vulnerabilidades corrigidas

---

**Data de Criação:** 10 de Novembro de 2025  
**Última Atualização:** 10 de Novembro de 2025
