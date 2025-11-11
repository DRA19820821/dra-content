"""
Modelos Pydantic para validação e estruturação de dados
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class ConteudoGerado(BaseModel):
    """Modelo para conteúdos gerados pelo agente criador"""
    tipo_material: Literal["Baralhos Anki", "Mapas Mentais", "Músicas", "Podcasts"]
    desc_hotmart: str = Field(max_length=1800, description="Descrição para Hotmart")
    artigo: str = Field(description="Artigo completo em HTML")
    legenda: str = Field(description="Legenda para Instagram")
    nome_criativo: str = Field(max_length=50, description="Nome criativo (máx 5 palavras)")
    desc_pv: str = Field(max_length=150, description="Descrição página de vendas (máx 25 palavras)")
    extra: Optional[str] = Field(default=None, description="Conteúdo extra customizável")


class AvaliacaoRevisor(BaseModel):
    """Modelo para avaliação do revisor"""
    nota: float = Field(ge=0, le=10, description="Nota de 0 a 10")
    feedback: Optional[str] = Field(default=None, description="Feedback detalhado")
    aprovado: bool = Field(description="Se o conteúdo foi aprovado")
    
    # Breakdown da nota
    clareza: float = Field(default=0, ge=0, le=2, description="Pontos de clareza")
    persuasao: float = Field(default=0, ge=0, le=2, description="Pontos de persuasão")
    criatividade: float = Field(default=0, ge=0, le=2, description="Pontos de criatividade")
    adequacao: float = Field(default=0, ge=0, le=2, description="Pontos de adequação ao público")
    conversao: float = Field(default=0, ge=0, le=2, description="Pontos de potencial de conversão")


class ConfigGerador(BaseModel):
    """Configurações para geração de conteúdo"""
    radical: str = Field(description="String alfanumérica (ex: dAdm, dConst)")
    insumos: str = Field(description="Texto base com informações do produto")
    max_iteracoes: int = Field(default=3, ge=1, le=10, description="Máximo de iterações")
    llm_provider: str = Field(default="anthropic", description="Provedor de LLM para texto")
    image_provider: str = Field(default="openai", description="Provedor para geração de imagens")
    
    # Checklist de conteúdos
    gerar_tipo_material: bool = Field(default=True)
    gerar_desc_hotmart: bool = Field(default=True)
    gerar_artigo: bool = Field(default=True)
    gerar_legenda: bool = Field(default=True)
    gerar_imagem_vert: bool = Field(default=True)
    gerar_imagem_quad: bool = Field(default=True)
    gerar_nome_criativo: bool = Field(default=True)
    gerar_desc_pv: bool = Field(default=False)
    gerar_extra: bool = Field(default=False)
    prompt_extra: Optional[str] = Field(default=None, description="Prompt para item extra")


class ResultadoFinal(BaseModel):
    """Modelo para o resultado final salvo em JSON"""
    data_geracao: str
    id_conteudos: str
    tipo_material: str
    desc_hotmart: str
    artigo: str
    legenda: str
    nome_imagem_vert: Optional[str] = None
    nome_imagem_quad: Optional[str] = None
    nome_criativo: str
    desc_pv: str
    extra: Optional[str] = None
    nota_conteudo: float
    iteracoes_realizadas: int
    qualidade_pendente: bool = False
