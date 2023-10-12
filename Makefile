STATIC_DIR = cws2/static
SASS_DIR = $(STATIC_DIR)/scss
SASS = base.scss
CSS_DIR = $(STATIC_DIR)/css
CSS = base.css
SASS_FLAGS = -g -t compressed

ENV = .env
ENV_EXAMPLE = .env.example

TEST = pytest

MANAGE_PY = python manage.py

.PHONY: clean env lint check_flake8 check_black check_isort flake8 black isort format sass watch migrate migrations admin static test serve servelan

clean:
	@echo "🧼 Getting rid of compiled directories."
	@if [ -d "$(CSS_DIR)" ]; then rm -r $(CSS_DIR); fi;

env:
	@if [ -f "$(ENV)" ]; then \
	echo "🔧 Environment file already exists."; \
	else cp $(ENV_EXAMPLE) $(ENV); \
	echo "🔧 Creating new environment file."; fi

lint: check_flake8 check_black check_isort

check_flake8:
	@if flake8 --format quiet-nothing .; \
	then echo "✅ flake8 passed."; \
	else echo "❌ flake8 failed. Run \`make flake8\` for more information."; \
	fi

check_black:
	@if black -q --check .; \
	then echo "✅ black passed."; \
	else echo "❌ black failed. Run \`make black\` for more information."; \
	fi

check_isort:
	@if isort -q -c . 2>/dev/null; \
	then echo "✅ isort passed."; \
	else echo "❌ isort failed. Run \`make isort\` for more information."; \
	fi

flake8:
	@flake8 .

black:
	@black --check .
	@echo "Run \`make format\` to automatically format files."

isort:
	@isort -c .
	@echo "Run \`make format\` to automatically format files."

format:
	@echo "🦄 Formatting Python files."
	@black .
	@isort .
	@echo "👍️ Python files have been formatted."

sass:
	@echo "🎨 Compiling SASS to CSS."
	@$(MANAGE_PY) sass $(SASS_DIR)/$(SASS) $(CSS_DIR)/$(CSS) $(SASS_FLAGS)

watch:
	@echo "🎨 Watching to compile SASS to CSS."
	@$(MANAGE_PY) sass $(SASS_DIR)/$(SASS) $(CSS_DIR)/$(CSS) $(SASS_FLAGS) --watch

migrate:
	@echo "📁 Running migrations."
	@$(MANAGE_PY) migrate

migrations:
	@echo "🧩 Checking for model changes."
	@$(MANAGE_PY) makemigrations

admin:
	@echo "👤 Let's make an admin account!"
	@$(MANAGE_PY) createsuperuser

static:
	@echo "🗃️ Collecting static files."
	@$(MANAGE_PY) collectstatic

test:
	@echo "🧪 Running tests."
	@ if $(TEST); then \
	echo "✅ All tests passed."; else \
	echo "❌ Some tests failed."; fi

serve:
	@echo "💻️ Running development server"
	@$(MANAGE_PY) runserver

servelan:
	@echo "💻️ Running development server (LAN accessible)"
	@$(MANAGE_PY) runserver 0.0.0.0:8000