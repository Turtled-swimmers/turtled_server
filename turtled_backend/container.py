from dependency_injector import containers, providers

from turtled_backend import router
from turtled_backend.common import util
from turtled_backend.repository.challenge import (
    CalenderRecordListRepository,
    ChallengeRecordRepository,
    MedalRepository,
    UserChallengeRepository,
)
from turtled_backend.repository.example import ExampleRepository
from turtled_backend.repository.user import UserDeviceRepository, UserRepository
from turtled_backend.service.challenge import ChallengeService
from turtled_backend.service.example import ExampleService
from turtled_backend.service.timer import TimerService
from turtled_backend.service.user import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[util, router])

    """ Repository """
    example_repository = providers.Singleton(ExampleRepository)
    user_repository = providers.Singleton(UserRepository)
    user_device_repository = providers.Singleton(UserDeviceRepository)
    medal_repository = providers.Singleton(MedalRepository)
    user_challenge_repository = providers.Singleton(UserChallengeRepository)
    challenge_record_repository = providers.Singleton(ChallengeRecordRepository)
    calendar_record_list_repository = providers.Singleton(CalenderRecordListRepository)

    """ Service """
    example_service = providers.Singleton(ExampleService, example_repository=example_repository)

    user_service = providers.Singleton(
        UserService,
        user_repository=user_repository,
        user_device_repository=user_device_repository,
        medal_repository=medal_repository,
    )

    challenge_service = providers.Singleton(
        ChallengeService,
        medal_repository=medal_repository,
        user_challenge_repository=user_challenge_repository,
        user_device_repository=user_device_repository,
        calendar_record_list_repository=calendar_record_list_repository,
        challenge_record_repository=challenge_record_repository,
    )

    timer_service = providers.Singleton(
        TimerService,
        user_device_repository=user_device_repository,
        challenge_record_repository=challenge_record_repository,
        calendar_record_list_repository=calendar_record_list_repository,
    )
