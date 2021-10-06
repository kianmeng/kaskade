from textual.app import App
from textual.keys import Keys

from kaskade.kafka import Kafka
from kaskade.utils.circular_list import CircularList
from kaskade.widgets.body import Body
from kaskade.widgets.footer import Footer
from kaskade.widgets.header import Header
from kaskade.widgets.sidebar import Sidebar


class Tui(App):
    def __init__(
        self,
        console=None,
        screen=True,
        driver_class=None,
        log="",
        log_verbosity=1,
        config=None,
    ):
        super().__init__(
            console=console,
            screen=screen,
            driver_class=driver_class,
            log=log,
            log_verbosity=log_verbosity,
        )
        self.config = config
        self.kafka = Kafka(self.config)
        self.topics = self.kafka.topics()
        self.topic = None

        self.sidebar = Sidebar()
        self.body = Body()
        self.footer = Footer()
        self.header = Header()
        self.focusables = CircularList([self.sidebar, self.body])

    async def on_mount(self):
        await self.view.dock(self.header, edge="top")
        await self.view.dock(self.footer, edge="bottom")
        await self.view.dock(self.sidebar, edge="left", size=40)
        await self.view.dock(self.body, edge="right")

    async def on_load(self):
        await self.bind("q", "quit")
        await self.bind(Keys.F5, "reload_content")

        await self.bind(Keys.Left, "change_focus('{}')".format(Keys.Left))
        await self.bind(Keys.Right, "change_focus('{}')".format(Keys.Right))

        await self.bind(Keys.Down, "on_key_press('{}')".format(Keys.Down))
        await self.bind(Keys.Up, "on_key_press('{}')".format(Keys.Up))

    async def action_reload_content(self):
        self.topics = self.kafka.topics()
        self.topic = None
        self.focused = None
        self.body.has_focus = False
        self.sidebar.has_focus = False

    async def action_on_key_press(self, key):
        if not self.focused:
            return

        self.focused.on_key_press(key)

    async def action_change_focus(self, key):
        if self.focused:
            self.focused.has_focus = False

        if key == Keys.Right:
            self.focused = self.focusables.next()
        else:
            self.focused = self.focusables.previous()

        self.focused.has_focus = True
