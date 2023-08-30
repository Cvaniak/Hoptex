from __future__ import annotations

from textual.app import ComposeResult, events
from textual.screen import ModalScreen, Screen
from textual.widgets import Static

from hoptex.configs import JUMPS, HoptexBindingConfig, HoptexWidgetsFiltersConfig
from hoptex.utils import get_focusable


class HopScreen(ModalScreen):
    """hoptex Screen that provides point to jump"""

    def __init__(
        self, bindings: HoptexBindingConfig, filters_lists: HoptexWidgetsFiltersConfig, label: type[Static]
    ) -> None:
        super().__init__()
        self._bindings.bind(*(bindings.quit, "return", "Return"))
        self.filters_lists = filters_lists
        self.label = label

    def set_parent_screen(self, screen: Screen, click: bool = False):
        self.data_screen = screen
        self.should_just_click = click

    def compose(self) -> ComposeResult:
        self.to_choose = dict()

        for idx, i in enumerate(tuple(get_focusable(self.data_screen, self.filters_lists))):
            bar = self.label(JUMPS[-1 - idx])
            self.mount(bar)
            bar.styles.layer = f"new_layer_{idx}"
            bar.styles.offset = (i.region.x, i.region.y)
            self.to_choose[JUMPS[-1 - idx]] = i

        yield from ()

    def on_key(self, event: events.Key) -> None:
        if event.key in self.to_choose:
            self.dismiss(self.to_choose[event.key])

    def action_return(self) -> None:
        self.app.pop_screen()
