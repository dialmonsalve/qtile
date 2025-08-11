# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import subprocess

from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Group, Key, Match, Screen
from libqtile.lazy import lazy

from custom.keymaps import keys, mod
from custom.utils import CustomColor, CustomFont, CustomOthers

from custom.widgets import CustomClock, CustomColumns, CustomNet, CustomTemperature

from custom.classes.PowerLineDecoration import PowerLineDecoration

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

custom_temp = CustomTemperature()
custom_net = CustomNet()
custom_clock = CustomClock()
custom_columns = CustomColumns(
    background=CustomColor.dark_gray,
    fontsize=CustomFont.font_size + 4,
)

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
layouts = [
    layout.TreeTab(
        active_bg=CustomColor.dark_orange,
        bg_color=CustomColor.dark_purple,
        active_fg=CustomColor.white,
        inactive_bg=CustomColor.white,
        inactive_fg=CustomColor.dark_orange,
    ),
    layout.Columns(
        margin=0,
        border_focus=CustomColor.purple,
        border_normal=CustomColor.dark_gray,
        border_width=3,
    ),
    # layout.Max( ),
    ## layout.Stack(num_stacks=2),
    ## layout.Bsp(),
    # layout.Matrix( ),
    # layout.MonadWide( ),
    # layout.Tile(),
    # layout.Plasma(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]


widget_defaults = {
    "font": "JetBrainsMono Nerd Font",
    "fontsize": 12,
    "padding": 3,
}

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active=CustomColor.orange,
                    background=CustomColor.dark_gray,
                    border_width=CustomOthers.border_width,
                    disabled_drag=True,
                    fontsize=CustomFont.font_size + 4,
                    foreground=CustomColor.purple,
                    highlight_method="block",
                    inactive=CustomColor.lighter_blue,
                    margin_x=8,
                    margin_y=4,
                    other_current_screen_border=CustomColor.gray,
                    other_screen_border=CustomColor.gray,
                    rounded=True,
                    this_current_screen_border=CustomColor.light,
                    this_screen_border=CustomColor.light,
                    urgent_alert_method="block",
                    urgent_border=CustomColor.urgent,
                ),
                custom_columns.current_layout_icon(),
                custom_columns.current_layout(),

                widget.Spacer(length=10, background=CustomColor.dark_gray),
                widget.Spacer(length=50, background=CustomColor.dark_gray),
                widget.Prompt(),
                widget.WindowName(
                    foreground=CustomColor.light,
                    background=CustomColor.dark_gray,
                    fontsize=12,
                ),
                custom_temp.create_icono(""),
                custom_temp.thermal_sensor(tag_sensor="Core 0", fmt="T1:{}"),
                custom_temp.thermal_sensor(tag_sensor="Core 1", fmt="T2:{}"),
                widget.Spacer(length=10, background=CustomColor.dark_gray),
                widget.CPU(
                    background=CustomColor.gray,
                    foreground=CustomColor.white,
                    format="CPU: {load_percent}%",
                ),
                widget.Spacer(length=10, background=CustomColor.dark_gray),
                custom_temp.memory(),
                widget.Spacer(length=10, background=CustomColor.dark_gray),
                custom_net.create_icono("󰁪"),
                custom_net.check_updates(),
                custom_net.create_icono("󰓅"),
                custom_net.widget_net(),
                widget.Spacer(length=10, background=CustomColor.dark_gray),
                custom_clock.clock(),
                # custom_clock.create_icono(""),
                # custom_clock.volume(),
                widget.Chord(
                    chords_colors={
                        "launch": (CustomColor.orange, "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),

                widget.Notify(action=True),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
            ],
            20,
            border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            margin=[0,10,10,10],
            opacity=0.5,
            border_color=[CustomColor.dark_purple, "000000", CustomColor.dark_purple, "000000"]  # Borders are magenta
        ),
        bottom=bar.Bar(
            [
                widget.TextBox("default config", name="default", foreground=CustomColor.dark_gray),
                widget.TextBox(
                    "Press &lt;M-r&gt; to search", foreground=CustomColor.gray
                ),
                widget.QuickExit(foreground=CustomColor.gray),
            ],
            24,
            background=CustomColor.orange
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.


dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile")
    subprocess.Popen([home + "/autostart.sh"])
    print(qtile.core.name)
