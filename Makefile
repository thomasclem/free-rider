

# PROJECT SETUP COMMANDS
install: requirements.txt  ## install project dependencies (requirements.txt)
	pip install -r requirements.txt
	touch install

install-dev: install requirements.dev.txt  ## install developpment dependencies (for testing, linting etc.)
	pip install -r requirements.dev.txt
	touch install-dev

activate: ## initiate virtual environment
	bash activate.sh
	touch activate

init: ## initiate virtual environment
	bash init.sh
	touch init
