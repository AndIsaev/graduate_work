[![Voice assistent](https://github.com/AndIsaev/graduate_work/actions/workflows/main.yml/badge.svg)](https://github.com/AndIsaev/graduate_work/actions/workflows/main.yml)
![redis](https://img.shields.io/badge/redis-%23DD0031.svg?&style=badge&logo=redis&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=badge&logo=postgresql&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-14354C?style=badge&logo=python&logoColor=white)
![Elasticsearch](https://badges.aleen42.com/src/elasticsearch.svg)
![Fastapi](https://img.shields.io/badge/Fastapi-000000?style=badge&logo=fastapi&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-000000?style=badge&logo=nginx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=badge&logo=docker&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-000000?.svg?style=Gunicorn&logo=Gunicorn&logoColor=green)

###[Ссылка на проект](https://github.com/AndIsaev/graduate_work)

# Техническое задание дипломной работы "Голосовой ассистент"

- Цели проекта
- Задачи "Голосового ассистента"
- Требования к программе
- Стек технологий
- Стадии и этапы разработки


## Цели проекта

- Демонстрация приобретенных навыков за время прохождения курса от Яндекс практикум "Python Middle developer"
- Исследование и создание на основе технологии голосового помощника для поиска фильмов, дополнительной информации о фильме, актерах и тп.

## Проблематика

Для упрощенного взаимодействия пользователя онлайн-кинотеатра с сервисом, предлагается дополнить функциональность голосовым помощником. Работа данного функционала поможет пользователю сократить время на ввод поискового запроса, упростить получение информации о фильме и тп. Особенно актуально использование голосового помощника будет пользователям, пользующимися онлайн-кинотеатр через смарт-тв, так как время ввода запроса с использованием пульта ДУ значительно больше времени, затраченного на ввод запроса с клавиатуры или пульта.


## Ограничения

На этапе проектирования системы предполагается использовать только ассистента «Алиса», в дальнейшем возможно подключить «Сири», «Алексу», «Марусю» и тп. В дальнейшем, возможно разделение сообщающего контента в зависимости от пользователя (пола, возраста и тп) и оплата подписок или покупок через ассистента.


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


# Схема
![Schema](https://github.com/AndIsaev/graduate_work/blob/develop/schema/schema.png)


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
