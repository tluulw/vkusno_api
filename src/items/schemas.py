from typing import Union

from pydantic import BaseModel


class ItemAdd(BaseModel):
    title: str
    image: str
    description: Union[str, None]
    price: int
    size: str
