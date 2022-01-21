RUN = docker-compose exec -it scheduling_system_web_1

makemigrations:
	$(RUN) python manage.py makemigrations

open_container_bash:
	$(RUN) bash

migrate:
	$(RUN) python manage.py migrate

trans-compile:
	$(RUN) django-admin compilemessages

local-start:
	docker-compose up --build

docker-build:
	docker-compose build

local-stop:
	docker-compose down

local-clean:
	docker-compose down -v

clear-git-cache:
	# remove all files from git cache
	git rm -r --cached .
	git add .
	git commit -m ".gitignore is now working"

freeze-requirements:
	$(RUN) pip freeze > ../requirements.txt