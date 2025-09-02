# justfile - Um executor de comandos para o projeto

# Variáveis (podem ser sobrescritas na linha de comando)
PYTHON_INTERPRETER := "python"
SRC_DIR := "src"
TEST_DIR := "tests"

# Instala todas as dependências do projeto
install:
    uv sync

# Roda o linter para verificar a qualidade do código
lint:
    @echo "Linting com ruff..."
    ruff check .
    @echo "Verificando formatação com black..."
    black --check .

# Formata o código automaticamente
format:
    @echo "Formatando com ruff..."
    ruff --fix .
    @echo "Formatando com black..."
    black .

# Roda os testes automatizados
test:
    @echo "Executando testes com pytest..."
    pytest {{TEST_DIR}}

# Inicia a aplicação principal
run:
    @echo "Iniciando a aplicação..."
    {{PYTHON_INTERPRETER}} {{SRC_DIR}}/main.py

# Limpa arquivos de cache e build
clean:
    @echo "Limpando arquivos de cache..."
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -delete
    rm -rf .pytest_cache .ruff_cache .mypy_cache build dist *.egg-info
