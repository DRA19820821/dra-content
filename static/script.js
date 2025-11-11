// Variáveis globais
let ws = null;
let resultadoAtual = null;
let outputDir = null;

// Elementos do DOM
const btnGerar = document.getElementById('btn-gerar');
const logsContainer = document.getElementById('logs-container');
const logsDiv = document.getElementById('logs');
const resultsContainer = document.getElementById('results-container');
const statusIndicator = document.getElementById('status');
const checkExtra = document.getElementById('check-extra');
const extraField = document.getElementById('extra-field');

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    initializeWebSocket();
});

function initializeEventListeners() {
    // Botão gerar
    btnGerar.addEventListener('click', iniciarGeracao);
    
    // Checkbox extra
    checkExtra.addEventListener('change', (e) => {
        extraField.style.display = e.target.checked ? 'block' : 'none';
    });
    
    // Tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });
    
    // Downloads
    document.getElementById('btn-download-json')?.addEventListener('click', downloadJSON);
    document.getElementById('btn-download-images')?.addEventListener('click', downloadImages);
}

function initializeWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
        console.log('WebSocket conectado');
        updateStatus('Pronto', 'success');
    };
    
    ws.onmessage = (event) => {
        handleWebSocketMessage(event.data);
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket erro:', error);
        updateStatus('Erro de conexão', 'error');
    };
    
    ws.onclose = () => {
        console.log('WebSocket desconectado');
        updateStatus('Desconectado', 'error');
        // Tentar reconectar após 3 segundos
        setTimeout(initializeWebSocket, 3000);
    };
}

function handleWebSocketMessage(data) {
    try {
        const message = JSON.parse(data);
        
        switch (message.type) {
            case 'log':
                addLog(message.message, 'log');
                break;
            case 'info':
                addLog(message.message, 'info');
                break;
            case 'success':
                addLog(message.message, 'success');
                break;
            case 'error':
                addLog(message.message, 'error');
                break;
            case 'resultado':
                exibirResultados(message.data);
                break;
        }
    } catch (e) {
        console.error('Erro ao processar mensagem:', e);
    }
}

function iniciarGeracao() {
    // Validar campos obrigatórios
    const radical = document.getElementById('radical').value.trim();
    const insumos = document.getElementById('insumos').value.trim();
    
    if (!radical || !insumos) {
        alert('Por favor, preencha os campos obrigatórios: Radical e Insumos');
        return;
    }
    
    // Coletar configuração
    const config = {
        radical,
        insumos,
        max_iteracoes: parseInt(document.getElementById('max-iteracoes').value),
        llm_provider: document.getElementById('llm-provider').value,
        image_provider: document.getElementById('image-provider').value,
        gerar_tipo_material: document.getElementById('check-tipo').checked,
        gerar_desc_hotmart: document.getElementById('check-desc-hotmart').checked,
        gerar_artigo: document.getElementById('check-artigo').checked,
        gerar_legenda: document.getElementById('check-legenda').checked,
        gerar_imagem_vert: document.getElementById('check-img-vert').checked,
        gerar_imagem_quad: document.getElementById('check-img-quad').checked,
        gerar_nome_criativo: document.getElementById('check-nome').checked,
        gerar_desc_pv: document.getElementById('check-desc-pv').checked,
        gerar_extra: document.getElementById('check-extra').checked,
        prompt_extra: document.getElementById('prompt-extra').value || null
    };
    
    // Resetar interface
    limparLogs();
    esconderResultados();
    logsContainer.style.display = 'block';
    
    // Desabilitar botão
    btnGerar.disabled = true;
    btnGerar.textContent = '⏳ Gerando...';
    updateStatus('Processando', 'processing');
    
    // Enviar via WebSocket
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ action: 'gerar', config }));
        
        // Iniciar geração via fetch (API)
        fetch('/gerar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Geração finalizada:', data);
        })
        .catch(error => {
            console.error('Erro na geração:', error);
            addLog(`Erro: ${error.message}`, 'error');
        })
        .finally(() => {
            btnGerar.disabled = false;
            btnGerar.textContent = '🎯 Gerar Conteúdos';
            updateStatus('Pronto', 'success');
        });
    } else {
        alert('Conexão WebSocket não está disponível. Tente recarregar a página.');
        btnGerar.disabled = false;
        btnGerar.textContent = '🎯 Gerar Conteúdos';
        updateStatus('Erro', 'error');
    }
}

function addLog(message, type = 'log') {
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;
    logEntry.textContent = message;
    logsDiv.appendChild(logEntry);
    
    // Auto-scroll
    logsDiv.scrollTop = logsDiv.scrollHeight;
}

function limparLogs() {
    logsDiv.innerHTML = '';
}

function updateStatus(text, state) {
    const statusText = statusIndicator.querySelector('.status-text');
    const statusDot = statusIndicator.querySelector('.status-dot');
    
    statusText.textContent = text;
    statusDot.className = `status-dot ${state}`;
}

