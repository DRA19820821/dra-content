@echo off
REM Script de inicialização do Marketing AI System (Windows)

echo.
echo ============================================
echo   Marketing AI System - Inicializando...
echo ============================================
echo.

REM Verificar se .env existe
if not exist ".env" (
    echo [ERRO] Arquivo .env nao encontrado!
    echo.
    echo Copie o .env.example e configure suas API keys:
    echo    copy .env.example .env
    echo.
    pause
    exit /b 1
)

REM Verificar se venv existe
if not exist "venv\" (
    echo [AVISO] Ambiente virtual nao encontrado
    echo.
    echo Recomendamos criar um ambiente virtual:
    echo    python -m venv venv
    echo    venv\Scripts\activate
    echo    pip install -r requirements.txt
    echo.
    set /p continue="Continuar mesmo assim? (S/N): "
    if /i not "%continue%"=="S" exit /b 1
)

echo.
echo [OK] Verificando dependencias...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [AVISO] Dependencias nao instaladas
    echo Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo ============================================
echo   Tudo pronto!
echo ============================================
echo.
echo Servidor sera iniciado em: http://localhost:8000
echo Pressione Ctrl+C para parar o servidor
echo.
echo ============================================
echo.

REM Iniciar servidor
python app.py

pause
