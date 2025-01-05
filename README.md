# Проект YaMDb

## Описание проекта:

YaMBd - API-платформа для сбора отзывов пользователй на различные произведений. Произведения делятся на категории, такие как "Книги", "Фильмы", "Музыка". Пользователи могут оставлять отзывы с оценками, комментировать и просматривать рейтинги произведений.

## Авторы и разработчики:

* *Яндекс Практикум (автор проекта):*  [Сайт](https://practicum.yandex.ru/)
* *Валерия Маданова (backend developer):* [Github](https://github.com/vlrmdn)
* *Дмитрий Корноухов (backend developer):* [Github](https://github.com/jpgIKenpachi)
* *Олег Ритум (backend developer):* [Github](https://github.com/oritum)

  Тимлид:*Олег Ритум*

  Год разработки: *2025.*

## Стек технологий:

* Python 3.9
* Django 3.2
* Django Rest Framework 3.12.4
* Simple JWT 5.3.1

## Развертывание проекта

#### Шаг 1: Клонирование репозитория

```shell
git clone git@github.com:<username>/api_yamdb.git
```

```shell
cd api_yamdb
```

#### Шаг 2: Создание и активация виртуального окружения

```shell
python3 -m venv venv
```

```shell
source venv/bin/activate
```

#### Шаг 3: Установка зависимостей

```shell
python3 -m pip install --upgrade pip
```

```shell
pip install -r requirements.txt
```

#### Шаг 4: Применение миграций

```shell
python manage.py migrate
```

#### Шаг 5: Создание файла с переменными окружения `.env`

```shell
touch .env
```

###### Требуемые переменные:

```shell
EMAIL_HOST=
EMAIL_PORT= 
EMAIL_USE_TLS= 
EMAIL_USE_SSL= 
EMAIL_HOST_USER= 
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
```

#### Шаг 6: Запуск сервера разработки

```shell
python manage.py runserver
```

## Основной функционал:

* **Регистрация и аутентификация:**
  * Регистрация нового пользователя с отправкой confirmation_code на email.
  * Получение JWT-токена для авторизации.
* **Категории, жанры и произведения:**
  * Просмотр списка категорий, жанров и произведений.
  * Администраторы могут добавлять, изменять и удалять категории, жанры и произведения.
* **Отзывы и комментарии:**
  * Создание, редактирование и удаление отзывов и комментариев к ним.
  * Просмотр отзывов и комментариев.
  * Модератор и администратор имеют право удалять любые отзывы и комментарии.
* **Управление пользователями:**
  * Администраторы могут управлять ролями и профилями пользователей.

#### Пользовательские роли

* **Аноним:** может просматривать описания произведений, отзывы и комментарии.
* **Аутентифицированный пользователь:** может оставлять отзывы и комментарии, редактировать и удалять их.
* **Модератор:** имеет право удалять отзывы и комментарии других пользователей.
* **Администратор:** полный доступ ко всем данным и управлению проектом.


## Примеры некоторых запросов и ответов к API (подробная документация API доступна по адресу `/redoc/`  после запуска проекта.)

#### Регистрация нового пользователя

**Запрос:**

```json
POST .../api/v1/auth/signup/

{
  "email": "user@example.com",
  "username": "^w\\Z"
}
```

**Ответ:**

```json
{
  "email": "string",
  "username": "string"
}
```

#### Получение JWT-токена

**Запрос:**

```json
POST .../api/v1/auth/token/

{
  "username": "^w\\Z",
  "confirmation_code": "string"
}
```

**Ответ:**

```json
{
  "token": "string"
}
```

#### Получение списка всех категорий

**Запрос:**

```json
GET .../api/v1/categories/
```

**Ответ:**

```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "^-$"
    }
  ]
}
```

#### Добавление новой категории

**Запрос:**

```json
POST .../api/v1/categories/

{
  "name": "string",
  "slug": "^-$"
}
```

**Ответ:**

```json
{
  "name": "string",
  "slug": "string"
}
```

#### Добавление жанра

**Запрос:**

```json
POST .../api/v1/genres/

{
  "name": "string",
  "slug": "^-$"
}
```

#### **Ответ:**

```json
{
  "name": "string",
  "slug": "string"
}
```

#### Получение списка всех произведений

**Запрос:**

```json
GET .../api/v1/titles/
```

**Ответ:**

```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "^-$"
        }
      ],
      "category": {
        "name": "string",
        "slug": "^-$"
      }
    }
  ]
}
```

#### Частичное обновление отзыва по id

**Запрос:**

```json
PATCH .../api/v1/titles/{title_id}/reviews/{review_id}/

{
  "text": "string",
  "score": 1
}
```

**Ответ:**

```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

#### Получение комментария к отзыву

**Запрос:**

```json
GET .../api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

**Ответ:**

```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

#### Изменение данных своей учетной записи

**Запрос:**

```json
PATCH .../api/v1/users/me/

{
  "username": "^w\\Z",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```

**Ответ:**

```json
{
  "username": "^w\\Z",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
