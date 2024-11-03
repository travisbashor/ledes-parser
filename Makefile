# Variables
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Available commands:"
	@echo "  make install        - Install production dependencies."
	@echo "  make install-dev    - Install development dependencies."
	@echo "  make install-test   - Install test dependencies."
	@echo "  make venv           - Create a virtual environment."
	@echo "  make clean-venv     - Remove the virtual environment."
	@echo "  make test           - Run tests."

# Create a virtual environment
venv:
	@python3 -m venv $(VENV_DIR)
	@echo "Virtual environment created at $(VENV_DIR)."

# Install production dependencies
install: venv
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "Production dependencies installed."

# Install development dependencies
install-dev: install
	@$(PIP) install -r requirements-dev.txt
	@echo "Development dependencies installed."

# Install test dependencies
install-test: install
	@$(PIP) install -r requirements-test.txt
	@echo "Test dependencies installed."

# Clean up the virtual environment
clean-venv:
	@rm -rf $(VENV_DIR)
	@echo "Virtual environment removed."

# Run tests
test: install-test
	@$(PYTHON) -m pytest
	@echo "Tests executed."
