#!/usr/bin/env python3
"""
app.py

MinePi - Minecraft Server on Raspberry Pi
"""
from rich.panel import Panel
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import Footer, Header, Label, Static


class TitledPanel(Vertical):
    def __init__(self, title: str, *children, **kwargs):
        super().__init__(Label(title, classes="panel-title"), *children, **kwargs)


class StardatePanel(Static):
    def render(self) -> str:
        # You can replace this with uptime or custom stardate logic
        return "🕒 Stardate 74001.1"


class MinecraftStats(Static):
    def render(self) -> str:
        return "👾 Players Online: 3\n📜 Lore Unlocks: 12"


class PiVitals(Static):
    def render(self) -> str:
        return "💻 CPU Usage: 18%\n🌡️ Temp: 45°C"


class MessageTicker(Static):
    def render(self) -> str:
        return "🛰️ All systems nominal. Awaiting commands…"


class MinePiTUI(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]
    CSS_PATH = "lcars.css"

    def compose(self) -> ComposeResult:
        yield Container(
            Container(Header(), id="header"),
            # TitledPanel("Star Date", StardatePanel(), id="stardate-panel"),
            TitledPanel(
                "System Status",
                Vertical(
                    StardatePanel(), MinecraftStats(), PiVitals(), id="status-panels"
                ),
                id="system-status",
            ),
            Horizontal(Container(MessageTicker(), id="ticker"), id="content-area"),
            Container(Footer(), id="footer"),
            id="main-container",
        )


def main():
    MinePiTUI().run()


if __name__ == "__main__":
    main()
