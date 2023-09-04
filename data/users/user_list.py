from dataclasses import dataclass


@dataclass
class User:
    name: str = None
    login: str = None
    password: str = None
    arm: str = ''
    name_with_dots: str = ''
    person_number: int = ''
    id: int = ''


USER_LIST = [
    User(name='Специалистов С С', login='sys112sp', password='Qwerty1234@@', arm='168',
         name_with_dots='Специалистов С.С.', person_number=0, id=100053),
    User(name='Системный П Т', login='sys112', password='Qwerty1234@@', arm='24',
         name_with_dots='Системный П. Т.', person_number=1002, id=100075),
    User(name='тест ФСБ', login='sys112testFSB', password='Qwerty1234@@', arm='175', name_with_dots='тест ФСБ'),
    User(name='Оператор ЭОС', login='sys112arm', password='Qwerty1234@@', arm='14'),
    User(name='Наблюдатель ЭОС', login='sys112FSBview', password='Qwerty1234@@', arm='527'),
    User(name='Контролер ЭОС', login='sys112kontroler', password='Qwerty1234@@', arm='528'),
    User(name='Оператор контроля', login='sys112edds', password='Qwerty1234@@', arm='297'),
    User(name='Оператор телефонии', login='sys112phone', password='Qwerty1234@@', arm='529'),
    User(name='Начальников Н Н', login='NachalnikovN', password='Qwerty1234@@', arm='100'),
    User(name='Машинистов М Е', login='sys112spec', password='Qwerty1234@@', arm='100', person_number=4456, id=100049),
]


class Users:
    SPECIALIST_1 = USER_LIST[0]
    MAIN_SPECIALIST = USER_LIST[1]
    FSB_SPECIALIST = USER_LIST[2]
    EOS_OPERATOR = USER_LIST[3]
    EOS_OBSERVER = USER_LIST[4]
    EOS_CONTROLLER = USER_LIST[5]
    CONTROL_OPERATOR = USER_LIST[6]
    TELEPHONY_OPERATOR = USER_LIST[7]
    SHIFT_SUPERVISOR = USER_LIST[8]
    MASHINISTOV_SPECIALIST = USER_LIST[9]


if __name__ == '__main__':
    pass
