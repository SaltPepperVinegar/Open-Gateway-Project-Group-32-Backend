from math import cos, radians
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon


def _point_in_ring(lng: float, lat: float, ring: List[List[float]]) -> bool:
    """Ray-casting with on-edge short-circuit."""
    inside = False
    n = len(ring)
    for i in range(n - 1):  # ring is closed (last == first)
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]

        # On-edge checks (horizontal and general collinearity within segment bounds)
        if ((y1 == y2 == lat) and min(x1, x2) <= lng <= max(x1, x2)) or (
            (min(y1, y2) <= lat <= max(y1, y2))
            and (x2 - x1) * (lat - y1) == (y2 - y1) * (lng - x1)
            and min(x1, x2) <= lng <= max(x1, x2)
            and min(y1, y2) <= lat <= max(y1, y2)
        ):
            return True

        # Standard raycast toggle (westward ray)
        intersects = ((y1 > lat) != (y2 > lat)) and (
            lng < (x2 - x1) * (lat - y1) / (y2 - y1 + 1e-16) + x1
        )
        if intersects:
            inside = not inside
    return inside


def _point_in_polygon(lng: float, lat: float, rings: List[List[List[float]]]) -> bool:
    """GeoJSON Polygon: [exterior, hole1, hole2, ...]."""
    if not rings:
        return False
    if not _point_in_ring(lng, lat, rings[0]):
        return False
    for hole in rings[1:]:
        if _point_in_ring(lng, lat, hole):
            return False
    return True


def _bbox(ring: List[List[float]]) -> Tuple[float, float, float, float]:
    xs = [p[0] for p in ring]
    ys = [p[1] for p in ring]
    return min(xs), min(ys), max(xs), max(ys)


# ----------------- tiling -----------------


def tile_strategy_square_centre(
    polygon_rings: List[List[List[float]]],
    spacing_m: float = 200,
    max_tiles: Optional[int] = None,
) -> List[List[List[float]]]:
    """
    Return a list of tile polygons (each a closed ring of [lng, lat] points)
    that lie inside the given GeoJSON Polygon (holes excluded).
    """
    if not polygon_rings or len(polygon_rings[0]) < 4:
        return []

    exterior = polygon_rings[0]
    minx, miny, maxx, maxy = _bbox(exterior)

    # meters → degrees
    dlat = spacing_m / 110_574.0

    tiles: List[List[List[float]]] = []
    lat = miny
    while lat <= maxy + 1e-12:
        # longitude degrees depend on latitude
        clat = max(min(lat, 89.9999), -89.9999)
        dlon = spacing_m / (111_320.0 * max(cos(radians(clat)), 1e-8))

        lng = minx
        while lng <= maxx + 1e-12:
            cx = lng + dlon / 2.0
            cy = lat + dlat / 2.0

            if _point_in_polygon(cx, cy, polygon_rings):
                x1, y1 = lng, lat
                x2, y2 = lng + dlon, lat
                x3, y3 = lng + dlon, lat + dlat
                x4, y4 = lng, lat + dlat
                boundary = [
                    [round(x1, 7), round(y1, 7)],
                    [round(x2, 7), round(y2, 7)],
                    [round(x3, 7), round(y3, 7)],
                    [round(x4, 7), round(y4, 7)],
                    [round(x1, 7), round(y1, 7)],  # close the ring
                ]
                tiles.append(boundary)

                if max_tiles is not None and len(tiles) >= max_tiles:
                    return tiles
            lng += dlon
        lat += dlat

    return tiles


def visualize_tiles(
    polygon_rings: List[List[List[float]]],
    tiles: List[List[List[float]]],
    show_centers: bool = False,
    save_path: Optional[str] = None,
    title: Optional[str] = None,
) -> None:
    """
    Plot the polygon outline and its tiles. Optionally mark tile centers and save to file.
    """
    fig, ax = plt.subplots(figsize=(7, 7))

    # polygon outline
    outline = MplPolygon(polygon_rings[0], closed=True, fill=False, linewidth=2)
    ax.add_patch(outline)

    # holes (if any)
    for hole in polygon_rings[1:]:
        ax.add_patch(
            MplPolygon(hole, closed=True, fill=False, linewidth=1.5, linestyle="--")
        )

    # tiles
    for b in tiles:
        ax.add_patch(MplPolygon(b, closed=True, fill=False, linewidth=0.8))
        if show_centers:
            # center = average of corners 0..3 (ignore closing point 4)
            xs = [p[0] for p in b[:4]]
            ys = [p[1] for p in b[:4]]
            cx = sum(xs) / 4.0
            cy = sum(ys) / 4.0
            ax.plot(cx, cy, marker=".", markersize=3)

    # frame
    xs = [p[0] for p in polygon_rings[0]]
    ys = [p[1] for p in polygon_rings[0]]
    ax.set_xlim(min(xs) - 0.001, max(xs) + 0.001)
    ax.set_ylim(min(ys) - 0.001, max(ys) + 0.001)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(title or "Polygon tiles")

    if save_path:
        plt.savefig(save_path, dpi=160, bbox_inches="tight")
    plt.show()


# ----------------- example usage -----------------
if __name__ == "__main__":
    polygon = [
        [
            [144.95, -37.82],
            [144.98, -37.82],
            [144.96, -37.78],
            [144.95, -37.80],
            [144.94, -37.79],
            [144.92, -37.79],
            [144.95, -37.82],
        ]
    ]
    spacing = 100

    tiles = tile_strategy_square_centre(polygon, spacing_m=spacing)
    print(f"Generated {len(tiles)} tiles.")
    # Visualize (set save_path="tiles.png" to export)
    visualize_tiles(
        polygon_rings=polygon,
        tiles=tiles,
        show_centers=True,
        save_path=None,
        title=f"Tiled polygon (spacing ≈ {int(spacing)} m)",
    )
