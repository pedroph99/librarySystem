# Makefile para iniciar o servidor backend

# Declara os alvos como "phony" (falsos), o que significa que eles não são arquivos reais.
# Isso garante que o 'make' sempre executará os comandos, mesmo que exista um arquivo
# ou pasta com o nome 'dev' ou 'prod'.
VENV_PYTHON = ./venv/bin/python
VENV_PIP = ./venv/bin/pip

include .env
export

.PHONY: dev prod help update

# Alvo padrão: Se você digitar apenas 'make', ele mostrará a ajuda.
default: help

## dev: Inicia o servidor em modo de DESENVOLVIMENTO com auto-reload.
dev:
	@echo "🚀 Iniciando servidor de DESENVOLVIMENTO (http://127.0.0.1:8000)..."
	$(VENV_PYTHON) -m uvicorn librarySystem.api.main:app --reload --host 127.0.0.1 --port 8000

## prod: Inicia o servidor em modo de PRODUÇÃO com 4 workers.
prod:
	@echo "📦 Iniciando servidor de PRODUÇÃO (http://0.0.0.0:8000)..."
	$(VENV_PYTHON) -m uvicorn librarySystem.api.main:app --workers 4 --host 0.0.0.0 --port 8000

update:
	@echo "📦  Sincronizando ambiente com requirements.txt..."
	$(VENV_PIP) install -r requirements.txt
	@echo "✅  Ambiente atualizado."

## add: Adiciona um novo pacote ao requirements.txt e instala.
##      Previne a adição de duplicatas.
##      Uso: make add PKG="fastapi==0.100.0"
add:
ifeq ($(PKG),)
	@echo "❌ Erro: Forneça o nome do pacote. Exemplo: make add PKG=requests"
	@exit 1
else
	@echo "🔎  Verificando se '$(PKG)' já existe em requirements.txt..."
	@# O comando grep verifica se o pacote (no início da linha ^) já existe.
	@# O -q faz ele ficar quieto (não mostrar output) e -E usa regex.
	@if grep -q -E "^$(PKG)" requirements.txt; then \
		echo "✅  Pacote '$(PKG)' já está na lista. Rodando 'make update' para garantir a instalação..."; \
		$(MAKE) update; \
	else \
		echo "➕  Adicionando '$(PKG)' a requirements.txt..."; \
		echo "$(PKG)" >> requirements.txt; \
		$(MAKE) update; \
	fi
endif	
    
	
## help: Mostra esta mensagem de ajuda.
help:
	@echo "Uso: make [alvo]"
	@echo ""
	@echo "Alvos disponíveis:"
	@echo "  \033[36mdev\033[0m          - Inicia o servidor em modo de desenvolvimento."
	@echo "  \033[36mprod\033[0m         - Inicia o servidor em modo de produção."
	@echo "  \033[36mhelp\033[0m         - Mostra esta mensagem de ajuda."
