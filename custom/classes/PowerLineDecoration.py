from libqtile.widget import base

class PowerLineDecoration(base._Widget):
    """
    Un widget que dibuja una transición tipo powerline.
    Compatible con la funcionalidad de path de qtile-extras.
    """

    defaults = [
        ("foreground", "#000000", "Triangle color"),
        ("background", "#ffffff", "background color"),
        ("size", 10, "Transition height"),
        (
            "path",
            "arrow_right",
            "Transaction type: 'arrow_right', 'arrow_left', 'rounded', 'zigzag'",
        ),
    ]

    def __init__(self, **config):
        base._Widget.__init__(self, config.get("size", 10))
        self.add_defaults(PowerLineDecoration.defaults)
        for key, value in config.items():
            setattr(self, key, value)

    def _configure(self, qtile, bar):
        base._Widget._configure(self, qtile, bar)

    def draw(self):
        self.drawer.clear(self.background)

        x = 0
        y = 0
        w = self.width
        h = self.bar.height

        if self.path == "arrow_right":
            self._draw_arrow_right(x, y, w, h)
        elif self.path == "arrow_left":
            self._draw_arrow_left(x, y, w, h)
        elif self.path == "rounded":
            self._draw_rounded(x, y, w, h)
        elif self.path == "zigzag":
            self._draw_zigzag(x, y, w, h)
        else:
            self._draw_arrow_right(x, y, w, h)

        self.drawer.draw(offsetx=self.offset, width=self.width)

    def _draw_arrow_right(self, x, y, w, h):
        """Dibuja una transición tipo flecha apuntando hacia la derecha"""
        self.drawer.ctx.move_to(x, y)
        self.drawer.ctx.line_to(x + w, y + h / 2)
        self.drawer.ctx.line_to(x, y + h)
        self.drawer.ctx.close_path()
        self.drawer.set_source_rgb(self.foreground)
        self.drawer.ctx.fill()

    def _draw_arrow_left(self, x, y, w, h):
        """Dibuja una transición tipo flecha apuntando hacia la izquierda"""
        self.drawer.ctx.move_to(x + w, y)
        self.drawer.ctx.line_to(x, y + h / 2)
        self.drawer.ctx.line_to(x + w, y + h)
        self.drawer.ctx.close_path()
        self.drawer.set_source_rgb(self.foreground)
        self.drawer.ctx.fill()

    def _draw_rounded(self, x, y, w, h):
        """Dibuja una transición tipo redondeada"""

        radius = min(w, h) / 2
        self.drawer.ctx.move_to(x, y)
        self.drawer.ctx.line_to(x + w - radius, y)
        self.drawer.ctx.arc(x + w - radius, y + radius, radius, -1.57, 1.57)
        self.drawer.ctx.line_to(x, y + h)
        self.drawer.ctx.close_path()
        self.drawer.set_source_rgb(self.foreground)
        self.drawer.ctx.fill()

    def _draw_zigzag(self, x, y, w, h):
        """Dibuja una transición tipo zigzag"""
        points = [
            (x, y),
            (x + w, y + h * 0.25),
            (x, y + h * 0.5),
            (x + w, y + h * 0.75),
            (x, y + h),
        ]

        if len(points) > 0:
            self.drawer.ctx.move_to(points[0][0], points[0][1])
            for point in points[1:]:
                self.drawer.ctx.line_to(point[0], point[1])
            self.drawer.ctx.line_to(x, y + h)
            self.drawer.ctx.close_path()
            self.drawer.set_source_rgb(self.foreground)
            self.drawer.ctx.fill()
