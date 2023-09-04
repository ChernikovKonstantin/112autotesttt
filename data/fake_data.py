from faker import Faker


def faker():
    return Faker('ru_RU')


class TestNames:
    WORK_SHIFT_GROUP = 'Группа_автотест'
