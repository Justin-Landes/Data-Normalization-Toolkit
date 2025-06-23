install:
	pip install -r requirements.txt

lint:
	flake8 src/ tests/

format:
	black src/ tests/

test:
	pytest tests/

run:
	python src/bmi_analyzer/main.py

clean:
	rm -rf __pycache__ .pytest_cache
