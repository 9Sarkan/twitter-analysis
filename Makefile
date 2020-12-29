startDjango:
	python source/manage.py collectstatic --no-input
	python source/manage.py migrate
ifeq ("$(DEBUG_MODE)","True")
	python source/manage.py runserver 0.0.0.0:8000
else
	gunicorn source.wsgi -b 0.0.0.0:8000 --log-level=debug --log-file=-
endif

settings:
	cp source/base/settings.sample.py source/base/settings.py

dockerImage:
	docker build -f deployment/docker/dockerfile -t sample-project:latest .

initSwarm:
	docker swarm init
	docker swarm update --task-history-limit 5

deployToSwarm:
	docker stack deploy --compose-file deployment/docker/docker-compose.yml sample-project-stack

rollingUpdate:
	docker service update --force --image sample-project:latest sample-project-stack_sample-project

env:
	cp ./deployment/.env.sample source/.env

nginxConf:
	cp ./deployment/nginx/nginx.sample.conf ./deployment/nginx/nginx.conf

superUser:
	docker exec -it sample-project-stack_sample-project.1.* ./manage.py createsuperuser

intoPsql:
	docker exec -it sample-project-stack_sample-project ./manage.py dbshell

restartsample-project:
	docker service update --force sample-project-stack_sample-project

restartPostgres:
	docker service update --force sample-project-stack_db

restartNginx:
	docker service update --force sample-project-stack_web-server

secrets:
	@read -p "Enter Postgres DB Name:" postgres_db; \
	read -p "Enter Postgres User Name:" postgres_user; \
	read -p "Enter Postgres User Password:" postgres_passwd; \
	read -p "Enter Django Secret Key:" secret_key; \
	echo $$postgres_db | docker secret create postgres-db -;\
	echo $$postgres_user | docker secret create postgres-user -;\
	echo $$postgres_passwd | docker secret create postgres-passwd -;\
	echo $$secret_key | docker secret create secret-key -
