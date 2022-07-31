[![Voice assistent](https://github.com/AndIsaev/graduate_work/actions/workflows/main.yml/badge.svg)](https://github.com/AndIsaev/graduate_work/actions/workflows/main.yml)

![redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![Elastic_Search](https://img.shields.io/badge/Elastic_Search-005571?style=for-the-badge&logo=elasticsearch&logoColor=white)
![Fastapi](https://img.shields.io/badge/Fastapi-000000?style=for-the-badge&logo=fastapi&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-000000?style=for-the-badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)


# Техническое задание дипломной работы "Голосовой ассистент"

- Цели проекта
- Задачи "Голосового ассистента"
- Требования к программе
- Стек технологий
- Стадии и этапы разработки


## Цели проекта

Основная цель данной работы заключается в демонстрации приобритенных навыков за время прохождения курса от Яндекс практикум "Python Middle developer"


## Задачи "Голосового ассистента"

- Реагирует на голосовой запрос со стороны клиента
- Производит поиск запроса в базе данных
- При находении результата - зачитывает его клиенту
- Если результатов несколько - зачитывает первый результат

## Требования к программе:
 - Программа реализована посредством языка Python
 - Соблюдены стандарты pep8
 - Реализован CI/CD с проверкой кода на его соответствие со стандартами pep8
 - Сервисы являются отказоустойчивыми и не зависимы друг от друга
 - Все ошибки обработаны и отдают соответствующие статусы
 - Реализовано логирование операций
 - Весь функционал протестирован
 - Все сервисы поднимаются посредством контейнерезации в Docker
 - Реализован план разработки "Голосового ассистента"
 - Представлена схема приложения (архитектура)


## Стек технологий

- Python
- ElasticSearch
- Django
- FastAPI
- PostgresSQL
- Yandex Cloud

# Запустить проект

### Создайте .env файл и скопируйте данные с env.example
````
touch .env
````

````
nano .env
````

### Запускаем последовательно команды
````
docker-compose build
````

````
docker-compose up -d
````
