# ========== Paths ==========
CPP_DIR=code_parser
CPP_BUILD=$(CPP_DIR)/.build
CPP_BIN=$(CPP_BUILD)/code_parser
PY_DIR=api
VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python3
UVICORN=$(VENV_DIR)/bin/uvicorn
SERVER_URL="h""ttp://localhost:8000/analyze/"
FRONTEND_DIR="frontend"
SOUNDFONT_DIR=soundfonts
SOUNDFONT_FILE=$(SOUNDFONT_DIR)/FluidR3_GM.sf2
SOUNDFONT_ZIP=FluidR3_GM.zip
SOUNDFONT_URL=https://keymusician01.s3.amazonaws.com/FluidR3_GM.zip

# ========== Targets ==========

.PHONY: all setup build run run_frontend clean test lint fmt lint-cpp lint-py fmt-cpp fmt-py fetch check

all: check fetch setup build run

check:
	@echo "🧪 Checking for required tools..."
	@command -v python3.13 >/dev/null 2>&1 || (echo "❌ python3.13 not found"; exit 1)
	@command -v curl >/dev/null 2>&1 || (echo "❌ curl not found"; exit 1)
	@command -v unzip >/dev/null 2>&1 || (echo "❌ unzip not found"; exit 1)
	@command -v cmake >/dev/null 2>&1 || (echo "❌ cmake not found"; exit 1)
	@command -v clang-tidy >/dev/null 2>&1 || echo "⚠️  clang-tidy not found (optional)"
	@command -v clang-format >/dev/null 2>&1 || echo "⚠️  clang-format not found (optional)"
	@command -v fluidsynth >/dev/null 2>&1 || (echo "❌ fluidsynth not found. Please install via: brew install fluid-synth"; exit 1)

fetch:
	@echo "🎧 Checking SoundFont..."
	@if [ ! -f "$(SOUNDFONT_FILE)" ]; then \
		echo "🎼 SoundFont not found. Downloading..."; \
		curl -L $(SOUNDFONT_URL) --output $(SOUNDFONT_ZIP); \
		unzip -o $(SOUNDFONT_ZIP) -d soundfonts; \
		rm -f $(SOUNDFONT_ZIP); \
		echo "✅ SoundFont ready: $(SOUNDFONT_FILE)"; \
	else \
		echo "✅ SoundFont already exists."; \
	fi

setup:
	@echo "🐍 Setting up Python environment..."
	@brew install llvm
	@python3.13 -m venv $(VENV_DIR)
	@$(VENV_DIR)/bin/pip install --upgrade pip
	@$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "✅ Python environment ready."

build:
	@echo "⚙️  Building C++ parser..."
	@mkdir -p $(CPP_BUILD)
	@cd $(CPP_BUILD) && cmake .. && make
	@echo "✅ Build complete."

run:
	@echo "🚀 Starting backend server..."
	@$(UVICORN) api.main:app --reload

run_frontend:
	@echo "🔍 Checking for existing server on port 8080..."
	@lsof -ti:8080 | xargs -r kill
	@echo "🌐 Starting frontend at http://localhost:8080"
	@python3 -m http.server 8080 --directory $(FRONTEND_DIR) &
	@sleep 1
	@open http://localhost:8080

test:
	@echo "📤 Uploading test file..."
	@curl -X POST ${SERVER_URL} -F "file=@test_samples/example.cpp"

clean:
	@echo "🧹 Cleaning project..."
	@rm -rf $(CPP_BUILD)
	@rm -rf $(VENV_DIR)
	@rm -rf ${PY_DIR}/.logs ${PY_DIR}/output/*.mid ${PY_DIR}/output/*.wav
	@rm -f $(SOUNDFONT_ZIP)
	@echo "✅ Cleaned."

# ========== Linting ==========

lint: lint-cpp lint-py

lint-cpp:
	@echo "🔍 Running clang-tidy..."
	@clang-tidy $(CPP_DIR)/*.cpp -- -std=c++17 || true

lint-py:
	@echo "🔍 Running pylint..."
	@$(VENV_DIR)/bin/pylint $(PY_DIR)/*.py || true

fmt: fmt-cpp fmt-py

fmt-cpp:
	@echo "🛠️  Formatting C++..."
	@clang-format -i $(CPP_DIR)/*.cpp

fmt-py:
	@echo "🛠️  Formatting Python..."
	@$(VENV_DIR)/bin/black $(PY_DIR)
