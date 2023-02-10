install:
	python -m pip install --upgrade pip && pip install -U -r requirements.txt

format:
	black .

lint:
	pylint .

clean:
	pyclean -v .

typecheck:
	mypy src
