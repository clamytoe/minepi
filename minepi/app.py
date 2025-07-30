#!/usr/bin/env python3
"""
app.py

MinePi - Minecraft Server on Raspberry Pi
"""
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Footer, Header, Static


class StardatePanel(Static):
    def compose(self) -> ComposeResult:
        # You can replace this with uptime or custom stardate logic
        return Static("🕒 Stardate 74001.1")


class MinecraftStats(Static):
    def compose(self) -> ComposeResult:
        return Static("👾 Players Online: 3\n📜 Lore Unlocks: 12")


class PiVitals(Static):
    def compose(self) -> ComposeResult:
        return Static("💻 CPU: 18%\n🌡️ Temp: 45°C")


class MessageTicker(Static):
    def compose(self) -> ComposeResult:
        return Static("🛰️ All systems nominal. Awaiting commands…")


class MinePiTUI(App):
    CSS_PATH = "lcars.css"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Horizontal(StardatePanel(), MinecraftStats(), PiVitals()), id="main-panel"
        )
        yield MessageTicker()
        yield Footer()


if __name__ == "__main__":
    MinePiTUI().run()
