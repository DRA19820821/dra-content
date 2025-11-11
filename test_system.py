"""
Script de teste para validar o sistema de agentes
Pode ser executado sem a interface web
"""
import asyncio
from models import ConfigGerador
from agents import MarketingAgents
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


def test_basic():
    """Teste básico do sistema de agentes"""
    
    print("=" * 60)
    print("TESTE DO SISTEMA DE GERAÇÃO DE CONTEÚDOS")
    print("=" * 60)
    print()
    
    # Configuração de teste
    config = ConfigGerador(
        radical="dTest",
        insumos="""
        Teste de Baralhos Anki para Direito Administrativo.
        Contém 500+ flashcards com questões de provas.
        Metodologia de repetição espaçada científica.
        Público: concurseiros em preparação.
        Diferenciais: Questões comentadas, estatísticas, app mobile.
        """,
        max_iteracoes=2,
        llm_provider="anthropic",  # Altere conforme necessário
        image_provider="openai",
        gerar_tipo_material=True,
        gerar_desc_hotmart=True,
        gerar_artigo=True,
        gerar_legenda=True,
        gerar_imagem_vert=False,  # Desabilitado para teste rápido
        gerar_imagem_quad=False,   # Desabilitado para teste rápido
        gerar_nome_criativo=True,
        gerar_desc_pv=True,
        gerar_extra=False
    )
    
    print(f"✓ Configuração criada")
    print(f"  - Radical: {config.radical}")
    print(f"  - LLM: {config.llm_provider}")
    print(f"  - Max Iterações: {config.max_iteracoes}")
    print()
    
    # Criar sistema de agentes
    print("🤖 Inicializando agentes...")
    agents = MarketingAgents(config)
    print("✓ Agentes inicializados")
    print()
    
    # Executar
    print("🚀 Executando fluxo de geração...")
    print("-" * 60)
    
    conteudo, avaliacao, logs, iteracoes = agents.executar()
    
    # Exibir logs
    print()
    print("📋 LOGS DE EXECUÇÃO:")
    print("-" * 60)
    for log in logs:
        print(log)
    print()
    
    # Verificar resultado
    if not conteudo or not avaliacao:
        print("❌ ERRO: Falha na geração de conteúdo")
        return False
    
    # Exibir resultados
    print("=" * 60)
    print("🎉 RESULTADOS")
    print("=" * 60)
    print()
    
    print(f"📊 AVALIAÇÃO")
    print(f"  - Nota Final: {avaliacao.nota:.1f}/10")
    print(f"  - Aprovado: {'✅ Sim' if avaliacao.aprovado else '❌ Não'}")
    print(f"  - Iterações: {iteracoes}")
    print()
    
    print(f"  Breakdown da Nota:")
    print(f"    • Clareza: {avaliacao.clareza:.1f}/2")
    print(f"    • Persuasão: {avaliacao.persuasao:.1f}/2")
    print(f"    • Criatividade: {avaliacao.criatividade:.1f}/2")
    print(f"    • Adequação: {avaliacao.adequacao:.1f}/2")
    print(f"    • Conversão: {avaliacao.conversao:.1f}/2")
    print()
    
    if avaliacao.feedback:
        print(f"  💬 Feedback: {avaliacao.feedback}")
        print()
    
    print(f"📝 CONTEÚDO GERADO")
    print(f"  - Tipo: {conteudo.tipo_material}")
    print(f"  - Nome: {conteudo.nome_criativo}")
    print(f"  - Desc. PV: {conteudo.desc_pv}")
    print()
    
    print(f"  📊 Tamanhos:")
    print(f"    • Desc. Hotmart: {len(conteudo.desc_hotmart)} caracteres")
    print(f"    • Artigo: {len(conteudo.artigo)} caracteres")
    print(f"    • Legenda: {len(conteudo.legenda)} caracteres")
    print()
    
    # Salvar em arquivo de teste
    test_output = {
        "conteudo": conteudo.model_dump(),
        "avaliacao": {
            "nota": avaliacao.nota,
            "aprovado": avaliacao.aprovado,
            "feedback": avaliacao.feedback,
            "breakdown": {
                "clareza": avaliacao.clareza,
                "persuasao": avaliacao.persuasao,
                "criatividade": avaliacao.criatividade,
                "adequacao": avaliacao.adequacao,
                "conversao": avaliacao.conversao
            }
        },
        "iteracoes": iteracoes,
        "timestamp": datetime.now().isoformat()
    }
    
    output_file = Path("test_output.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(test_output, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Resultado salvo em: {output_file}")
    print()
    
    print("=" * 60)
    print("✅ TESTE CONCLUÍDO COM SUCESSO")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        success = test_basic()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
