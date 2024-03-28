STATIC_DIR = cws2/static
SASS_DIR = $(STATIC_DIR)/scss
SASS = base.scss
CSS_DIR = $(STATIC_DIR)/css
CSS = base.css
SASS_FLAGS = -g -t compressed

ENV = .env
ENV_EXAMPLE = .env.example

RUN = poetry run
TEST = $(RUN) pytest
MANAGE = $(RUN) python manage.py

.PHONY: clean env lint format sass watch migrate migrations admin static test serve servelan

clean:
	@echo "🧼 Getting rid of compiled directories."
	@if [ -d "$(CSS_DIR)" ]; then rm -r $(CSS_DIR); fi;

env:
	@if [ -f "$(ENV)" ]; then \
	echo "🔧 Environment file already exists."; \
	else cp $(ENV_EXAMPLE) $(ENV); \
	echo "🔧 Creating new environment file."; fi

lint:
	@echo "🛀 Checking linter..."
	@$(RUN) ruff check .
	@$(RUN) ruff format --check .

format:
	@echo "🦄 Formatting Python files."
	@$(RUN) ruff format .
	@echo "👍️ Python files have been formatted."

sass:
	@echo "🎨 Compiling SASS to CSS."
	@$(MANAGE) sass $(SASS_DIR)/$(SASS) $(CSS_DIR)/$(CSS) $(SASS_FLAGS)

watch:
	@echo "🎨 Watching to compile SASS to CSS."
	@$(MANAGE) sass $(SASS_DIR)/$(SASS) $(CSS_DIR)/$(CSS) $(SASS_FLAGS) --watch

migrate:
	@echo "📁 Running migrations."
	@$(MANAGE) migrate

migrations:
	@echo "🧩 Checking for model changes."
	@$(MANAGE) makemigrations

admin:
	@echo "👤 Let's make an admin account!"
	@$(MANAGE) createsuperuser

static:
	@echo "🗃️ Collecting static files."
	@$(MANAGE) collectstatic

test:
	@echo "🧪 Running tests."
	@ if $(TEST); then \
	echo "✅ All tests passed."; else \
	echo "❌ Some tests failed."; fi

serve:
	@echo "💻️ Running development server"
	@$(MANAGE) runserver

servelan:
	@echo "💻️ Running development server (LAN accessible)"
	@$(MANAGE) runserver 0.0.0.0:8000