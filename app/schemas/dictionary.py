from pydantic import BaseModel

class DictionaryItemCreate(BaseModel):
    user_id: str
    dictionary_item: str

class DictionaryItemResponse(BaseModel):
    id: int
    item: str

    class Config:
        orm_mode = True

class DictionaryItemsResponse(BaseModel):
    items: list[DictionaryItemResponse]

    class Config:
        orm_mode = True 