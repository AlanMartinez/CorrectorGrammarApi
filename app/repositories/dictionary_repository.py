from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.database import User, DictionaryItem

class IDictionaryRepository(ABC):
    @abstractmethod
    def add_dictionary_item(self, user_id: str, item: str) -> DictionaryItem:
        pass

    @abstractmethod
    def get_all_dictionary_items(self, user_id: str) -> List[DictionaryItem]:
        pass

    @abstractmethod
    def find_matching_item(self, user_id: str, item: str) -> Optional[DictionaryItem]:
        pass

class DictionaryRepository(IDictionaryRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_dictionary_item(self, user_id: str, item: str) -> DictionaryItem:
        # Check if user exists, if not create it
        user = self.db_session.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id)
            self.db_session.add(user)
            self.db_session.commit()

        # Create new dictionary item
        dictionary_item = DictionaryItem(item=item, user_id=user_id)
        self.db_session.add(dictionary_item)
        self.db_session.commit()
        return dictionary_item

    def get_all_dictionary_items(self, user_id: str) -> List[DictionaryItem]:
        return self.db_session.query(DictionaryItem).filter(DictionaryItem.user_id == user_id).all()

    def find_matching_item(self, user_id: str, item: str) -> Optional[DictionaryItem]:
        return self.db_session.query(DictionaryItem).filter(
            DictionaryItem.user_id == user_id,
            DictionaryItem.item.ilike(item)  # Case-insensitive comparison using SQL ILIKE
        ).first() 