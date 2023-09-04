from dataclasses import dataclass
from typing import Optional


@dataclass
class GosService:
    title: Optional[str] = None
    id: Optional[int] = None
    phone: Optional[str] = None


class GosServices:
    SERVICE_101 = GosService(title='Служба 101', id=1, phone='101')
    SERVICE_FSB = GosService(title='ФСБ', id=3)
    AUTO_TEST_SERVICE = GosService(title='Авто Тестовая Служба', id=123456)
