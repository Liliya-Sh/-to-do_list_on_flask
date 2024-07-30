Техническое задание: Сервис для работы с Календарем.

## запуск приложения

```
.venv\Scripts\activate.bat

flask --app  server run --debug
```


## cURL тестирование

### добавление нового события
```
curl http://127.0.0.1:5000/api/v1/calendar/event/ -X POST -d "2020-12-05|title|text"
```

### получение всего списка событий
```
curl http://127.0.0.1:5000/api/v1/calendar/event/
```

### получение события по идентификатору / ID == 1
```
curl http://127.0.0.1:5000/api/v1/calendar/event/1/
```

### обновление текста события по идентификатору / ID == 1 /  новый текст == "new text"
```
http://127.0.0.1:5000/api/v1/calendar/event/1/ -X PUT -d "2020-10-05|title| new text
```

### добавление события с уже существующей датой  / date ==2020-12-10,  нове событие == "text1"/
```
http://127.0.0.1:5000/api/v1/calendar/event/ -X POST -d "2020-12-10|title|text1"
```

### удаление события по идентификатору / ID == 1
```
curl http://127.0.0.1:5000/api/v1/calendar/event/1/ -X DELETE
```


## пример исполнения команд с выводом

```
$ curl http://127.0.0.1:5000/api/v1/calendar/event/ -X POST -d "2020-12-05|title|text"
new id: 1

$ curl http://127.0.0.1:5000/api/v1/calendar/event/ -X POST -d "2|2020-12-10|title|text"
new id: 2

$ curl http://127.0.0.1:5000/api/v1/calendar/event/
1|2020-12-05|title|text
2|2020-12-10|title|text

$ curl http://127.0.0.1:5000/api/v1/calendar/event/1/
1|2020-12-05|title|text

$ curl http://127.0.0.1:5000/api/v1/calendar/event/2/ -X PUT -d "2020-12-10|title| new text"
updated

$ curl http://127.0.0.1:5000/api/v1/calendar/event/2/
2|2020-12-10|title| new text

$ curl http://127.0.0.1:5000/api/v1/calendar/event/ -X POST -d "2020-12-10|title|text1"
failed to CREATE with: An event already exists for date 2020-12-10

$ curl http://127.0.0.1:5000/api/v1/calendar/event/2/ -X PUT -d "20201210|title| new text"
failed to UPDATE with: time data '20201210' does not match format '%Y-%m-%d'

$ curl http://127.0.0.1:5000/api/v1/calendar/event/2/ -X PUT -d "2020-12-10|loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong title| new text"
failed to UPDATE with: title lenght > MAX: 30

$ curl http://127.0.0.1:5000/api/v1/calendar/event/2/ -X PUT -d "2020-12-10|title| looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong text"
failed to UPDATE with: text lenght > MAX: 200


$ curl curl http://127.0.0.1:5000/api/v1/calendar/event/1/ -X DELETE
deleted

$ curl http://127.0.0.1:5000/api/v1/calendar/event/2/ -X DELETE
deleted

$ curl http://127.0.0.1:5000/api/v1/calendar/event/
-- пусто --
```