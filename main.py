from typing import Any, List
from fastapi import FastAPI, Depends, Body, Security
from fastapi.params import Query
from fastapi.security import (
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer,
)
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from containers import Container
from auth import AuthService
from services import BookService
from model import FileProcessResponse, FileProcessErrorResponse, PaginatedBooksResponse
from serializers import serializer, serialize_book

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token", scopes={"read": "Read access", "write": "Write access"}
)


app = FastAPI()

app.state.saved_books = []


@app.post("/token", include_in_schema=False)
@inject
def login_route(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    return auth_service.login(form_data)


@app.get(
    "/interface/001",
    response_model=PaginatedBooksResponse,
    operation_id="list_books_interface_001_get",
)
@inject
def list_items_with_pagination(
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of records to skip",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of records to return",
    ),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    book_service: BookService = Depends(Provide[Container.book_service]),
    token: str = Security(oauth2_scheme, scopes=["read"]),
):
    print("====")
    print(app.state.saved_books)
    current_user = auth_service.get_current_user(token)
    if app.state.saved_books:
        items = book_service.get_books_with_pagination(
            skip, limit, app.state.saved_books
        )
    else:
        items = book_service.get_default_books_with_pagination(skip, limit)

    data = {
        "total": len(items),
        "skip": skip,
        "limit": limit,
        "items": items,
    }
    return PaginatedBooksResponse.model_validate(data)


example_payload = """1|TXN-20250921-001|BUY|Alice Ltd|1200.50|2025-09-26 18:07:02
2|The Silent Forest|Alice Johnson|2023-04-15
2|Echoes of Tomorrow|Michael Chen|2021-09-30
2|Whispers in the Dark|Sophia Martinez|2022-01-12
2|The Last Horizon|David Brown|2020-06-05
2|Shadows of Time|Emma Wilson|2019-11-21
2|Beneath the Stars|James Lee|2024-02-08
2|Forgotten Legends|Lily Zhang|2018-08-14
2|The Crimson Dawn|William Scott|2023-12-03
2|Paths Untaken|Olivia Davis|2022-07-19
2|Dreams of Infinity|Ethan Kim|2021-03-27
99|10"""


@app.post(
    "/interface/001",
    responses={
        200: {"model": FileProcessResponse},
        400: {"description": "Validation failed", "model": FileProcessErrorResponse},
    },
)
@inject
def create_record(
    book: str = Body(media_type="text/plain", example=example_payload),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    token: str = Security(oauth2_scheme, scopes=["write"]),
):
    current_user = auth_service.get_current_user(token)
    payload = serializer(book)
    # print(payload)
    if payload.get("status") == "Success":
        if serialize_book(book):
            print("Bar")
            app.state.saved_books = serialize_book(book)
            print(app.state.saved_books)
        return JSONResponse(
            status_code=200,
            content=FileProcessResponse.model_validate(payload).model_dump(),
        )
    else:
        payload["reason"] = "invalid data"
        return JSONResponse(
            status_code=400,
            content=FileProcessErrorResponse.model_validate(payload).model_dump(),
        )


container = Container()
container.wire(modules=[__name__])
app.container = container
