# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o Marketing AI System! Este documento fornece diretrizes para contribuições.

## 📋 Índice

- [Como Contribuir](#como-contribuir)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Melhorias](#sugerir-melhorias)
- [Desenvolvimento](#desenvolvimento)
- [Padrões de Código](#padrões-de-código)
- [Processo de Pull Request](#processo-de-pull-request)

## Como Contribuir

Existem várias formas de contribuir:

1. **Reportar bugs** - Encontrou um problema? Nos avise!
2. **Sugerir melhorias** - Tem uma ideia? Compartilhe!
3. **Melhorar documentação** - Documentação clara ajuda todos
4. **Escrever código** - Corrija bugs ou adicione features
5. **Testar** - Use o sistema e dê feedback

## Reportar Bugs

Antes de reportar um bug, verifique se ele já não foi reportado.

### Como Reportar

Inclua no seu report:

- **Descrição clara** do problema
- **Passos para reproduzir**:
  1. Passo 1
  2. Passo 2
  3. ...
- **Comportamento esperado** vs **comportamento atual**
- **Screenshots** (se aplicável)
- **Ambiente**:
  - OS: [Windows/Mac/Linux]
  - Python: [versão]
  - Provedor LLM usado
- **Logs de erro** (se houver)

### Exemplo

```markdown
**Bug**: Geração de imagem falha silenciosamente

**Passos**:
1. Marcar checkbox "Imagem Vertical"
2. Clicar em "Gerar Conteúdos"
3. Processo finaliza mas imagem não aparece

**Esperado**: Imagem deve ser gerada ou erro deve ser exibido

**Atual**: Nenhuma imagem e nenhum erro

**Ambiente**:
- OS: Windows 11
- Python: 3.11.5
- Provedor: OpenAI
```

## Sugerir Melhorias

Sugestões são bem-vindas! Para features grandes, abra uma discussão primeiro.

### Template de Sugestão

```markdown
**Feature**: [Nome da feature]

**Problema**: Que problema isso resolve?

**Solução**: Como você imagina que funcione?

**Alternativas**: Considerou outras abordagens?

**Contexto**: Qualquer informação adicional
```

## Desenvolvimento

### Setup Local

```bash
# 1. Fork o repositório
# 2. Clone seu fork
git clone https://github.com/seu-usuario/marketing-ai-system.git
cd marketing-ai-system

# 3. Criar branch para sua feature
git checkout -b feature/minha-feature

# 4. Instalar em modo desenvolvimento
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 5. Configurar .env com suas keys
cp .env.example .env
# Editar .env

# 6. Testar
python test_system.py
python app.py
```

### Estrutura do Projeto

```
marketing-ai-system/
├── app.py              # Backend FastAPI principal
├── agents.py           # Lógica LangGraph (agentes)
├── models.py           # Modelos Pydantic
├── test_system.py      # Testes
├── templates/          # HTML
│   └── index.html
├── static/             # CSS e JS
│   ├── style.css
│   └── script.js
└── outputs/            # Resultados gerados
```

### Áreas de Contribuição

#### 🤖 Backend (Python)
- `app.py` - API e servidor
- `agents.py` - Lógica de agentes
- `models.py` - Validação de dados

#### 🎨 Frontend
- `templates/index.html` - Estrutura
- `static/style.css` - Estilos
- `static/script.js` - Interatividade

#### 📚 Documentação
- `README.md` - Documentação principal
- `QUICKSTART.md` - Guia rápido
- Comentários no código

## Padrões de Código

### Python

```python
# Use docstrings
def minha_funcao(param: str) -> bool:
    """
    Descrição breve.
    
    Args:
        param: Descrição do parâmetro
        
    Returns:
        Descrição do retorno
    """
    pass

# Type hints sempre que possível
def processar(dados: dict) -> list[str]:
    ...

# Nomes descritivos
def calcular_nota_qualidade() -> float:  # ✅ Bom
def calc() -> float:  # ❌ Evitar
```

### JavaScript

```javascript
// Use const/let, nunca var
const config = {...};
let resultado = null;

// Funções descritivas
function atualizarInterfaceComResultados() { }  // ✅
function update() { }  // ❌

// Comentários quando necessário
// Atualiza UI após geração bem-sucedida
function exibirResultados(data) { }
```

### CSS

```css
/* Use variáveis CSS */
:root {
    --primary: #6366f1;
}

/* Nomes BEM ou descritivos */
.button-primary { }  /* ✅ */
.btn1 { }  /* ❌ */

/* Comentários para seções */
/* === Header === */
.header { }
```

## Processo de Pull Request

### Antes de Submeter

- [ ] Código testado localmente
- [ ] Sem erros no console
- [ ] Documentação atualizada (se necessário)
- [ ] Commits com mensagens claras
- [ ] Code review próprio realizado

### Convenções de Commit

```bash
# Formato
<tipo>: <descrição curta>

[corpo opcional explicando o que e por que]

# Tipos
feat:     Nova feature
fix:      Correção de bug
docs:     Apenas documentação
style:    Formatação (não afeta código)
refactor: Refatoração
test:     Adicionar/modificar testes
chore:    Tarefas de manutenção

# Exemplos
feat: adicionar suporte para Grok LLM
fix: corrigir erro de conexão WebSocket
docs: atualizar README com novos exemplos
refactor: simplificar lógica de validação
```

### Submeter PR

1. **Push** sua branch
   ```bash
   git push origin feature/minha-feature
   ```

2. **Criar PR** no GitHub
   - Título claro e descritivo
   - Descrição explicando:
     - O que muda
     - Por que muda
     - Como testar

3. **Template de PR**
   ```markdown
   ## Descrição
   Breve descrição das mudanças
   
   ## Tipo de Mudança
   - [ ] Bug fix
   - [ ] Nova feature
   - [ ] Breaking change
   - [ ] Documentação
   
   ## Como Testar
   1. Passo 1
   2. Passo 2
   
   ## Checklist
   - [ ] Código testado
   - [ ] Documentação atualizada
   - [ ] Sem warnings/erros
   ```

4. **Aguardar Review**
   - Responder comentários
   - Fazer ajustes se necessário
   - Manter discussão construtiva

## Código de Conduta

### Nossos Padrões

**Comportamento Incentivado:**
- Ser respeitoso e empático
- Aceitar críticas construtivas
- Focar no que é melhor para a comunidade
- Mostrar empatia com outros membros

**Comportamento Inaceitável:**
- Linguagem ofensiva ou depreciativa
- Ataques pessoais ou políticos
- Assédio público ou privado
- Publicar informação privada de outros

### Aplicação

Instâncias de comportamento inaceitável podem ser reportadas.
Todas as reclamações serão revisadas e investigadas.

## Dúvidas?

- Abra uma **Issue** para dúvidas gerais
- Use **Discussions** para conversas mais abertas
- Entre em contato diretamente se preferir

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto (MIT).

---

**Obrigado por contribuir! 🎉**

Toda contribuição, grande ou pequena, é valiosa e apreciada.
