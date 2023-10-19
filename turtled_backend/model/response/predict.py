from pydantic import BaseModel

class PredictResponse(BaseModel):
    medal_id: str
    image: str


    @classmethod
    def of(cls, medal_id: str, image: str):
        return cls(medal_id=medal_id, image=image)
