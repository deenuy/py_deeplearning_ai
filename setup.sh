#!/bin/bash

# Define the root directory for the project
ROOT_DIR="/Users/deenuy/Documents/Workspace/Pet-projects/python_repos/py_deeplearning_ai"

# Create directories
mkdir -p "$ROOT_DIR"/{api/models,build,ci,config/{dev,prod,stage},deployment/{docker,gitops,helm,openshift,pipelines},docs,infrastructure,manifests,src/{data,datasets/{bronze,silver,gold},experiments,evaluation,models,notebooks,scripts/{tests,training},utils},ui,monitoring,feature_store,security,data_validation,environments,releases,load_testing,drift_detection}

# Create essential files
touch "$ROOT_DIR"/{.gitignore,Makefile,README.md,Dockerfile,requirements.txt,pyproject.toml,CHANGELOG.md,.pre-commit-config.yaml}

# Create linting and formatting config files
touch "$ROOT_DIR"/{.flake8,.pylintrc,.black}

# Create environment files
touch "$ROOT_DIR/environments"/{dev.env,stage.env,prod.env}

# Create API versioning directories
mkdir -p "$ROOT_DIR/api"/{v1,v2}

# Create example configuration files
echo "DEBUG=True" > "$ROOT_DIR/config/dev/config.env"
echo "DEBUG=False" > "$ROOT_DIR/config/prod/config.env"

# Create a basic README.md
cat << EOF > "$ROOT_DIR/README.md"
# ML Project

This is a containerized production-grade machine learning project.

## Project Structure

[Insert project structure here]

## Setup

[Insert setup instructions here]

## Usage

[Insert usage instructions here]

## Contributing

[Insert contribution guidelines here]

## License

[Insert license information here]
EOF

# Create a basic .gitignore
cat << EOF > "$ROOT_DIR/.gitignore"
# Python
__pycache__/
*.py[cod]
*.so

# Environments
.env
.venv
env/
venv/
ENV/

# Jupyter Notebook
.ipynb_checkpoints

# IDEs
.vscode/
.idea/

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
/src/datasets/
/src/models/
EOF

# Create a basic Makefile
cat << EOF > "$ROOT_DIR/Makefile"
.PHONY: setup test lint format

setup:
	pip install -r requirements.txt

test:
	pytest src/scripts/tests

lint:
	flake8 src

format:
	black src
EOF

# Display project structure
echo "Project structure created successfully!"
if command -v tree &> /dev/null; then
    tree "$ROOT_DIR"
else
    find "$ROOT_DIR" -print | sed -e "s;$ROOT_DIR;.;g;s;[^/]*/;|____;g;s;____|; |;g"
fi