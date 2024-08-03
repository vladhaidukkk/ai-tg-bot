default: lint fmt

run:
	python -m bot.main

fmt:
	ruff format

lint:
	ruff check

fix:
	ruff check --fix

revise msg:
    alembic revision --autogenerate -m "{{msg}}"

migrate target="head":
    alembic upgrade {{target}}

revert target="-1":
    alembic downgrade {{target}}
