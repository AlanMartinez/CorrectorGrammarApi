from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.database import User
from app.repositories.dictionary_repository import DictionaryRepository
from app.services.dictionary_service import DictionaryService
from app.services.auth_service import (
    get_current_user,
    create_access_token,
    get_password_hash,
    verify_password,
    get_user_by_email,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.schemas.dictionary import DictionaryItemCreate, DictionaryItemResponse, DictionaryItemsResponse
from app.schemas.auth import UserCreate, Token, TokenData
from app.database import get_db

app = FastAPI(title="Dictionary API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def get_dictionary_service(db: Session = Depends(get_db)) -> DictionaryService:
    repository = DictionaryRepository(db)
    return DictionaryService(repository)

@app.post("/register", response_model=Token)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.email, "user_id": db_user.id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user_id": db_user.id}

@app.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}

@app.get("/validate-token", response_model=TokenData)
async def validate_token(current_user: User = Depends(get_current_user)):
    """
    Validate the JWT token and return the user's information.
    This endpoint can be used by other services to verify if a token is valid.
    """
    return TokenData(email=current_user.email, user_id=current_user.id)

@app.post("/dictionary", response_model=DictionaryItemResponse)
def add_dictionary_item(
    item: DictionaryItemCreate,
    current_user: User = Depends(get_current_user),
    service: DictionaryService = Depends(get_dictionary_service)
):
    dictionary_item = service.add_dictionary_item(current_user.id, item.dictionary_item)
    return dictionary_item

@app.get("/dictionary/{user_id}", response_model=DictionaryItemsResponse)
def get_all_dictionary_items(
    user_id: str,
    current_user: User = Depends(get_current_user),
    service: DictionaryService = Depends(get_dictionary_service)
):
    # Ensure users can only access their own dictionary items
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access other users' dictionary items"
        )
    items = service.get_all_dictionary_items(user_id)
    return DictionaryItemsResponse(items=items) 