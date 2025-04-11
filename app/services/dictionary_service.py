from app.repositories.dictionary_repository import IDictionaryRepository
from app.models.database import DictionaryItem
from app.schemas.dictionary import DictionaryItemResponse

class DictionaryService:
    def __init__(self, repository: IDictionaryRepository):
        self.repository = repository

    def add_dictionary_item(self, user_id: str, item: str) -> DictionaryItemResponse:
        existing_item = self.repository.find_matching_item(user_id, item)
        if existing_item:
            return DictionaryItemResponse.parse_obj({
                "id": existing_item.id,
                "item": existing_item.item,
                "user_id": existing_item.user_id
            })
        
        new_item = self.repository.add_dictionary_item(user_id, item)
        return DictionaryItemResponse.parse_obj({
            "id": new_item.id,
            "item": new_item.item,
            "user_id": new_item.user_id
        })

    def get_all_dictionary_items(self, user_id: str) -> list[DictionaryItemResponse]:
        items = self.repository.get_all_dictionary_items(user_id)
        return [DictionaryItemResponse.parse_obj({
            "id": item.id,
            "item": item.item
        }) for item in items] 