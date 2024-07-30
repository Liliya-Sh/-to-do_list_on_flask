from datetime import datetime

from flask import Flask
from flask import request
from storage import StorageException

app = Flask(__name__)

import model
import logic

_event_logic = logic.EventLogic()


class ApiException(Exception):
    pass


def _from_raw(raw_event: str) -> model.Event:
    """Разделяем полученную строку по '|', id вляется не обязательным для ввода """
    parts = raw_event.split('|')
    if len(parts) == 3:
        event = model.Event()
        event.id = None
        event.date = datetime.strptime(parts[0], "%Y-%m-%d").date()
        event.title = parts[1]
        event.text = parts[2]
        return event
    elif len(parts) == 4:
        event = model.Event()
        event.id = parts[0]
        event.date = datetime.strptime(parts[1], "%Y-%m-%d").date()
        event.title = parts[2]
        event.text = parts[3]
        return event
    else:
        raise ApiException(f"invalid RAW event data {raw_event}")


def _to_raw(event: model.Event) -> str:
    if event.id is None:
        return f"{event.date}|{event.title}|{event.text}"
    else:
        return f"{event.id}|{event.date}|{event.title}|{event.text}"


API_ROOT = "/api/v1/calendar"
EVENT_API_ROOT = API_ROOT + "/event"


@app.route(EVENT_API_ROOT + "/", methods=["POST"])
def create():
    """Добавляем новое событие"""
    try:
        data = request.get_data().decode('utf-8')
        event = _from_raw(data)

        # Проверяем, есть ли уже событие в этот день
        for existing_event in _event_logic.list():
            if existing_event.date == event.date:
                raise StorageException(f"An event already exists for date {event.date}")

        _id = _event_logic.create(event)
        return f"new id: {_id}", 201
    except Exception as ex:
        return f"failed to CREATE with: {ex}", 404


@app.route(EVENT_API_ROOT + "/", methods=["GET"])
def list_event():
    """Просмотреть список всех событий"""
    try:
        events = _event_logic.list()
        raw_events = ""
        for event in events:
            raw_events += _to_raw(event) + '\n'
        return raw_events, 200
    except Exception as ex:
        return f"failed to LIST with: {ex}", 404


@app.route(EVENT_API_ROOT + "/<_id>/", methods=["GET"])
def read(_id: str):
    """Просмотр события"""
    try:
        event = _event_logic.read(_id)
        raw_event = _to_raw(event)
        return raw_event, 200
    except Exception as ex:
        return f"failed to READ with: {ex}", 404


@app.route(EVENT_API_ROOT + "/<_id>/", methods=["PUT"])
def update(_id: str):
    """Изменяем событие"""
    try:
        data = request.get_data().decode('utf-8')
        event = _from_raw(data)
        _event_logic.update(_id, event)
        return "updated", 200
    except Exception as ex:
        return f"failed to UPDATE with: {ex}", 404


@app.route(EVENT_API_ROOT + "/<_id>/", methods=["DELETE"])
def delete(_id: str):
    """Удаляем событие"""
    try:
        _event_logic.delete(_id)
        return "deleted", 200
    except Exception as ex:
        return f"failed to DELETE with: {ex}", 404
