from dependency_injector import containers, providers

from turtled_backend import router
from turtled_backend.common import util
from turtled_backend.repository.example import ExampleRepository
from turtled_backend.service.example import ExampleService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[util, router])

    """ Repository """
    example_repository = providers.Singleton(ExampleRepository)

    """ Service """
    example_service = providers.Singleton(ExampleService,
                                          example_repository=example_repository)
