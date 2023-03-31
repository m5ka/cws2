STATIC_DIR = cws2/static
SASS_DIR = $(STATIC_DIR)/sass
SASS = base.sass
CSS_DIR = $(STATIC_DIR)/css
CSS = base.css
SASS_FLAGS = -g -t compressed

LINTER = flake8

ENV = .env
ENV_EXAMPLE = .env.example

TEST = pytest

MANAGE_PY = python manage.py

.PHONY: clean env lint sass watch migrate migrations admin static test serve

clean:
	@echo "🧼 Getting rid of compiled directories."
	@if [ -d "$(CSS_DIR)" ]; then rm -r $(CSS_DIR); fi;

env:
	@if [ -f "$(ENV)" ]; then \
	echo "🔧 Environment file already exists."; \
	else cp $(ENV_EXAMPLE) $(ENV); \
	echo "🔧 Creating new environment file."; fi

lint:
	@echo "🔦 Running code-style linter."
	@if $(LINTER) .; then \
	echo "✅ No code-style issues found."; else \
	echo "❌ Some code-style issues found."; fi

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