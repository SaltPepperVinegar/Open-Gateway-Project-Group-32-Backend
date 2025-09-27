from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class GeoJSONPolygon(BaseModel):
    """
    Polygons in this application has one more restriction:
    Every polygon can only have ONE ring.
    Those with multiple rings are not accepted (like doughnut shape).
    """

    gid: str
    type: Literal["Polygon"] = Field("Polygon", description="type must be 'Polygon'")
    coordinates: List[List[List[float]]] = Field(
        ..., description="Array of linear rings, each a list of [lng, lat] points"
    )

    @field_validator("coordinates")
    def validate_coordinates(cls, coords):
        if not coords or not isinstance(coords, list):
            raise ValueError("Polygon must have one linear ring")
        
        if len(coords) > 1:
            raise ValueError("Polygon must have exactly one ring.")
        
        ring = coords[0]

        if len(ring) < 4:
                raise ValueError("Each linear ring must have at least 4 positions")
        
        if ring[0] != ring[-1]:
            raise ValueError("Linear ring must be closed (first and last positions must match)")
        
        for point in ring:
            if len(point) != 2:
                raise ValueError("Each position must be a [lng, lat] coordinate pair")
            
        return coords


class GeoJSONPoint(BaseModel):
    gid: Optional[str] = None
    type: Literal["Point"] = Field("Point", description="type must be 'Point'")
    coordinates: List[float]
