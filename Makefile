run:
	uv run manage.py runserver

lint:
	uv run pre-commit run --all-files
