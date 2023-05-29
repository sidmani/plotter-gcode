from svgelements import Group, Polyline, Path, Move, Line, Close
from .transform import apply_transform


def process_svg_polyline(e):
    result = []
    if len(e.points) > 1:
        last_p = e.points[0]
        for p in e.points[1:]:
            result.append(("line", (last_p, p)))
            last_p = p
    return result


def process_svg_path(path):
    first_p = None
    last_p = None
    result = []
    for segment in path:
        if isinstance(segment, Move):
            if last_p is None:
                last_p = segment.end
        elif isinstance(segment, Line):
            if first_p is None:
                first_p = segment.start
            if last_p is None:
                last_p = segment.end
            if segment.start == segment.end:
                continue
            result.append(("line", (segment.start, segment.end)))

        elif isinstance(segment, Close):
            if first_p is None or last_p is None:
                raise Exception(f"Cannot close path {path.__dict__}")
            result.append(("line", (first_p, last_p)))
        else:
            raise Exception(f"Unhandled path segment of type {type(segment)}")

    return result


def svg_to_paths(svg):
    paths = []
    for e in svg.elements():
        if isinstance(e, Group):
            # skip groups, because we recurse into them anyway
            continue
        elif isinstance(e, Polyline):
            paths += process_svg_polyline(e)
        elif isinstance(e, Path):
            paths += process_svg_path(e)
        else:
            raise Exception(f"Unhandled element type {type(e)}")

    return paths


def transform_paths(paths, scale, offset):
    result = []
    for kind, data in paths:
        if kind == "line":
            result.append(
                ("line", tuple(map(lambda p: apply_transform(p, scale, offset), data)))
            )
        else:
            raise Exception("unknown path type")
    return result


# def filter_dups(paths):
#     hmap = set()
#     result = []
#     for p in paths:
#         if p not in hmap:
#             result.append(p)
#             hmap.add(p)
#     return result
