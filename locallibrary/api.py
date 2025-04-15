from ninja import NinjaAPI, Schema
from typing import List, Optional
from django.contrib.auth.decorators import login_required
from ninja.security import HttpBearer
from catalog.models import Author, Genre, Language, Book, BookInstance
from datetime import date
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        from django.contrib.auth.models import User
        try:
            return User.objects.get(auth_token=token)
        except User.DoesNotExist:
            return None

api = NinjaAPI()

# Author Schemas and Endpoints

class AuthorSchema(Schema):
    id: int
    first_name: str
    last_name: str
    date_of_birth: date | None
    date_of_death: date | None

class AuthorCreateSchema(Schema):
    first_name: str
    last_name: str
    date_of_birth: date | None
    date_of_death: date | None

# Create
@api.post("/authors/", response=AuthorSchema)
def create_author(request, data: AuthorCreateSchema):
    author = Author.objects.create(**data.dict())
    return author

# Read All
@api.get("/authors/", response=list[AuthorSchema])
def list_authors(request):
    return Author.objects.all()

# Read One
@api.get("/authors/{author_id}", response=AuthorSchema)
def get_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    return author

# Update
@api.put("/authors/{author_id}", response=AuthorSchema)
def update_author(request, author_id: int, data: AuthorCreateSchema):
    author = get_object_or_404(Author, id=author_id)
    for attr, value in data.dict().items():
        setattr(author, attr, value)
    author.save()
    return author

