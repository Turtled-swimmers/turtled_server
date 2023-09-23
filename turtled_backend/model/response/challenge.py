from datetime import date

from pydantic import BaseModel

from turtled_backend.schema.challenge import Medal


class ChallengeResponse(BaseModel):
    medal_id: str
    image: str
    title: str
    subtitle: str
    content: str
    requirement: str
    isAchieved: bool

    @classmethod
    def from_entity(cls, entity: Medal, is_achieved: bool):
        return cls(
            medal_id=entity.id,
            image=entity.image,
            title=entity.title,
            subtitle=entity.subtitle,
            content=entity.content,
            requirement=entity.requirement,
            isAchieved=is_achieved,
        )


class CalendarEventResponse(BaseModel):
    calendar_date: date
    has_event: bool

    @staticmethod
    def of(calendar_date: date, has_event: bool):
        return CalendarEventResponse(
            calendar_date=calendar_date,
            has_event=has_event
        )
