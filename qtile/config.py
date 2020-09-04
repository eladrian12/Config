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
import os, subprocess
from typing import List  # noqa: F401
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook



mod = "mod4"
lazy.spawncmd("nitrogen --restore \n")
keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("gnome-terminal")),
    Key([mod], "c", lazy.spawn("code")),
    Key([mod], "a", lazy.spawn("pcmanfm")),
    #u2b privado 
    Key([mod], "y", lazy.spawn("firefox --private-window youtube.com")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod, "shift"], "t", lazy.spawn("teamviewer")),
    Key([mod], "f", lazy.spawn("firefox")),
    Key([mod], "t", lazy.spawn("texmaker")),
    Key([mod], "o", lazy.spawn("libreoffice7.0")),
    Key([mod], "r", lazy.spawn("dmenu_run -p 'Run: '")),
    Key([mod], "v", lazy.spawn("VBoxManage startvm 'Windows 10 '")),
    Key([mod], "b", lazy.spawn("dbeaver")),
    Key([], 'XF86AudioMute', lazy.spawn('amixer -D pulse set Master toggle')),
	#Key([], 'XF86AudioMicMute', lazy.spawn('amixer -D pulse set Master toggle')),
	Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -c 0 -q set Master 2dB+')),
	Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -c 0 -q set Master 2dB-')),
	Key([], 'XF86MonBrightnessUp', lazy.spawn('brightnessctl s +5%')),
	Key([], 'XF86MonBrightnessDown', lazy.spawn('brightnessctl s 5%-')),
	Key([mod], 'Print', lazy.spawn('gnome-screenshot -a')),
    Key([mod], "h",
    lazy.layout.grow(),
    lazy.layout.increase_nmaster(),
    desc='Expand window (MonadTall), increase number in master pane (Tile)'
    ),
    Key([mod], "l",
    lazy.layout.shrink(),
    lazy.layout.decrease_nmaster(),
    desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
    ),

    Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),

    #Key([], "XF86AudioPlay",lazy.function(playpause)),
    #Key([], "XF86AudioNext",lazy.function(next_prev("next"))),
    #Key([], "XF86AudioPrev",lazy.function(next_prev("prev")))

]

group_names = [("WWW", {'layout': 'monadtall'}),
               ("DEV", {'layout': 'monadtall'}),
               ("SSH", {'layout': 'monadtall'}),
               ("DB", {'layout': 'monadtall'}),
               ("VM", {'layout': 'monadtall'}),
               ("MEDIA", {'layout': 'monadtall'})
               ]

groups = [Group(name, **kwargs) for name, kwargs in group_names]



for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group	

layout_theme = {"border_width": 2,
                "margin": 6,
                "border_focus": "09c9f4",#"e1acff",
                "border_normal": "1D2330"
                }


layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=3),#"FF0000",
    layout.Floating(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    #layout.MonadWide(),
    # layout.RatioTile(),
    #layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
    ]

widget_defaults = dict(
    font='sans',
    fontsize=13,
    padding=1,
    
    background="07679b"
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.50),
                widget.GroupBox(hide_unused=True),
                widget.Sep(linewidth = 0,
                        padding = 100),
                widget.Prompt(),
                
                widget.WindowName(foreground="000000", font='sans bold',),
                #widget.ThermalSensor(foreground="09c9f4"),
                # widget.TextBox( "Memory",foreground="#FFFF00",name="default"),
                # widget.MemoryGraph(
                #                     width=30,
                #                     border_width=1,
                #                     border_color="#000000",
                #                     line_width=1,
                #                     frequency=5,
                #                     fill_color="EEE8AA"
                # ),
                # widget.Notify(),
                # widget.TextBox( "CPU",foreground="#FFFF00",name="default"),
                # widget.CPUGraph(width=30,
                #                 border_width=1,
                #                 border_color="#000000",
                #                 frequency=5,
                #                 line_width=1,
                #                 samples=50,),

                widget.Systray(icon_size=22),
                widget.Sep(linewidth = 0,
                        padding = 10),
                widget.Net(foreground="09c9f4"),
                widget.Volume(foreground="1afc0a"),
              
                widget.Battery(energy_now_file = "charge_now",
                                energy_full_file = "charge_full",
                                power_now_file = "current_now",
                                update_delay = 5,
                                low_percentage = 0.2,
                                low_foreground = "FF0000",
                                notify_below = True,
                                charge_char = u'↑',
                                discharge_char = u'↓',),
                widget.TextBox( "AdrianG",foreground="#FFFF00",name="default"),
                
                widget.Clock(foreground="#000000", format='%Y-%m-%d %a %I:%M %p', font='sans bold'),
                widget.QuickExit(foreground="1afc0a"),
            ],
            23,
        ), 
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])
# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
