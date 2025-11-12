"""
Sistema de agentes usando LangGraph para criação e revisão de conteúdos
"""
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from models import ConteudoGerado, AvaliacaoRevisor, ConfigGerador
import operator
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

MAX_TOKENS_ = 16000

# Estado compartilhado entre os nós
class AgentState(TypedDict):
    config: ConfigGerador
    conteudo: ConteudoGerado | None
    avaliacao: AvaliacaoRevisor | None
    iteracao_atual: Annotated[int, operator.add]
    logs: Annotated[list[str], operator.add]
    timestamp: str


class MarketingAgents:
    """Sistema de agentes para geração de conteúdos de marketing"""
    
    def __init__(self, config: ConfigGerador):
        self.config = config
        self.llm = self._get_llm(config.llm_provider)
        
    def _get_llm(self, provider: str):
        """Retorna o LLM configurado baseado no provedor"""
        if provider == "anthropic":
            return ChatAnthropic(
                model="claude-sonnet-4-5",  # Claude Sonnet 4.5 (mais recente)
                temperature=0.7,
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                max_tokens = MAX_TOKENS_
            )
        elif provider == "openai":
            return ChatOpenAI(
                model="gpt-5",  # GPT-5 (mais recente)
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY"),
                max_tokens = MAX_TOKENS_
            )
        elif provider == "google":
            return ChatGoogleGenerativeAI(
                model="gemini-2.5-pro",  # Gemini 2.5 Plus (mais recente)
                temperature=0.7,
                google_api_key=os.getenv("GOOGLE_API_KEY"),
                max_tokens = MAX_TOKENS_
            )
        elif provider == "deepseek":
            return ChatOpenAI(
                base_url="https://api.deepseek.com",
                model="deepseek-chat",  # DeepSeek v3
                temperature=0.7,
                api_key=os.getenv("DEEPSEEK_API_KEY"),
                max_tokens = MAX_TOKENS_
            )
        elif provider == "grok":
            return ChatOpenAI(
                base_url="https://api.x.ai/v1",
                model="grok-2.0",  # Grok 2.0
                temperature=0.7,
                api_key=os.getenv("XAI_API_KEY"),
                max_tokens = MAX_TOKENS_
            )
        elif provider == "qwen":
            return ChatOpenAI(
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                model="qwq-32b-preview",  # Qwen QwQ-32B-Preview
                temperature=0.7,
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                max_tokens = MAX_TOKENS_
            )
        else:
            # Default para Anthropic Claude Sonnet 4.5
            return ChatAnthropic(
                model="claude-sonnet-4-5",
                temperature=0.7,
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                max_tokens = MAX_TOKENS_
            )
    
    def criar_conteudo(self, state: AgentState) -> dict:
        """Nó criador: gera conteúdos usando resposta estruturada"""
        logs = [f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando criação de conteúdo..."]
        
        # Construir prompt baseado no checklist
        prompt = self._construir_prompt_criador(state)
        
        try:
            # Usar structured output com Pydantic
            llm_estruturado = self.llm.with_structured_output(ConteudoGerado)
            
            # Se já existe conteúdo e avaliação, incluir feedback
            if state.get("conteudo") and state.get("avaliacao"):
                prompt += f"\n\nFEEDBACK DA REVISÃO ANTERIOR:\n{state['avaliacao'].feedback}\n"
                prompt += f"Nota anterior: {state['avaliacao'].nota}/10\n"
                prompt += "Por favor, melhore o conteúdo considerando este feedback."
                logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Melhorando conteúdo com base no feedback...")
            
            conteudo = llm_estruturado.invoke(prompt)
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Conteúdo gerado com sucesso!")
            
            return {
                "conteudo": conteudo,
                "iteracao_atual": 1,
                "logs": logs
            }
            
        except Exception as e:
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ERRO ao gerar conteúdo: {str(e)}")
            return {
                "conteudo": None,
                "iteracao_atual": 1,
                "logs": logs
            }
    
    def revisar_conteudo(self, state: AgentState) -> dict:
        """Nó revisor: avalia qualidade com critérios claros"""
        logs = [f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando revisão (iteração {state.get('iteracao_atual', 0)})..."]
        
        conteudo = state["conteudo"]
        if not conteudo:
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ERRO: Nenhum conteúdo para revisar")
            return {"logs": logs}
        
        prompt = self._construir_prompt_revisor(conteudo, state["config"])
        
        try:
            llm_estruturado = self.llm.with_structured_output(AvaliacaoRevisor)
            avaliacao = llm_estruturado.invoke(prompt)
            
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Revisão concluída!")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Nota: {avaliacao.nota}/10")
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Status: {'✅ Aprovado' if avaliacao.aprovado else '❌ Precisa melhorar'}")
            
            if avaliacao.feedback:
                logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] Feedback: {avaliacao.feedback}")
            
            return {
                "avaliacao": avaliacao,
                "logs": logs
            }
            
        except Exception as e:
            logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] ERRO na revisão: {str(e)}")
            # Criar avaliação default em caso de erro
            avaliacao_default = AvaliacaoRevisor(
                nota=7.0,
                feedback=f"Erro na revisão: {str(e)}",
                aprovado=True,
                clareza=1.4,
                persuasao=1.4,
                criatividade=1.4,
                adequacao=1.4,
                conversao=1.4
            )
            return {
                "avaliacao": avaliacao_default,
                "logs": logs
            }
    
    def deve_continuar(self, state: AgentState) -> Literal["criar_conteudo", "finalizar"]:
        """Decide se deve continuar o loop ou finalizar"""
        avaliacao = state.get("avaliacao")
        iteracao = state.get("iteracao_atual", 0)
        max_iter = state["config"].max_iteracoes
        
        # Se aprovado ou atingiu max iterações, finalizar
        if avaliacao and avaliacao.aprovado:
            return "finalizar"
        
        if iteracao >= max_iter:
            return "finalizar"
        
        # Caso contrário, tentar novamente
        return "criar_conteudo"
    
    def _construir_prompt_criador(self, state: AgentState) -> str:
        """Constrói prompt dinâmico baseado na configuração"""
        config = state["config"]
        
        prompt = f"""Você é um especialista em marketing digital e copywriting para produtos educacionais brasileiros.

INFORMAÇÕES DO PRODUTO:
Radical: {config.radical}
Insumos: {config.insumos}

TAREFA: Gere conteúdos persuasivos, modernos e otimizados para conversão, sempre mantendo tom descontraído mas profissional.

DIRETRIZES:
1. **Tipo de Material**: Classifique entre "Baralhos Anki", "Mapas Mentais", "Músicas" ou "Podcasts" baseado nos insumos
2. **Descrição Hotmart**: Texto atrativo e instigante (máximo 1.800 caracteres). Foque nos benefícios e transformação
3. **Artigo Blog**: HTML completo com estrutura moderna (<article>, <section>, <h1-h3>, <p>, <strong>, <ul>). Narrativa de venda engajadora com:
   - Introdução que prende atenção
   - Desenvolvimento mostrando benefícios
   - Call-to-action forte
4. **Legenda Instagram**: Texto curto, envolvente, com emojis estratégicos e hashtags relevantes
5. **Nome Criativo**: Máximo 5 palavras impactantes que vendam o produto
6. **Descrição Página de Vendas**: Máximo 25 palavras ultra-persuasivas

PÚBLICO-ALVO: Estudantes brasileiros de concursos públicos e OAB que buscam aprovação

ESTILO: 
- Tom: Motivacional, acessível, brasileiro
- Evite jargões excessivos
- Use linguagem que conecta e inspira
- Destaque transformação e resultados

"""

        if config.gerar_extra and config.prompt_extra:
            prompt += f"\n\n**ITEM EXTRA CUSTOMIZADO**:\n{config.prompt_extra}"
        
        return prompt
    
    def _construir_prompt_revisor(self, conteudo: ConteudoGerado, config: ConfigGerador) -> str:
        """Constrói prompt do revisor"""
        return f"""Você é um revisor especializado em conteúdos de marketing digital para educação.

CRITÉRIOS DE AVALIAÇÃO (Total: 10 pontos):
1. **Clareza** (2 pontos): Mensagem clara e objetiva?
2. **Persuasão** (2 pontos): Convincente e envolvente?
3. **Criatividade** (2 pontos): Original e memorável?
4. **Adequação ao Público** (2 pontos): Conecta com estudantes brasileiros?
5. **Potencial de Conversão** (2 pontos): Leva à ação de compra?

CONTEÚDO A AVALIAR:
---
Tipo: {conteudo.tipo_material}
Nome: {conteudo.nome_criativo}
Desc. Hotmart: {conteudo.desc_hotmart[:200]}...
Legenda: {conteudo.legenda[:100]}...
Desc. PV: {conteudo.desc_pv}
---

INSTRUÇÕES:
- Avalie cada critério de 0 a 2 pontos
- Nota >= 8: aprovar (aprovado=true)
- Nota < 8: reprovar (aprovado=false) e dar feedback específico e acionável
- No feedback, seja direto sobre o que precisa melhorar

ANÁLISE:
Considere se o conteúdo:
- Desperta interesse imediato
- Comunica benefícios claros
- Usa linguagem adequada ao público brasileiro
- Tem call-to-action efetivo
- É profissional mas descontraído"""

    def criar_grafo(self) -> StateGraph:
        """Cria o grafo LangGraph com nós e transições"""
        workflow = StateGraph(AgentState)
        
        # Adicionar nós
        workflow.add_node("criar_conteudo", self.criar_conteudo)
        workflow.add_node("revisar_conteudo", self.revisar_conteudo)
        workflow.add_node("finalizar", lambda state: state)
        
        # Definir transições
        workflow.set_entry_point("criar_conteudo")
        
        workflow.add_edge("criar_conteudo", "revisar_conteudo")
        workflow.add_conditional_edges(
            "revisar_conteudo",
            self.deve_continuar,
            {
                "criar_conteudo": "criar_conteudo",
                "finalizar": "finalizar"
            }
        )
        
        workflow.add_edge("finalizar", END)
        
        return workflow.compile()
    
    def executar(self) -> tuple[ConteudoGerado | None, AvaliacaoRevisor | None, list[str], int]:
        """Executa o fluxo completo e retorna resultado"""
        grafo = self.criar_grafo()
        
        estado_inicial = AgentState(
            config=self.config,
            conteudo=None,
            avaliacao=None,
            iteracao_atual=0,
            logs=[],
            timestamp=datetime.now().isoformat()
        )
        
        try:
            resultado = grafo.invoke(estado_inicial)
            
            conteudo = resultado.get("conteudo")
            avaliacao = resultado.get("avaliacao")
            logs = resultado.get("logs", [])
            iteracoes = resultado.get("iteracao_atual", 0)
            
            return conteudo, avaliacao, logs, iteracoes
            
        except Exception as e:
            logs_erro = [f"[{datetime.now().strftime('%H:%M:%S')}] ERRO CRÍTICO: {str(e)}"]
            return None, None, logs_erro, 0
