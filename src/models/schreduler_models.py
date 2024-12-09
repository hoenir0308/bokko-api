from pydantic import BaseModel

class Schreduler(BaseModel):
    send_at: str
    enable: bool
    interval: str
    motivate: bool
