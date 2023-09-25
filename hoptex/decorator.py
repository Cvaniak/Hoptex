from __future__ import annotations

import inspect
from typing import Any, Optional

from textual.app import App
from textual.widget import Widget
from textual.widgets import Static

from hoptex.configs import HopLabel, HoptexBindingConfig, HoptexWidgetsFiltersConfig
from hoptex.hop_screen import HopScreen
from hoptex.utils import DUMMY_MOUSE_EVENT


async def _action_hoptex_screen_choose(self: App, focus_and_press: bool = False) -> None:
    bindings = getattr(self, "_hoptex_bindings", None)
    filter_lists = getattr(self, "_hoptex_filter_lists", None)
    label = getattr(self, "_hoptex_label", HopLabel)

    if not bindings or not filter_lists:
        raise AttributeError("Missing bindings or filter lists")

    screen = HopScreen(bindings, filter_lists, label)

    parent_widgets = getattr(self, "_hoptex_parent_widgets", set()) or {self.screen}

    screen.set_parent_screen(parent_widgets)

    async def _perform_action(widget: Widget):
        for function, attrs, kwargs in [("_on_click", [DUMMY_MOUSE_EVENT], {}), ("on_click", [], {})]:
            if not hasattr(widget, function):
                continue

            if inspect.iscoroutinefunction(getattr(widget, function)):
                await getattr(widget, function)(*attrs, **kwargs)
            else:
                getattr(widget, function)(*attrs, **kwargs)

    async def change_focus(widget: Widget):
        self.set_focus(widget)
        if not focus_and_press:
            return

        await _perform_action(widget)

    self.push_screen(screen, change_focus)


async def _action_hoptex_unfocus(self: App) -> None:
    self.screen.set_focus(None)


def set_parent_widgets(self, widgets: list[Widget]):
    self._hoptex_parent_widgets = widgets


def hoptex(
    cls: Optional[type[Any]] = None,
    *,
    bindings: HoptexBindingConfig = HoptexBindingConfig(),
    widgets_filters: HoptexWidgetsFiltersConfig = HoptexWidgetsFiltersConfig(),
    label: type[Static] = HopLabel,
):
    def _hoptex_decorator(cls: type[Any]) -> type[Any]:
        original_init = cls.__init__

        def hoptex_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self._bindings.bind(*(bindings.focus, "hoptex_screen_choose"), **bindings.focus_conf)
            self._bindings.bind(*(bindings.press, "hoptex_screen_choose(True)"), **bindings.press_conf)
            self._bindings.bind(*(bindings.quit, "hoptex_unfocus"), **bindings.quit_conf)

        cls.__init__ = hoptex_init

        setattr(cls, "_action_hoptex_screen_choose", _action_hoptex_screen_choose)
        setattr(cls, "_action_hoptex_unfocus", _action_hoptex_unfocus)

        setattr(cls, "_hoptex_bindings", bindings)
        setattr(cls, "_hoptex_filter_lists", widgets_filters)

        setattr(cls, "_hoptex_label", label)

        setattr(cls, "set_parent_widgets", set_parent_widgets)

        return cls

    if cls is None:
        return _hoptex_decorator

    return _hoptex_decorator(cls)
