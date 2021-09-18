startDjango:
	python source/manage.py collectstatic --no-input
	python source/manage.py migrate
ifeq ("$(DEBUG_MODE)","True")
	python source/manage.py runserver 0.0.0.0:8000
else
	cd source && gunicorn base.wsgi -b 0.0.0.0:8000 --log-level=debug --log-file=-
endif

settings:
	cp source/base/settings.sample.py source/base/settings.py

dockerImage:
	docker build -f deployment/docker/dockerfile -t twitter-analyser:latest .

initSwarm:
	docker swarm init
	docker swarm update --task-history-limit 5

deployToSwarm:
	docker stack deploy --compose-file deployment/docker/docker-compose.yml twitter-analyser-stack

rollingUpdate:
	docker service update --force --image twitter-analyser:latest twitter-analyser-stack_twitter-analyser

env:
	cp deployment/.env.sample source/.env

nginxConf:
	cp deployment/nginx/nginx.conf.sample deployment/nginx/nginx.conf

superUser:
	docker exec -it $(docker ps -q -f name=twitter-analyser-stack_twitter-analyser) python3 source/manage.py createsuperuser

intoPsql:
	docker exec -it $(docker ps -q -f name=twitter-analyser-stack_twitter-analyser) ./source/manage.py dbshell

restarttwitter-analyser:
	docker service update --force twitter-analyser-stack_twitter-analyser

restartPostgres:
	docker service update --force twitter-analyser-stack_db

restartNginx:
	docker service update --force twitter-analyser-stack_web-server

secrets:
	@read -p "Enter Postgres DB Name:" twitter-analyser_postgres_db; \
	read -p "Enter Postgres User Name:" twitter-analyser_postgres_user; \
	read -p "Enter Postgres User Password:" twitter-analyser_postgres_passwd; \
	read -p "Enter Django Secret Key:" twitter-analyser_secret_key; \
	echo $$twitter-analyser_postgres_db | docker secret create twitter-analyser-postgres-db -;\
	echo $$twitter-analyser_postgres_user | docker secret create twitter-analyser-postgres-user -;\
	echo $$twitter-analyser_postgres_passwd | docker secret create twitter-analyser-postgres-passwd -;\
	echo $$twitter-analyser_secret_key | docker secret create twitter-analyser-secret-key -
