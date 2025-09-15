run_dev:
	docker compose --env-file vars.dev.env -f docker-compose.yml up

stop_dev:
	docker compose --env-file vars.dev.env -f docker-compose.yml down

build:
	docker compose --env-file vars.dev.env -f docker-compose.yml build

run_tests:
	uv run pytest

run_linter:
	uv run ruff format --force-exclude .
	uv run ruff check --force-exclude .

run_linter_fix:
	uv run ruff format --force-exclude .
	uv run ruff check --fix --force-exclude .

run_app:
	uv run uvicorn main:app --reload --app-dir ./app