# Delete
@api.delete("/authors/{author_id}")
def delete_author(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return {"success": True}


# Genre Schemas and Endpoints

class GenreSchema(Schema):
    id: int
    name: str

class GenreCreateSchema(Schema):
    name: str

# Create
@api.post("/genres/", response=GenreSchema)
def create_genre(request, data: GenreCreateSchema):
    genre = Genre.objects.create(**data.dict())
    return genre

# Read All
@api.get("/genres/", response=list[GenreSchema])
def list_genres(request):
    return Genre.objects.all()

# Read One
@api.get("/genres/{genre_id}", response=GenreSchema)
def get_genre(request, genre_id: int):
    genre = get_object_or_404(Genre, id=genre_id)
    return genre

# Update
@api.put("/genres/{genre_id}", response=GenreSchema)
def update_genre(request, genre_id: int, data: GenreCreateSchema):
    genre = get_object_or_404(Genre, id=genre_id)
    genre.name = data.name
    genre.save()
    return genre

# Delete
@api.delete("/genres/{genre_id}")
def delete_genre(request, genre_id: int):
    genre = get_object_or_404(Genre, id=genre_id)
    genre.delete()
    return {"success": True}


# Language Schemas and Endpoints

class LanguageSchema(Schema):
    id: int
    name: str

class LanguageCreateSchema(Schema):
    name: str

# Create
@api.post("/languages/", response=LanguageSchema)
def create_language(request, data: LanguageCreateSchema):
    language = Language.objects.create(**data.dict())
    return language

# Read All
@api.get("/languages/", response=list[LanguageSchema])
def list_languages(request):
    return Language.objects.all()

# Read One
@api.get("/languages/{language_id}", response=LanguageSchema)
def get_language(request, language_id: int):
    language = get_object_or_404(Language, id=language_id)
    return language

# Update
@api.put("/languages/{language_id}", response=LanguageSchema)
def update_language(request, language_id: int, data: LanguageCreateSchema):
    language = get_object_or_404(Language, id=language_id)
    language.name = data.name
    language.save()
    return language

# Delete
@api.delete("/languages/{language_id}")
def delete_language(request, language_id: int):
    language = get_object_or_404(Language, id=language_id)
    language.delete()
    return {"success": True}

# Book Schemas and Endpoints

class BookSchema(Schema):
    id: int
    title: str
    summary: str
    isbn: str
    language_id: Optional[int]  
    author_id: Optional[int]   
    genre_ids: List[int]  

    @staticmethod
    def from_orm(book: Book) -> "BookSchema":
        return BookSchema(
            id=book.id,
            title=book.title,
            summary=book.summary,
            isbn=book.isbn,
            language_id=book.language.id if book.language else None,  
            author_id=book.author.id if book.author else None,        
            genre_ids=[genre.id for genre in book.genre.all()]    
        )

class BookCreateSchema(Schema):
    title: str
    summary: str
    isbn: str
    language_id: Optional[int]
    author_id: Optional[int]
    genre_ids: List[int]

class BookInstanceSchema(BaseModel):
    id: UUID 
    book_id: int
    imprint: str
    due_back: Optional[date]
    status: str

    class Config:
        orm_mode = True
        from_attributes = True
    

#Create Book
@api.post("/books/", response=BookSchema, auth=GlobalAuth())
def create_book(request, data: BookCreateSchema):
    author = Author.objects.get(id=data.author_id) if data.author_id else None
    language = Language.objects.get(id=data.language_id) if data.language_id else None
    book = Book.objects.create(
        title=data.title,
        summary=data.summary,
        isbn=data.isbn,
        author=author,
        language=language,
    )
    book.genre.set(Genre.objects.filter(id__in=data.genre_ids))  # Add genres to book

    response_data = BookSchema.from_orm(book)  # Serializes the book including genres
    response_data.genre_ids = [genre.id for genre in book.genre.all()]  # Add genre_ids explicitly
    return response_data


#Read All Books
@api.get("/books/", response=List[BookSchema])
def list_books(request):
    books = Book.objects.all()
    response_data = []
    for book in books:
        book_data = BookSchema.from_orm(book)  # Serializes the book including genres
        book_data.genre_ids = [genre.id for genre in book.genre.all()]  # Add genre_ids explicitly
        response_data.append(book_data)

    return response_data

#Read One Book
@api.get("/books/{book_id}", response=BookSchema)
def get_book(request, book_id: int):
    book = get_object_or_404(Book, id=book_id)
    
    response_data = BookSchema.from_orm(book)  # Serializes the book including genres
    response_data.genre_ids = [genre.id for genre in book.genre.all()]  # Add genre_ids explicitly
    return response_data


#Update Book
@api.put("/books/{book_id}", response=BookSchema, auth=GlobalAuth())
def update_book(request, book_id: int, data: BookCreateSchema):
    book = get_object_or_404(Book, id=book_id)
    book.title = data.title
    book.summary = data.summary
    book.isbn = data.isbn

    if data.language_id:
        book.language = get_object_or_404(Language, id=data.language_id)
    if data.author_id:
        book.author = get_object_or_404(Author, id=data.author_id)
    book.genre.set(Genre.objects.filter(id__in=data.genre_ids))
    book.save()
    response_data = BookSchema.from_orm(book)
    response_data.genre_ids = [genre.id for genre in book.genre.all()]
    return response_data

#Delete Book
@api.delete("/books/{book_id}", auth=GlobalAuth())
def delete_book(request, book_id: int):
    book = Book.objects.get(id=book_id)
    book.delete()
    return {"success": True}

#Create BookInstance
@api.post("/bookinstances/", response=BookInstanceSchema, auth=GlobalAuth())
def create_bookinstance(request, data: BookInstanceSchema):
    book = Book.objects.get(id=data.book_id)
    book_instance = BookInstance.objects.create(
        book=book,
        imprint=data.imprint,
        due_back=data.due_back,
        status=data.status,
    )
    return BookInstanceSchema.from_orm(book_instance)

#Read All BookInstances
@api.get("/bookinstances/", response=List[BookInstanceSchema])
def list_bookinstances(request):
    book_instances = BookInstance.objects.all()
    response_data = []
    for book_instance in book_instances:
        book_instance_data = BookInstanceSchema.from_orm(book_instance)
        response_data.append(book_instance_data)

    return response_data


#Read One BookInstance
@api.get("/bookinstances/{bookinstance_id}", response=BookInstanceSchema)
def get_bookinstance(request, bookinstance_id: str):
    return BookInstance.objects.get(id=bookinstance_id)

#Update BookInstance
@api.put("/bookinstances/{bookinstance_id}", response=BookInstanceSchema, auth=GlobalAuth())
def update_bookinstance(request, bookinstance_id: str, data: BookInstanceSchema):
    book_instance = BookInstance.objects.get(id=bookinstance_id)
    book_instance.imprint = data.imprint
    book_instance.due_back = data.due_back
    book_instance.status = data.status
    book_instance.save()
    return book_instance

#Delete BookInstance
@api.delete("/bookinstances/{bookinstance_id}", auth=GlobalAuth())
def delete_bookinstance(request, bookinstance_id: str):
    book_instance = BookInstance.objects.get(id=bookinstance_id)
    book_instance.delete()
    return {"success": True}
