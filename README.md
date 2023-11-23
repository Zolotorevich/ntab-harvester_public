# Сборщик новостей с сайтов
Собирает заголовки с новостных сайтов и сохраняет в базе данных.

Внутри: beautifulsoup4, mysql, requests

Зачем: www.zolotorevich.com/works/ntab/newsletter/

## app.py
Запускает обходчики сайтов по команде из CLI

## crawlers/factory.py
Создаёт обходчики сайтов

## crawlers/abstract.py
Абстрактный класс обходчика и датакласс собранной информации

## crawlers/%website%.py
Обходчики
