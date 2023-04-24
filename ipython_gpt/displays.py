import IPython as ipy
from IPython.display import Markdown, display


class BaseDisplay:
    def display(self, results):
        raise NotImplementedError


class NotebookDisplay(BaseDisplay):
    TEMPLATE = "<div style='width:60%;margin-left:5%;overflow: scroll;max-height:500px'>\n\n{}\n\n</div>"

    def display(self, results):
        display(Markdown(self.TEMPLATE.format(results)))


class ShellDisplay(BaseDisplay):
    def display(self, results):
        print(results)


DISPLAY_METHODS = {
    "ZMQInteractiveShell": NotebookDisplay,
    "TerminalInteractiveShell": ShellDisplay,
}

DEFAULT_DISPLAY = ShellDisplay


def get_registered_display():
    DisplayClass = DISPLAY_METHODS.get(
        ipy.get_ipython().__class__.__name__, DEFAULT_DISPLAY
    )
    return DisplayClass()
