from dataclasses import dataclass
from typing import Optional

from conf.env import get


@dataclass
class Stand:
    ui: Optional[str] = None
    db: Optional[str] = None


STAND_SELECTOR = {
    "stb": Stand(ui="type_url_ui", db="type_db_ip"),
}


def get_stand_data():
    # type: () -> Stand
    return STAND_SELECTOR[get('ENV', default='stb')]
