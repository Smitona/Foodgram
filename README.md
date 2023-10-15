# Foodgram
Площадка, чтобы поделиться рецептами с фото.


*Сайт доступен по ссылке [projectforpracticum.myftp.biz/recipes/](http://projectforpracticum.myftp.biz/recipes/)*
#### Доступ в админку [projectforpracticum.myftp.biz/recipes/admin/](https://projectforpracticum.myftp.biz/admin/):

Логин — `admn@ya.ru`

Пароль — `admin123`


### Зарегстрировавшись, вы получаете возможность:
* Опубликовать рецепт с фото и ингредиентами. Ингредиенты есть в базе.
* Добавить рецепт в избранное.
* Положить рецепт в корзину. Скачать файл с необходимыми продуктами для приготовления рецептов. Ингредиенты суммируются.
* Подписаться на авторов, чтобы следить за обновлениями и иметь к ним быстрый доступ.

### Примеры запросов:

#### GET /api/recipes/1/

```
{
    "id": 1,
    "tags": [
        {
            "id": 1,
            "name": "Завтрак",
            "color": "#98D919",
            "slug": "zavtrak"
        }
    ],
    "author": {
        "email": "petya@ya.ru",
        "id": 2,
        "username": "petya",
        "first_name": "Петя",
        "last_name": "Петров",
        "is_subscribed": false
    },
    "ingredients": [
        {
            "id": 948,
            "name": "малиновый чай",
            "measurement_unit": "г",
            "amount": 20
        },
        {
            "id": 609,
            "name": "кипяток",
            "measurement_unit": "г",
            "amount": 500
        }
    ],
    "image": "http://projectforpracticum.myftp.biz/media/recipes/images/c357bca7-d9fd-4e97-ae5c-218cf1a030a3.png",
    "name": "Малиновый чай",
    "text": "Вскипятить воду. Насыпать в чайник 20г чая с малиной. Залить и дать настояться.",
    "cooking_time": 8,
    "is_favorited": false,
    "is_in_shopping_cart": false
}
```

#### POST /api/users/2/subscribe/
```
{
    "email": "petya@ya.ru",
    "id": 2,
    "username": "petya",
    "first_name": "Петя",
    "last_name": "Петров",
    "recipes": [
        {
            "id": 2,
            "name": "Яичница с помидорами и перцем",
            "image": "http://projectforpracticum.myftp.biz/media/recipes/images/a28d88c3-3835-4eab-821a-01a82b1ebc30.png",
            "cooking_time": 8
        },
        {
            "id": 1,
            "name": "Малиновый чай",
            "image": "http://projectforpracticum.myftp.biz/media/recipes/images/c357bca7-d9fd-4e97-ae5c-218cf1a030a3.png",
            "cooking_time": 8
        }
    ],
    "recipes_count": 2
}
```
_____________________________________________________________________________________________________________________________________________

Проект работает на основе Django REST Framework.
