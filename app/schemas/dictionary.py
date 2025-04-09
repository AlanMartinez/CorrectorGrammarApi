from pydantic import BaseModel
from typing import List

class DictionaryItemCreate(BaseModel):
    user_id: str
    dictionary_item: str

class DictionaryItemResponse(BaseModel):
    id: int
    item: str
    user_id: str

    class Config:
        from_attributes = True

class DictionaryItemsResponse(BaseModel):
    items: List[DictionaryItemResponse] 