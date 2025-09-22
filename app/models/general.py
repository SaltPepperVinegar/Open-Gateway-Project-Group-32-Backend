from typing import List, Literal

from pydantic import BaseModel, Field, field_validator


class GeoJSONPolygon(BaseModel):
    type: Literal["Polygon"] = Field("Polygon", description="type must be 'Polygon'")
    coordinates: List[List[List[float]]] = Field(
        ..., 
        description="Array of linear rings, each a list of [lng, lat] points"
    )

    @field_validator("coordinates")
    def validate_coordinates(cls, coords):
        if not coords or not isinstance(coords, list):
            raise ValueError("Polygon must have at least one linear ring")
        
        for ring in coords:
            if len(ring) < 4:
                raise ValueError("Each linear ring must have at least 4 positions")
            if ring[0] != ring[-1]:
                raise ValueError("Linear ring must be closed (first and last positions must match)")
            for point in ring:
                if len(point) != 2:
                    raise ValueError("Each position must be a [lng, lat] coordinate pair")
        return coords