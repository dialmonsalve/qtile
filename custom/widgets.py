from libqtile import widget

from .classes.PowerLineDecoration import PowerLineDecoration
from .utils import CustomColor, CustomFont

# from qtile_extras import widget
# from qtile_extras.widget.decorations import PowerLineDecoration


class BaseWidget:
    def __init__(
        self,
        foreground=CustomColor.white,
        background=CustomColor.white,
    ):
        self.foreground = foreground
        self.background = background

    def create_icono(self, icon):
        return widget.TextBox(
            text=icon,
            foreground=self.foreground,
            background=self.background,
            fontsize=CustomFont.icon_size,
            decorations=[PowerLineDecoration(path="arrow_right")],
        )


class CustomTemperature(BaseWidget):

    def __init__(
        self, foreground=CustomColor.white, background=CustomColor.dark_orange
    ):
        super().__init__(foreground, background)

    def thermal_sensor(self, tag_sensor, fmt, threshold=60):
        return widget.ThermalSensor(
            foreground=self.foreground,
            background=self.background,
            threshold=threshold,
            tag_sensor=tag_sensor,
            fmt=fmt,
        )

    def memory(self):
        return widget.Memory(
            foreground=self.foreground,
            background=self.background,
            decorations=[PowerLineDecoration(path="arrow_right")],
        )


class CustomNet(BaseWidget):
    def __init__(self, foreground=CustomColor.white, background=CustomColor.purple):
        super().__init__(foreground, background)

    def check_updates(self):
        return widget.CheckUpdates(
            background=self.background,
            colour_have_updates=CustomColor.red,
            colour_no_updates=CustomColor.white,
            no_update_string="0",
            display_format="Updates: {updates}",
            update_interval=60,
            distro="Arch_checkupdates",
        )

    def widget_net(self):
        return widget.Net(
            foreground=CustomColor.white,
            background=self.background,
            format="{down} -- {up}",
            interface="enp2s0f1",
            use_bits="true",
            decorations=[PowerLineDecoration(path="arrow_right")],
        )


class CustomClock(BaseWidget):
    def __init__(self, foreground=CustomColor.white, background=CustomColor.sky_blue):
        super().__init__(foreground, background)

    def clock(self):
        return widget.Clock(
            background=self.background,
            foreground=self.foreground,
            format="%d/%m/%Y %A %H:%M",
        )

    def volume(self):
        return widget.Volume(
            foreground=CustomColor.white,
            background=self.background,
            limit_max_volume=True,
            fontsize=CustomFont.font_size + 6,
            decorations=[PowerLineDecoration(path="arrow_right")],
        )


class CustomColumns(BaseWidget):
    def __init__(
        self, foreground="#ffffff", background=CustomColor.orange, fontsize=10
    ):
        self.foreground = foreground
        self.background = background
        self.fontsize = fontsize

    def current_layout_icon(self):
        return widget.CurrentLayoutIcon(
            background=self.background, scale=0.7, foreground=self.foreground
        )

    def current_layout(self):
        return widget.CurrentLayout(
            background=self.background,
            foreground=self.foreground,
            fontsize=self.fontsize,
        )
