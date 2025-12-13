from pydantic import BaseModel, Field


class Stats(BaseModel):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int


class Character(BaseModel):
    id: int
    name: str
    race: str
    class_: str = Field(alias="class")  # 'class' is a reserved keyword
    alignment: str
    description: str
    stats: Stats

    model_config = {
        "populate_by_name": True  # Allows both 'class' and 'class_' to work
    }


class CharactersResponse(BaseModel):
    characters: list[Character]
