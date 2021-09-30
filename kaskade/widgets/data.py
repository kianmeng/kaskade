from rich import box
from rich.table import Table
from rich.text import Text

from kaskade.tui_widget import TuiWidget


class Data(TuiWidget):
    name = "Data"
    topic = None

    def __init__(self, config):
        super().__init__(name=self.name)
        self.config = config

    def render_content(self):
        if self.topic:
            name = self.topic[0]
            partitions = self.topic[1].partitions.items()

            title = Text()
            title.append("Name: ", style="green")
            title.append(name, style="bold magenta")
            content = Table(
                title=title,
                expand=True,
                title_justify="left",
                box=box.SIMPLE_HEAD,
                row_styles=["none", "dim"],
            )

            content.add_column(
                "id",
                justify="right",
                style="bright_green",
                header_style="bright_green bold",
                ratio=10,
            )
            content.add_column(
                "leader", style="bright_red", header_style="bright_red bold", ratio=10
            )
            content.add_column(
                "replicas",
                style="bright_blue",
                header_style="bright_blue bold",
                ratio=40,
            )
            content.add_column(
                "in sync",
                style="bright_yellow",
                header_style="bright_yellow bold",
                ratio=40,
            )

            for id, partition in partitions:
                content.add_row(
                    str(partition.id),
                    str(partition.leader),
                    str(partition.replicas),
                    str(partition.isrs),
                )

            return content
        else:
            return Text()

    def initial_state(self):
        self.topic = None
        self.has_focus = False
