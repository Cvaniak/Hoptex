from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, Union

from textual.widgets import Static

if TYPE_CHECKING:
    from typing_extensions import TypeAlias


BINDING_QUIT_HOP = "escape"
BINDING_START_HOP = "space"
BINDING_PRESS_HOP = "ctrl+o"

BINDING_UNFOCUS_HOP = "escape"

JUMPS = "asdghklqwertyuiopzxcvbnmfj"

ConfType: TypeAlias = Dict[str, Union[str, bool]]


@dataclass
class HoptexBindingConfig:
    focus: str = BINDING_START_HOP
    press: str = BINDING_PRESS_HOP
    quit: str = BINDING_QUIT_HOP
    unfocus: str = BINDING_UNFOCUS_HOP

    focus_conf: ConfType = field(default_factory=lambda: {"description": "Hop Focus"})
    press_conf: ConfType = field(default_factory=lambda: {"description": "Hop Press"})
    quit_conf: ConfType = field(default_factory=lambda: {"description": "Hop Quit", "show": False})
    unfocus_conf: ConfType = field(default_factory=lambda: {"description": "Hop Unfocus", "show": False})


@dataclass
class HoptexWidgetsFiltersConfig:
    include_focusable: bool = True
    allow_list: list[type] = field(default_factory=lambda: [])
    block_list: list[type] = field(default_factory=lambda: [])


class HopLabel(Static):
    DEFAULT_CSS = """
    HopLabel {
        width: auto;
        height: 1;
        color: yellow;
        text-style: bold;
        background: black;
    }
    """
