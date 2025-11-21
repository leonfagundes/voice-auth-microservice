.PHONY: help install run test docker-build docker-up docker-down clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make install       - Instala dependências"
	@echo "  make run           - Executa servidor localmente"
	@echo "  make test          - Executa testes"
	@echo "  make docker-build  - Constrói imagem Docker"
	@echo "  make docker-up     - Inicia containers"
	@echo "  make docker-down   - Para containers"
	@echo "  make clean         - Remove arquivos temporários"

install:
	pip install -r requirements.txt

run:
	python run_local.py

test:
	python test_api.py

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f app

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
