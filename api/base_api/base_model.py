from dataclasses import dataclass, asdict


@dataclass
class BaseModel:

    def asdict(self):
        return {key: value for key, value in asdict(self).items() if value is not None}
