run:
	uv run manage.py runserver

startapp:
	uv run manage.py startapp $(name)

createsuperuser:
	uv run manage.py createsuperuser

makemigrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

lint:
	uv run pre-commit run --all-files

print_posts:
	uv run manage.py print_posts

print_published_posts:
	uv run manage.py print_published_posts

create_post:
	uv run manage.py create_post -t "$(title)" -c "$(content)"

delete_post:
	uv run manage.py delete_post $(id)

update_post:
	uv run manage.py update_post $(id) -t "$(title)"

shell_plus:
	uv run manage.py shell_plus --print-sql

test_all:
	uv run manage.py test

docker-build:
	docker build -t blog_image .

docker-create-network:
	docker network create blog_net

docker-up-blog:
	docker run --name blog --network blog_net -p 8000:8000 \
	  -v ./media:/app/media \
	  --env-file .env \
	  -e DATABASE_URL=postgres://admin:admin@blog_db:5432/blog_db \
  	  -e ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0 \
	  -d blog_image

docker-down:
	docker rm -f blog

docker-migrate:
	docker exec blog uv run manage.py migrate

docker-up-blog_db:
	docker run \
	  --name blog_db \
	  --network blog_net \
	  -e POSTGRES_USER=admin \
	  -e POSTGRES_PASSWORD=admin \
	  -e POSTGRES_DB=mydb \
	  -v blog_db_data:/var/lib/postgresql/data \
	  -d postgres:17
