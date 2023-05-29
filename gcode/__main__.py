import argparse
from svgelements import SVG, Group, Polyline
from .gcode import PlotterGcode
from .path import svg_to_paths, transform_paths
from .transform import make_transform, correct_svg_bbox


def main(args):
    gcode = PlotterGcode(
        safe_height=args.safe_height,
        retract_height=args.retract_height,
        work_height=args.work_height,
    )
    rect = args.rect

    gcode.Z_safe_height()
    if not args.skip_home:
        gcode.auto_home()
    gcode.move({"X": rect[0], "Y": rect[1]})

    if args.trace_rect:
        gcode.move({"Y": rect[3]})
        gcode.move({"X": rect[2]})
        gcode.move({"Y": rect[1]})
        gcode.move({"X": rect[0]})

    if args.svg:
        with open(args.svg, "r") as svg_file:
            svg = SVG.parse(svg_file)
            paths = svg_to_paths(svg)
            bbox = correct_svg_bbox(svg.bbox())
            scale, offset = make_transform(bbox, args.rect)
            paths = transform_paths(paths, scale, offset)
            for p in paths:
                gcode.add_path(p)

    gcode.Z_safe_height()
    print(gcode.compile())


parser = argparse.ArgumentParser()
parser.add_argument("-r", "--rect", nargs=4, type=int, required=True)
parser.add_argument("--safe-height", type=float, required=True)
parser.add_argument("--work-height", type=float, required=True)
parser.add_argument("--retract-height", type=float, required=True)
parser.add_argument("--skip-home", action="store_true")
parser.add_argument("--svg")
parser.add_argument("--trace-rect", action="store_true")
args = parser.parse_args()

if __name__ == "__main__":
    main(args)
