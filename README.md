# PROJECT_NAME

## Развертывание

1. `sudo apt update && sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl`
2. `sudo -H pip3 install virtualenv`
3. `mkdir ~/project`
4. `cd ~/project`
5. `virtualenv myprojectenv`
6. `source myprojectenv/bin/activate`
7. `pip3 install -r requirements.txt`
8. `Создание файла сокета gunicorn`
9. `Создание служебного файла systemd`
10. `sudo systemctl start gunicorn.socket`
11. `sudo systemctl enable gunicorn.socket`
12. `sudo systemctl status gunicorn.socket`
13. `Редактирование конфигурации nginx для обработки gunicorn`

## Тесты

`python3 manage.py test`

## Сервер
`http://178.154.215.99:8080/`
