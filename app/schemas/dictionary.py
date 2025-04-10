from pydantic import BaseModel

class DictionaryItemCreate(BaseModel):
    user_id: str
    dictionary_item: str

class DictionaryItemResponse(BaseModel):
    id: int
    item: str
    user_id: str

    model_config = {
        "from_attributes": True
    }

class DictionaryItemsResponse(BaseModel):
    items: list[DictionaryItemResponse]
    
    model_config = {
        "from_attributes": True
    } 