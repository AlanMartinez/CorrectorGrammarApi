from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.models.database import engine
from app.repositories.dictionary_repository import DictionaryRepository
from app.services.dictionary_service import DictionaryService
from app.schemas.dictionary import DictionaryItemCreate, DictionaryItemResponse, DictionaryItemsResponse

app = FastAPI(title="Dictionary API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

def get_dictionary_service(db: Session = Depends(get_db)) -> DictionaryService:
    repository = DictionaryRepository(db)
    return DictionaryService(repository)

@app.post("/dictionary", response_model=DictionaryItemResponse)
def add_dictionary_item(
    item: DictionaryItemCreate,
    service: DictionaryService = Depends(get_dictionary_service)
):
    dictionary_item = service.add_dictionary_item(item.user_id, item.dictionary_item)
    return dictionary_item

@app.get("/dictionary/{user_id}", response_model=DictionaryItemsResponse)
def get_all_dictionary_items(
    user_id: str,
    service: DictionaryService = Depends(get_dictionary_service)
):
    items = service.get_all_dictionary_items(user_id)
    return DictionaryItemsResponse(items=items) 