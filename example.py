from textual.app import App, ComposeResult
from textual.widgets import Button, Input, RadioButton, Switch

from hoptex import hoptex
from hoptex.configs import HoptexBindingConfig, HoptexWidgetsFiltersConfig, Static


class NotFocusableButton(Button):
    ...


widgets_filters = HoptexWidgetsFiltersConfig(block_list=[NotFocusableButton])
bindings = HoptexBindingConfig(press="ctrl+g", press_conf={"description": "Another description"})


@hoptex(widgets_filters=widgets_filters, bindings=bindings)
class DemoAppMy(App):
    def compose(self) -> ComposeResult:
        yield Input("One", classes="box")
        yield Button("Button", classes="box")
        yield Static("Static", classes="box")
        yield Switch(True, classes="box")
        yield RadioButton("Radio Button", classes="box")
        yield NotFocusableButton("Not Focusable", classes="box")


if __name__ == "__main__":
    DemoAppMy().run()
