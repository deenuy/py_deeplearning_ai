.PHONY: setup test lint format clean run docs docker-build docker-run mkdocs-setup mkdocs-serve mkdocs-build

# Variables
PYTHON = python3
PIP = $(PYTHON) -m pip
PYTEST = pytest
FLAKE8 = flake8
BLACK = black
UVICORN = uvicorn
MKDOCS = mkdocs

# Directories
SRC_DIR = src
API_DIR = api
TEST_DIR = tests
DOCS_DIR = docs

# Setup
setup:
	$(PIP) install -r requirements.txt

# Testing
test:
	$(PYTEST) $(TEST_DIR)

# Linting
lint:
	$(FLAKE8) $(SRC_DIR) $(API_DIR)

# Formatting
format:
	$(BLACK) $(SRC_DIR) $(API_DIR) $(TEST_DIR)

# Cleaning
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf $(DOCS_DIR)/site

# Run FastAPI server
run:
	$(UVICORN) api.app:app --reload

# Docker
docker-build:
	docker build -t logistic-regression-classifier .

docker-run:
	docker run -p 8000:8000 -p 8080:8080 logistic-regression-classifier

# Data processing
process-data:
	$(PYTHON) $(SRC_DIR)/data/data_processing.py

# Model training
train:
	$(PYTHON) $(SRC_DIR)/train.py

# Model evaluation
evaluate:
	$(PYTHON) $(SRC_DIR)/evaluate.py

# Documentation with MkDocs
mkdocs-setup:
	$(PIP) install mkdocs mkdocs-material
	$(MKDOCS) new $(DOCS_DIR)

mkdocs-serve:
	$(MKDOCS) serve -f $(DOCS_DIR)/mkdocs.yml

mkdocs-build:
	$(MKDOCS) build -f $(DOCS_DIR)/mkdocs.yml

# All
all: setup lint format test mkdocs-build

# Help
help:
	@echo "Available commands:"
	@echo "  make setup         : Install dependencies"
	@echo "  make test          : Run tests"
	@echo "  make lint          : Run linter"
	@echo "  make format        : Format code"
	@echo "  make clean         : Remove compiled Python files and build artifacts"
	@echo "  make run           : Run FastAPI server"
	@echo "  make docker-build  : Build Docker image"
	@echo "  make docker-run    : Run Docker container"
	@echo "  make process-data  : Run data processing script"
	@echo "  make train         : Train the model"
	@echo "  make evaluate      : Evaluate the model"
	@echo "  make mkdocs-setup  : Set up MkDocs for documentation"
	@echo "  make mkdocs-serve  : Serve MkDocs documentation locally"
	@echo "  make mkdocs-build  : Build MkDocs documentation"
	@echo "  make all           : Run setup, lint, format, test, and build docs"
	@echo "  make help          : Show this help message"