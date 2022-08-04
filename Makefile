run:
	/bin/bash make_secret.sh
	echo запускаем контейнеры
	docker-compose build
	docker-compose up -d
	echo контейнеры запущены

stop:
	docker-compose stop

down:
	docker-compose down
