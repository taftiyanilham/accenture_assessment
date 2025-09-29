from fastapi import FastAPI, Depends, Body, Security, Response
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
from model import (
    FileProcessResponse,
    FileProcessErrorResponse,
    PaginatedBooksResponse,
)

from serializers import parse_book_line
from sqlalchemy.orm import Session
from database import engine, Base, get_db

Base.metadata.create_all(bind=engine)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token", scopes={"read": "Read access", "write": "Write access"}
)


app = FastAPI()

app.state.saved_books = []


@app.post("/token", include_in_schema=False)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    response: Response = None,
    auth_service: AuthService = Depends(),
):
    return auth_service.login(form_data, db, response)


@app.get("/interface/001", response_model=PaginatedBooksResponse)
@inject
def list_items_with_pagination(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    token: str = Security(oauth2_scheme, scopes=["read"]),
    db: Session = Depends(get_db),
):
    current_user: str = Depends(AuthService().get_current_user)
    book_service = BookService(db)
    items = book_service.get_books_with_pagination(skip, limit)

    return {
        "total": len(items),
        "skip": skip,
        "limit": limit,
        "items": items,
    }


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
        400: {"model": FileProcessErrorResponse},
    },
)
@inject
def create_record(
    book: str = Body(media_type="text/plain", example=example_payload),
    auth_service: AuthService = Depends(Provide[Container.auth_service]),
    token: str = Security(oauth2_scheme, scopes=["write"]),
    db: Session = Depends(get_db),
):
    current_user: str = (Depends(AuthService().get_current_user),)
    book_service = BookService(db)

    lines = book.strip().splitlines()
    processed_count = 0
    issues = []

    for idx, line in enumerate(lines, start=1):
        result = parse_book_line(line, idx)

        if isinstance(result, dict):
            issues.append(result)
            continue

        payload = result
        existing = book_service.get_book_by_title(payload.book_title)
        if existing:
            issues.append(
                {
                    "line_number": idx,
                    "raw_data": line,
                    "reason": f"Duplicate book_title '{payload.book_title}'",
                }
            )
            continue

        book_service.create_book(payload)
        processed_count += 1

    if issues:
        return JSONResponse(
            status_code=400,
            content=FileProcessErrorResponse(
                status="Failed",
                reason="Some rows failed validation",
                processed_body_count=processed_count,
                body_with_issues=len(issues),
                issues=issues,
            ).model_dump(),
        )

    return JSONResponse(
        status_code=200,
        content=FileProcessResponse(
            status="Success",
            processed_body_count=processed_count,
            body_with_issues=0,
            issues=[],
        ).model_dump(),
    )


container = Container()
container.wire(modules=[__name__])
app.container = container
