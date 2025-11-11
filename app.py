"""
Backend FastAPI para sistema de geração de conteúdos de marketing
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import Request
from pydantic import ValidationError
import asyncio
import json
import uuid
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import base64
from dotenv import load_dotenv

from models import ConfigGerador, ResultadoFinal
from agents import MarketingAgents

# Importações para geração de imagens
from openai import OpenAI
import google.generativeai as genai
import httpx

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI(title="Marketing AI System")

# Configurar templates e arquivos estáticos
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Gerenciador de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_log(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Página principal"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para logs em tempo real"""
    await manager.connect(websocket)
    try:
        while True:
            # Manter conexão aberta
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def gerar_imagem_openai(prompt: str, tamanho: str = "1024x1024") -> Optional[bytes]:
    """Gera imagem usando GPT Image 1 (DALL-E 3)"""
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Mapear tamanhos
        size_map = {
            "1080x1920": "1024x1792",  # Vertical
            "1080x1080": "1024x1024"   # Quadrado
        }
        dalle_size = size_map.get(tamanho, "1024x1024")
        
        response = client.images.generate(
            model="dall-e-3",  # GPT Image 1
            prompt=prompt,
            size=dalle_size,
            quality="hd",  # Usar HD para melhor qualidade
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Baixar imagem
        async with httpx.AsyncClient() as http_client:
            img_response = await http_client.get(image_url)
            if img_response.status_code == 200:
                return img_response.content
        
        return None
        
    except Exception as e:
        print(f"Erro ao gerar imagem GPT Image 1: {e}")
        return None


async def gerar_imagem_google(prompt: str, tamanho: str = "1024x1024") -> Optional[bytes]:
    """Gera imagem usando Google Imagen 3 (Nano Banana)"""
    try:
        # Configurar Google Imagen 3
        import google.generativeai as genai
        
        # Configurar API key
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            print("GOOGLE_API_KEY não configurada")
            return None
            
        genai.configure(api_key=google_api_key)
        
        # Nota: Imagen 3 via API pode ter configurações específicas
        # Esta é uma implementação adaptável conforme a API do Google
        
        model = genai.GenerativeModel('imagen-3')
        
        # Ajustar prompt para melhor qualidade
        enhanced_prompt = f"{prompt} high quality, professional, modern design"
        
        # Gerar imagem
        response = model.generate_images(
            prompt=enhanced_prompt,
            number_of_images=1,
            aspect_ratio=tamanho,
        )
        
        if response and response.images:
            # Retornar bytes da primeira imagem
            return response.images[0]._pil_image.tobytes()
        
        return None
        
    except Exception as e:
        print(f"Erro ao gerar imagem Google Imagen 3: {e}")
        # Fallback para OpenAI se Google falhar
        return await gerar_imagem_openai(prompt, tamanho)


async def processar_geracao(config_dict: dict, websocket: WebSocket):
    """Processa a geração completa de conteúdos"""
    try:
        # Validar configuração
        config = ConfigGerador(**config_dict)
        
        await manager.send_log(
            json.dumps({"type": "info", "message": "🚀 Iniciando geração de conteúdos..."}),
            websocket
        )
        
        # Criar sistema de agentes
        agents = MarketingAgents(config)
        
        await manager.send_log(
            json.dumps({"type": "info", "message": f"🤖 Usando LLM: {config.llm_provider}"}),
            websocket
        )
        
        # Executar fluxo
        conteudo, avaliacao, logs, iteracoes = agents.executar()
        
        # Enviar logs em tempo real
        for log in logs:
            await manager.send_log(
                json.dumps({"type": "log", "message": log}),
                websocket
            )
        
        if not conteudo or not avaliacao:
            await manager.send_log(
                json.dumps({"type": "error", "message": "❌ Erro ao gerar conteúdo"}),
                websocket
            )
            return None
        
        # Gerar ID único
        id_conteudos = str(uuid.uuid4())[:10]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Criar pasta de output
        output_dir = Path(f"outputs/{timestamp}_{id_conteudos}")
        output_dir.mkdir(parents=True, exist_ok=True)
        images_dir = output_dir / "imagens"
        images_dir.mkdir(exist_ok=True)
        
        await manager.send_log(
            json.dumps({"type": "info", "message": f"📁 Pasta criada: {output_dir}"}),
            websocket
        )
        
        # Gerar imagens se solicitado
        nome_img_vert = None
        nome_img_quad = None
        
        if config.gerar_imagem_vert or config.gerar_imagem_quad:
            await manager.send_log(
                json.dumps({"type": "info", "message": "🎨 Gerando imagens..."}),
                websocket
            )
            
            # Criar prompt para imagem
            prompt_imagem = f"""Crie uma imagem moderna e profissional para um produto educacional brasileiro.
Produto: {conteudo.nome_criativo}
Tipo: {conteudo.tipo_material}
Estilo: Moderno, clean, cores vibrantes, tipografia legível
Elementos: Livros, mapas mentais, elementos educacionais
Público: Estudantes de concursos públicos e OAB"""
            
            if config.gerar_imagem_vert:
                if config.image_provider == "google":
                    img_vert = await gerar_imagem_google(prompt_imagem, "1080x1920")
                else:
                    img_vert = await gerar_imagem_openai(prompt_imagem, "1080x1920")
                    
                if img_vert:
                    nome_img_vert = f"{config.radical}_{conteudo.tipo_material.replace(' ', '')}_Vert_{timestamp}.png"
                    with open(images_dir / nome_img_vert, "wb") as f:
                        f.write(img_vert)
                    await manager.send_log(
                        json.dumps({"type": "success", "message": f"✅ Imagem vertical gerada: {nome_img_vert}"}),
                        websocket
                    )
            
            if config.gerar_imagem_quad:
                if config.image_provider == "google":
                    img_quad = await gerar_imagem_google(prompt_imagem, "1080x1080")
                else:
                    img_quad = await gerar_imagem_openai(prompt_imagem, "1080x1080")
                    
                if img_quad:
                    nome_img_quad = f"{config.radical}_{conteudo.tipo_material.replace(' ', '')}_Quad_{timestamp}.png"
                    with open(images_dir / nome_img_quad, "wb") as f:
                        f.write(img_quad)
                    await manager.send_log(
                        json.dumps({"type": "success", "message": f"✅ Imagem quadrada gerada: {nome_img_quad}"}),
                        websocket
                    )
        
        # Criar resultado final
        resultado = ResultadoFinal(
            data_geracao=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            id_conteudos=id_conteudos,
            tipo_material=conteudo.tipo_material,
            desc_hotmart=conteudo.desc_hotmart,
            artigo=conteudo.artigo,
            legenda=conteudo.legenda,
            nome_imagem_vert=nome_img_vert,
            nome_imagem_quad=nome_img_quad,
            nome_criativo=conteudo.nome_criativo,
            desc_pv=conteudo.desc_pv,
            extra=conteudo.extra,
            nota_conteudo=avaliacao.nota,
            iteracoes_realizadas=iteracoes,
            qualidade_pendente=(avaliacao.nota < 8 and iteracoes >= config.max_iteracoes)
        )
        
        # Salvar JSON
        json_path = output_dir / "conteudo.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(resultado.model_dump(), f, ensure_ascii=False, indent=2)
        
        await manager.send_log(
            json.dumps({"type": "success", "message": f"✅ JSON salvo: {json_path}"}),
            websocket
        )
        
        # Enviar resultado completo
        await manager.send_log(
            json.dumps({
                "type": "resultado",
                "data": {
                    **resultado.model_dump(),
                    "output_dir": str(output_dir),
                    "json_path": str(json_path)
                }
            }),
            websocket
        )
        
        await manager.send_log(
            json.dumps({"type": "success", "message": f"🎉 Geração concluída! Nota final: {avaliacao.nota}/10"}),
            websocket
        )
        
        return resultado
        
    except ValidationError as e:
        await manager.send_log(
            json.dumps({"type": "error", "message": f"❌ Erro de validação: {str(e)}"}),
            websocket
        )
        return None
    except Exception as e:
        await manager.send_log(
            json.dumps({"type": "error", "message": f"❌ Erro: {str(e)}"}),
            websocket
        )
        return None


@app.post("/gerar")
async def gerar_conteudo(config: dict, websocket: WebSocket):
    """Endpoint para iniciar geração (chamado via WebSocket)"""
    resultado = await processar_geracao(config, websocket)
    return {"status": "success" if resultado else "error"}


@app.get("/download/{folder}/{filename}")
async def download_arquivo(folder: str, filename: str):
    """Endpoint para download de arquivos"""
    file_path = Path(f"outputs/{folder}/{filename}")
    if file_path.exists():
        return FileResponse(file_path, filename=filename)
    raise HTTPException(status_code=404, detail="Arquivo não encontrado")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
