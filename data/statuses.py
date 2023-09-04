from dataclasses import dataclass


@dataclass
class Status:
    id: int = None
    title: str = None


class SmsStatuses:
    READED = 'Прочитана'


class IncidentCardStatuses:
    REGISTERED = Status(id=1, title='Зарегистрирована')


class GosServicesStatuses:
    ADDED = 'Добавлена'
    RECEIVED = 'Получена службой'
    ACCEPTED = 'Принята'
    NOT_ACCEPTED = 'Не принята'
    START_RESPONSE = 'Начало реагирования'
    CANCEL_PERFORM_WORKS = 'Отказ от выполнения работ'
    WORKS_FINISHED = 'Работы завершены'
    ARRIVED = 'Прибытие'
    EXECUTION_WORKS = 'Проведение работ'
