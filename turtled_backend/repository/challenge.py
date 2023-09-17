from turtled_backend.common.util.repository import Repository
from turtled_backend.schema.challenge import Medal, UserChallenge


class MedalRepository(Repository[Medal]):
    ...


class UserChallengeRepository(Repository[UserChallenge]):
    ...
