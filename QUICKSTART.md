# 🚀 Guia de Início Rápido

## Instalação em 5 Minutos

### 1. Instalar Python
```bash
# Verifique se tem Python 3.11+
python --version
```

### 2. Clonar/Baixar o Projeto
```bash
cd marketing-ai-system
```

### 3. Criar Ambiente Virtual
```bash
# Criar
python -m venv venv

# Ativar (Linux/Mac)
source venv/bin/activate

# Ativar (Windows)
venv\Scripts\activate
```

### 4. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 5. Configurar API Keys
```bash
# Copiar template
cp .env.example .env

# Editar .env e adicionar pelo menos uma key:
nano .env  # ou usar qualquer editor
```

**Mínimo necessário:**
```env
ANTHROPIC_API_KEY=sk-ant-seu-key-aqui
# OU
OPENAI_API_KEY=sk-seu-key-aqui
```

### 6. Iniciar Servidor

**Linux/Mac:**
```bash
./start.sh
# OU
python app.py
```

**Windows:**
```bash
start.bat
# OU
python app.py
```

### 7. Acessar Interface
Abra seu navegador em: **http://localhost:8000**

---

## 🎯 Primeiro Uso

1. **Selecione o provedor** de LLM (ex: Anthropic)
2. **Digite o radical** (ex: `dTest`)
3. **Cole os insumos** do produto
4. **Marque os conteúdos** que deseja gerar
5. Clique em **"Gerar Conteúdos"**
6. Aguarde o processo (1-3 minutos)
7. **Visualize e baixe** os resultados!

---

## ⚡ Teste Rápido (Sem Interface)

```bash
# Testar o sistema sem abrir o navegador
python test_system.py
```

Isso vai:
- ✅ Validar a instalação
- ✅ Testar conexão com LLM
- ✅ Gerar conteúdo de exemplo
- ✅ Salvar resultado em `test_output.json`

---

## 🆘 Problemas Comuns

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key not found"
- Verifique se `.env` existe
- Confirme que a key está correta
- Reinicie o servidor

### Porta 8000 ocupada
```bash
# Use outra porta
uvicorn app:app --port 8001
```

### WebSocket não conecta
- Recarregue a página (F5)
- Limpe cache do navegador
- Verifique firewall

---

## 📚 Próximos Passos

- Leia o [README.md](README.md) completo
- Customize os prompts em `agents.py`
- Ajuste o CSS em `static/style.css`
- Explore os exemplos de uso

---

## 🎓 Exemplo Prático

**Radical:** `dAdm`

**Insumos:**
```
Baralhos Anki de Direito Administrativo para concursos.
500+ flashcards com questões de provas anteriores.
Metodologia de repetição espaçada.
Público: concurseiros que buscam memorização eficiente.
Diferenciais: Questões comentadas, estatísticas, app mobile.
```

**Resultado:** O sistema vai gerar automaticamente:
- ✅ Nome criativo
- ✅ Descrição Hotmart
- ✅ Artigo para blog
- ✅ Legenda Instagram
- ✅ Imagens (se ativado)
- ✅ Tudo com qualidade revisada!

---

**Precisa de ajuda?** Consulte o [README.md](README.md) completo ou a seção de troubleshooting.
