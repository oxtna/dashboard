from typing import Literal, Annotated
import pydantic as pdt
from .tags import Tags


class FilterParams(pdt.BaseModel):
    country: Annotated[
        int | None,
        pdt.Field(
            default=None, ge=0, title="ID of the country that is related to this data"
        ),
    ]
    year: Annotated[
        int | None,
        pdt.Field(default=None, ge=1900, title="Year in which this data was recorded"),
    ]
    order_by: Literal["country", "year"] = "year"
    tags: list[Tags | str] = []


class CountriesFilterParams(pdt.BaseModel):
    order_by: Literal["id", "name"] = "id"
    tags: list[Tags | str] = [Tags.country]
