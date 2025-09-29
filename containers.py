from dependency_injector import containers, providers
from auth import AuthService
from services import BookService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["__main__"])

    # Service provider
    auth_service = providers.Factory(AuthService)
    book_service = providers.Factory(BookService)
