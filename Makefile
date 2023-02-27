install:
	python -m pip install --upgrade pip && pip install -U -r requirements.txt

install-dev:
	python -m pip install --upgrade pip && pip install -U -r requirements-dev.txt

format:
	black src

lint:
	pylint src/

clean:
	pyclean -v .

type:
	mypy src/apps/stripe

ruff:
	ruff check src/

ruff-watch:
	ruff check src/apps/xero --watch

coverage:
	pytest --cov=tests/ --cov-report=term-missing --cov-report=html
