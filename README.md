# Foodgram
Площадка, чтобы поделиться рецептами с фото.


*Сайт доступен по ссылке [127.0.0.1/recipes/](http://127.0.0.1/recipes/)*
#### Доступ в админку:

admn@ya.ru

admin123


### Зарегстрировавшись, вы получаете возможность:
* Опубликовать рецепт с фото и ингредиентами. Ингредиенты есть в базе.
* Добавить рецепт в избранное.
* Положить рецепт в корзину. Скачать файл с необходимыми продуктами для приготовления рецептов. Ингредиенты суммируются.
* Подписаться на авторов, чтобы следить за обновлениями и иметь к ним быстрый доступ.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:Smitona/foodgram-project-react.git
```
```
cd foodgram-project-react/
```

Создать и активировать вирутальное окружение версией python:
```
python -m venv venv
```

```
source venv/Scripts/activate   #for Windows
```
```
source venc/bin/activate       #for Linux
```

Установить необходимы зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Запустить контейнеры из папки infra:
```
cd infra/
```
```
docker compose up
```

Выполнить миграции внутри контейнера бэкенда, загрузить ингредиенты:
```
docker compose exec backend python manage.py migrate
```
```
docker compose exec backend python manage.py import_ingredients
```

Собрать статику проекта и скопировать её для отображения:
```
docker compose exec backend python manage.py collectstatic
```
```
docker compose exec backend cp -r /app/collected_static/. /app/backend_static/static/ #in powershell
```
_____________________________________________________________________________________________________________________________________________

Проект работает на основе Django REST Framework. На данном этапе он работает только локально.
