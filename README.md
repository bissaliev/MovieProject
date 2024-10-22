# BestMovie - сервис о фильмах :movie_camera:

## О проекте

__BestMovie__ - это сайт с описанием популярных и интересных фильмов. Пользователи могут просматривать описание фильма и оценивать их. Так же зарегистрированные пользователи могут добавлять фильмы в список избранных и просматривать после. Доступно комментирование фильмов, с возможностью проголосовать за определенный комментарий. Каждому фильму выставляется определенный рейтинг, основанный на среднем значении проголосовавших пользователей. Возможен поиск по названию фильма. Также доступны фильтрация и сортировка фильмов. Фильмы можно фильтровать по жанрам, диапазону дат, странам и рейтингу. Пользователь может сортировать список фильмов по названию(А-Я, Я-А), рейтингу(на убывание и возрастание) и году выпуска фильма(на убывание и возрастание).

На сайте помимо списков фильмов, представлена возможность просматривать списки участников создания фильмов(Персон которые являются либо актером, либо режиссером). Список персон также возможно фильтровать и сортировать. Фильтрация производится по принадлежности персоны к гендеру и статусу участия его при создании фильма(т.е. либо актер, либо режиссер). Сортировка возможно по фамилии(А-Я, Я-А), имени(А-Я, Я-А) персоны. Пользователь также может добавлять персон в список избранных, а также ставить лайки и дизлайки.

На сайте возможна регистрация, возможность восстановить пароль по ссылке отправленной на электронную почту пользователя.

Также проект имеет свой API с практически теми же возможностями.

На данный момент проект находится на стадии разработки.

## Технологии

- Python
- Django
- DRF
- Pillow

## Как запустить

- Клонируем репозиторий:
  
  ```bash
  git@github.com:bissaliev/MovieProject.git
  ```

- Устанавливаем виртуальное окружение:

  ```bash
  python3 -m venv venv
  ```

- Устанавливаем зависимости:
  
  ```bash
  pip install -r requirements.txt
  ```

- Переходим в директорию с файлом `manage.py`:

  ```bash
  cd movie_sites
  ```

- Выполняем миграции:

  ```bash
  python3 manage.py migrate
  ```

- Запускаем проект на локальном сервере:

  ```bash
  python3 manage.py runserver
  ```

- Теперь проект доступен на [локальном сервере](http://127.0.0.1:8000/)

## Автор

[Биссалиев Олег](https://github.com/bissaliev)
