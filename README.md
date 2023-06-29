# Django site

Докеризированный сайт на Django для экспериментов с Kubernetes.

Внутри конейнера Django запускается с помощью Nginx Unit, не путать с Nginx. Сервер Nginx Unit выполняет сразу две функции: как веб-сервер он раздаёт файлы статики и медиа, а в роли сервера-приложений он запускает Python и Django. Таким образом Nginx Unit заменяет собой связку из двух сервисов Nginx и Gunicorn/uWSGI. [Подробнее про Nginx Unit](https://unit.nginx.org/).

[Рабочий сайт](https://edu-trusting-bartik.sirius-k8s.dvmn.org/admin/)


## Задайте переменные окружения в файл .env

`SECRET_KEY` -- обязательная секретная настройка Django. Это соль для генерации хэшей. Значение может быть любым, важно лишь, чтобы оно никому не было известно. [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key).

`DEBUG` -- настройка Django для включения отладочного режима. Принимает значения `TRUE` или `FALSE`. [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-DEBUG).

`ALLOWED_HOSTS` -- настройка Django со списком разрешённых адресов. Если запрос прилетит на другой адрес, то сайт ответит ошибкой 400. Можно перечислить несколько адресов через запятую, например `127.0.0.1,192.168.0.1,site.test`. [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts).

`DATABASE_URL` -- адрес для подключения к базе данных PostgreSQL. Другие СУБД сайт не поддерживает. [Формат записи](https://github.com/jacobian/dj-database-url#url-schema).



## Как запустить в кластере
- В файле `.\kubernetes\deployment.yml` указан образ, с которого будут запускаться поды: `image: nstonic/test_django_app:latest`. Все теги можно найти по [ссылке](https://hub.docker.com/r/nstonic/test_django_app/tags). Название тега соотвествует хешу коммитов в данном репозитории.
- Создайте под с Postgres с помощью helm: `helm install django-db oci://registry-1.docker.io/bitnamicharts/postgresql`
- Создайте [базу данных](https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e)
- Создайте в директории kubernetes configmap.yml cо следующим манифестом:
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: django-config
  namespace: edu-trusting-bartik
data:
  DATABASE_URL: postgres://USER:PASSWORD@HOST:PORT/NAME
  SECRET_KEY: 123456
  DEBUG: 'false'
  ALLOWED_HOSTS: star-burger.test
```
- Примените созданный configMap `kubectl apply -f .\kubernetes\configmap.yml`
- Примените все манифесты из папки kubernetes: `kubectl apply -f .\kubernetes\`
- [Откройте сайт](https://edu-trusting-bartik.sirius-k8s.dvmn.org/admin/)