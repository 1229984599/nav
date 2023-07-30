from pydantic import BaseModel


class SetLinkSchema(BaseModel):
    links: list[int]
    menu_id: int
