class PlotterGcode:
    def __init__(self, safe_height, retract_height, work_height):
        self.safe_height = safe_height
        self.retract_height = retract_height
        self.work_height = work_height
        self.commands = []
        self.last_p = None

    def command(self, command, params=None):
        cmd = f"{command}"
        if params is not None:
            cmd += " " + " ".join([f"{key}{value}" for key, value in params.items()])
        self.commands.append(cmd)

    def compile(self):
        return "\n".join(self.commands)

    def auto_home(self):
        self.command("G28")

    def move(self, axes, fast=False):
        self.command("G0" if fast else "G1", axes)

    def Z_safe_height(self):
        self.move({"Z": self.safe_height}, fast=True)

    def Z_retract_height(self):
        self.move({"Z": self.retract_height}, fast=True)

    def Z_work_height(self):
        self.move({"Z": self.work_height}, fast=True)

    def add_path(self, path):
        kind, data = path
        if kind == "line":
            ((x0, y0), (x1, y1)) = data
            # don't move if we're already there
            if self.last_p is None or self.last_p != (x0, y0):
                self.Z_retract_height()
                self.move({"X": x0, "Y": y0})
                self.Z_work_height()
            self.last_p = (x1, y1)
            self.move({"X": x1, "Y": y1})
        else:
            raise Exception("unknown path type")
