from __future__ import annotations

from collections.abc import Iterator

from textual.widget import Widget, events

from hoptex.configs import HoptexWidgetsFiltersConfig

DUMMY_MOUSE_EVENT = events.Click(0, 0, 0, 0, 0, False, False, False, False)


def focusable_children(widget: Widget) -> list[Widget]:
    focusable = [child for child in widget._nodes if child.display and child.visible]
    return focusable


def get_focusable(widget: Widget, filter_lists: HoptexWidgetsFiltersConfig):
    widgets: list[Widget] = []
    add_widget = widgets.append
    stack: list[Iterator[Widget]] = [iter(focusable_children(widget))]
    pop = stack.pop
    push = stack.append

    while stack:
        node = next(stack[-1], None)
        if node is None:
            pop()
        else:
            if type(node) in filter_lists.block_list:
                continue
            if node.is_container and node.can_focus_children:
                push(iter(node.focusable_children))
            if filter_lists.include_focusable and node.focusable:
                add_widget(node)
            elif type(node) in filter_lists.allow_list:
                add_widget(node)

    return widgets
