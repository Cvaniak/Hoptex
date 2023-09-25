from __future__ import annotations

import itertools
from typing import Iterable

from textual.app import ComposeResult, events
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Static

from hoptex.configs import JUMPS, HoptexBindingConfig, HoptexWidgetsFiltersConfig
from hoptex.utils import get_focusable


def _generate_label(n):
    elements = reversed(JUMPS)
    if n < 26:
        yield from elements
    else:
        yield from ("".join(p) for p in itertools.product(elements, repeat=2))


class HopScreen(ModalScreen):
    """hoptex Screen that provides point to jump"""

    def __init__(
        self, bindings: HoptexBindingConfig, filters_lists: HoptexWidgetsFiltersConfig, label: type[Static]
    ) -> None:
        super().__init__()
        self._bindings.bind(*(bindings.quit, "return", "Return"))
        self.filters_lists = filters_lists
        self.label = label
        self.finall_key = ""
        self.parent_widgets = set()

    def set_parent_screen(self, parent_widgets: Iterable[Widget], click: bool = False):
        self.parent_widgets = parent_widgets
        self.should_just_click = click

    def compose(self) -> ComposeResult:
        self.to_choose = dict()
        self.to_choose_bar = dict()
        self.to_choose_set = set()

        z = set()
        for parent_widget in self.parent_widgets:
            for widget in get_focusable(parent_widget, self.filters_lists):
                z.add(widget)

        laberer = _generate_label(len(z))

        for idx, i in enumerate(z):
            label_text = next(laberer)
            bar = self.label(label_text)
            self.mount(bar)
            bar.styles.layer = f"new_layer_{idx}"
            bar.styles.offset = (i.region.x, i.region.y)
            self.to_choose[label_text] = i
            self.to_choose_bar[label_text] = bar
            for i in range(len(label_text)):
                self.to_choose_set.add(label_text[: i + 1])

        yield from ()

    def _adjust_to_new_letter(self, finall_key):
        items = self.to_choose.keys()
        bar: Static
        for letter in items:
            bar = self.to_choose_bar[letter]
            if letter.startswith(finall_key):
                bar.update(str(bar.renderable)[1:])
            else:
                self.to_choose_set.discard(letter)
                bar.remove()
                del self.to_choose_bar[letter]

    def on_key(self, event: events.Key) -> None:
        finall_key = self.finall_key + event.key
        if finall_key in self.to_choose:
            self.dismiss(self.to_choose[finall_key])
            return
        if finall_key not in self.to_choose_set:
            return
        self._adjust_to_new_letter(finall_key)
        self.finall_key = finall_key

        return

    def action_return(self) -> None:
        self.app.pop_screen()