function exibirResultados(data) {
    resultadoAtual = data;
    outputDir = data.output_dir;
    
    // Mostrar seção de resultados
    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
    
    // Preencher header
    document.getElementById('result-nome').textContent = data.nome_criativo;
    document.getElementById('result-tipo').textContent = data.tipo_material;
    
    // Nota com cor
    const notaBadge = document.getElementById('result-nota');
    notaBadge.textContent = `Nota: ${data.nota_conteudo.toFixed(1)}/10`;
    if (data.nota_conteudo >= 8) {
        notaBadge.classList.add('high-score');
    } else if (data.nota_conteudo >= 6) {
        notaBadge.classList.add('medium-score');
    } else {
        notaBadge.classList.add('low-score');
    }
    
    // Iterações
    const iterBadge = document.getElementById('result-iteracoes');
    iterBadge.textContent = `${data.iteracoes_realizadas} iterações`;
    
    // Preview
    document.getElementById('preview-nome').textContent = data.nome_criativo;
    document.getElementById('preview-desc-pv').textContent = data.desc_pv;
    document.getElementById('preview-tipo').textContent = data.tipo_material;
    
    // Conteúdos
    document.getElementById('content-desc-hotmart').textContent = data.desc_hotmart;
    document.getElementById('content-artigo').innerHTML = data.artigo;
    document.getElementById('content-legenda').textContent = data.legenda;
    document.getElementById('content-json').textContent = JSON.stringify(data, null, 2);
    
    // Imagens
    exibirImagens(data);
}

function exibirImagens(data) {
    const imagesContainer = document.getElementById('images-container');
    imagesContainer.innerHTML = '';
    
    const hasImages = data.nome_imagem_vert || data.nome_imagem_quad;
    
    if (!hasImages) {
        imagesContainer.innerHTML = '<p>Nenhuma imagem foi gerada</p>';
        return;
    }
    
    if (data.nome_imagem_vert) {
        const imgDiv = createImageItem(
            `Vertical (1080x1920)`,
            `/outputs/${outputDir}/imagens/${data.nome_imagem_vert}`,
            data.nome_imagem_vert
        );
        imagesContainer.appendChild(imgDiv);
    }
    
    if (data.nome_imagem_quad) {
        const imgDiv = createImageItem(
            `Quadrada (1080x1080)`,
            `/outputs/${outputDir}/imagens/${data.nome_imagem_quad}`,
            data.nome_imagem_quad
        );
        imagesContainer.appendChild(imgDiv);
    }
    
    // Mostrar botão de download de imagens
    if (hasImages) {
        document.getElementById('btn-download-images').style.display = 'inline-block';
    }
}

function createImageItem(title, src, filename) {
    const div = document.createElement('div');
    div.className = 'image-item';
    
    const img = document.createElement('img');
    img.src = src;
    img.alt = title;
    img.onerror = () => {
        img.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect fill="%23ddd" width="100" height="100"/%3E%3Ctext x="50" y="50" text-anchor="middle" dy=".3em"%3EImagem não disponível%3C/text%3E%3C/svg%3E';
    };
    
    const h4 = document.createElement('h4');
    h4.textContent = title;
    
    const p = document.createElement('p');
    p.textContent = filename;
    p.style.fontSize = '0.875rem';
    p.style.color = 'var(--text-light)';
    
    div.appendChild(img);
    div.appendChild(h4);
    div.appendChild(p);
    
    return div;
}

function switchTab(tabName) {
    // Desativar todas as tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    
    // Ativar tab selecionada
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    document.getElementById(`tab-${tabName}`).classList.add('active');
}

function esconderResultados() {
    resultsContainer.style.display = 'none';
}

function downloadJSON() {
    if (!resultadoAtual) return;
    
    const dataStr = JSON.stringify(resultadoAtual, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `conteudo_${resultadoAtual.id_conteudos}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
}

function downloadImages() {
    if (!resultadoAtual || !outputDir) return;
    
    // Criar downloads individuais para cada imagem
    const images = [];
    
    if (resultadoAtual.nome_imagem_vert) {
        images.push({
            url: `/outputs/${outputDir}/imagens/${resultadoAtual.nome_imagem_vert}`,
            filename: resultadoAtual.nome_imagem_vert
        });
    }
    
    if (resultadoAtual.nome_imagem_quad) {
        images.push({
            url: `/outputs/${outputDir}/imagens/${resultadoAtual.nome_imagem_quad}`,
            filename: resultadoAtual.nome_imagem_quad
        });
    }
    
    // Download cada imagem
    images.forEach(img => {
        const link = document.createElement('a');
        link.href = img.url;
        link.download = img.filename;
        link.click();
    });
}

// Prevenir fechamento acidental durante processamento
window.addEventListener('beforeunload', (e) => {
    if (btnGerar.disabled) {
        e.preventDefault();
        e.returnValue = '';
    }
});
