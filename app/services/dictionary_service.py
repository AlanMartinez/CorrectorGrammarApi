from typing import List
from app.repositories.dictionary_repository import IDictionaryRepository
from app.models.database import DictionaryItem

class DictionaryService:
    def __init__(self, repository: IDictionaryRepository):
        self.repository = repository

    def add_dictionary_item(self, user_id: str, item: str) -> DictionaryItem:
        existing_item = self.repository.find_matching_item(user_id, item)
        if existing_item:
            return existing_item 
        
        return self.repository.add_dictionary_item(user_id, item)

    def get_all_dictionary_items(self, user_id: str) -> List[DictionaryItem]:
        return self.repository.get_all_dictionary_items(user_id) 