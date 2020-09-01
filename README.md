![yamdb workflow](https://github.com/idesu/yamdb_final/workflows/yamdb%20workflow/badge.svg)
# Докеризация API для Ya|MDb. Интернет-сервис о кино на базе Django REST

Тренировочный проект в рамках учебного курса Яндекс.Практикум


## Установка

#### Шаг первый. Проверьте установлен ли у вас Docker и docker-compose

```bash
docker -v
```
Если у вас все еще не установлен Docker и вы используете Linux, то воспользуйтесь скриптом:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh # эта команда запустит его
```
Если же у вас другая ОС, то воспользуйтесь официальной [инструкцией](https://docs.docker.com/engine/install/).

Далее также проверяем наличие docker-compose:
```bash
docker-compose -v
```
Если у вас не установлен docker-compose и вы пользователь системы Linux, то вы можете установить его из официального репозитория:
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/ \
    docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

#Как только завершилась установка, измените права доступа права доступа
sudo chmod +x /usr/local/bin/docker-compose
```

#### Шаг второй. Запуск контейнера
```bash
docker-compose up
```
#### Шаг третий. База данных
```bash
docker-compose run web python manage.py migrate --no-input
```
## Использование
### Создание суперпользователя Django
```bash
docker-compose run web python manage.py createsuperuser
```
### Импорт стартовых данных из json
```bash
docker-compose run web python manage.py loaddata path/to/your/json
```
### Остановка контейнеров
```bash
docker-compose down
```

### Полезные ссылки:
[Docker cheatsheet](http://dockerlabs.collabnix.com/docker/cheatsheet/) <br>

[Django loaddata документация](https://docs.djangoproject.com/en/3.0/ref/django-admin/#django-admin-dumpdata) <br>

[README API_YaMDb](https://github.com/Gregog/api_yamdb/blob/master/README.md) <br>
