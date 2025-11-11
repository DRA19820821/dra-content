"""
Script de diagnóstico para verificar configuração das API keys
Execute: python check_config.py
"""
import os
from pathlib import Path
from dotenv import load_dotenv

def check_env_file():
    """Verifica se arquivo .env existe"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Arquivo .env NÃO encontrado!")
        print()
        print("📝 SOLUÇÃO:")
        print("1. Copie o arquivo de exemplo:")
        print("   cp .env.example .env")
        print("   (Windows: copy .env.example .env)")
        print()
        print("2. Edite o .env e adicione suas API keys")
        print()
        return False
    else:
        print("✅ Arquivo .env encontrado!")
        return True

def check_api_keys():
    """Verifica quais API keys estão configuradas"""
    load_dotenv()
    
    keys_to_check = {
        'ANTHROPIC_API_KEY': 'Anthropic (Claude Sonnet 4.5)',
        'OPENAI_API_KEY': 'OpenAI (GPT-5, GPT Image 1)',
        'GOOGLE_API_KEY': 'Google (Gemini 2.5 Plus, Imagen 3)',
        'DEEPSEEK_API_KEY': 'DeepSeek (v3)',
        'XAI_API_KEY': 'Grok (2.0)',
        'DASHSCOPE_API_KEY': 'Qwen (QwQ-32B-Preview)'
    }
    
    print()
    print("📋 STATUS DAS API KEYS:")
    print("-" * 60)
    
    configured_keys = []
    missing_keys = []
    
    for key_name, provider in keys_to_check.items():
        key_value = os.getenv(key_name)
        
        if key_value and key_value != f"your_{key_name.lower()}_here":
            status = "✅ CONFIGURADA"
            configured_keys.append(provider)
            # Mostrar preview da key (primeiros e últimos 4 caracteres)
            if len(key_value) > 8:
                preview = f"{key_value[:4]}...{key_value[-4:]}"
            else:
                preview = "***"
            print(f"{status} | {provider}")
            print(f"            {key_name} = {preview}")
        else:
            status = "❌ FALTANDO "
            missing_keys.append(provider)
            print(f"{status} | {provider}")
            print(f"            {key_name} não configurada")
        print()
    
    print("-" * 60)
    print()
    
    if configured_keys:
        print(f"✅ {len(configured_keys)} provider(s) configurado(s):")
        for provider in configured_keys:
            print(f"   • {provider}")
        print()
    
    if missing_keys:
        print(f"⚠️  {len(missing_keys)} provider(s) faltando:")
        for provider in missing_keys:
            print(f"   • {provider}")
        print()
    
    return len(configured_keys) > 0

def recommend_provider():
    """Recomenda qual provider usar baseado nas keys configuradas"""
    load_dotenv()
    
    print("🎯 RECOMENDAÇÕES:")
    print("-" * 60)
    
    if os.getenv('ANTHROPIC_API_KEY') and os.getenv('ANTHROPIC_API_KEY') != "your_anthropic_api_key_here":
        print("✨ Use: Anthropic (Claude Sonnet 4.5)")
        print("   • Melhor custo-benefício")
        print("   • Excelente qualidade")
        print("   • Recomendado pelo sistema")
        print()
        print("   No teste, use: llm_provider='anthropic'")
        return 'anthropic'
    
    elif os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != "your_openai_api_key_here":
        print("✨ Use: OpenAI (GPT-5)")
        print("   • Muito poderoso")
        print("   • Suporte completo a imagens")
        print()
        print("   No teste, use: llm_provider='openai'")
        return 'openai'
    
    elif os.getenv('GOOGLE_API_KEY') and os.getenv('GOOGLE_API_KEY') != "your_google_api_key_here":
        print("✨ Use: Google (Gemini 2.5 Plus)")
        print("   • Janela de contexto grande")
        print("   • Boa para tarefas técnicas")
        print()
        print("   No teste, use: llm_provider='google'")
        return 'google'
    
    else:
        print("❌ Nenhuma API key válida encontrada!")
        print()
        print("📝 VOCÊ PRECISA DE PELO MENOS UMA API KEY:")
        print()
        print("Opção 1 - Anthropic (Recomendado):")
        print("   • Crie conta: https://console.anthropic.com/")
        print("   • Gere API key")
        print("   • Adicione ao .env: ANTHROPIC_API_KEY=sk-ant-...")
        print()
        print("Opção 2 - OpenAI:")
        print("   • Crie conta: https://platform.openai.com/")
        print("   • Gere API key")
        print("   • Adicione ao .env: OPENAI_API_KEY=sk-...")
        print()
        print("Opção 3 - Google:")
        print("   • Crie conta: https://ai.google.dev/")
        print("   • Gere API key")
        print("   • Adicione ao .env: GOOGLE_API_KEY=AI...")
        print()
        return None

def show_next_steps(provider):
    """Mostra próximos passos"""
    if provider:
        print()
        print("🚀 PRÓXIMOS PASSOS:")
        print("-" * 60)
        print("1. Execute o teste novamente:")
        print("   python test_system.py")
        print()
        print("2. Se quiser testar outro provider, edite test_system.py:")
        print(f"   Mude: llm_provider='{provider}'")
        print()
        print("3. Para usar a interface web:")
        print("   python app.py")
        print("   Depois acesse: http://localhost:8000")
        print()

def main():
    print("=" * 60)
    print("🔍 DIAGNÓSTICO DE CONFIGURAÇÃO")
    print("=" * 60)
    print()
    
    # Verificar .env
    has_env = check_env_file()
    
    if not has_env:
        print()
        print("⚠️  Configure o .env primeiro antes de continuar!")
        return
    
    # Verificar API keys
    has_keys = check_api_keys()
    
    # Recomendar provider
    provider = recommend_provider()
    
    # Próximos passos
    show_next_steps(provider)
    
    if has_keys:
        print("=" * 60)
        print("✅ SISTEMA PRONTO PARA USO!")
        print("=" * 60)
    else:
        print("=" * 60)
        print("❌ CONFIGURE AS API KEYS PRIMEIRO")
        print("=" * 60)

if __name__ == "__main__":
    main()
