from dependency_injector import containers, providers

from turtled_backend import router
from turtled_backend.common import util
from turtled_backend.repository.example import ExampleRepository
from turtled_backend.repository.user import UserRepository
from turtled_backend.service.example import ExampleService
from turtled_backend.service.user import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[util, router])

    """ Repository """
    example_repository = providers.Singleton(ExampleRepository)
    user_repository = providers.Singleton(UserRepository)

    """ Service """
    example_service = providers.Singleton(ExampleService,
                                          example_repository=example_repository)

    user_service = providers.Singleton(UserService,
                                          user_repository=user_repository)