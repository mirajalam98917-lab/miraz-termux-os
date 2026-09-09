
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class MirazOS(App):
    def build(self):
        root = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=8
        )

        root.add_widget(Label(
            text=(
                "[color=00ffff][b]MIRAZ[/b][/color]\n"
                "[color=ff00ff]TERMUX OS[/color]\n"
                "[color=ffff00]4D DAILY TOOLBOX[/color]"
            ),
            markup=True,
            font_size="26sp"
        ))

        for x in [
            "01 MONEY & CALCULATION",
            "02 STUDY CENTER",
            "03 PRODUCTIVITY",
            "04 PHONE / SYSTEM",
            "05 FILE TOOLS",
            "06 SECURITY",
            "07 CODING",
            "08 NETWORK",
            "09 QUICK ACCESS",
        ]:
            root.add_widget(
                Button(
                    text=x,
                    size_hint_y=None,
                    height=45
                )
            )

        root.add_widget(
            Button(
                text="00 EXIT",
                size_hint_y=None,
                height=45
            )
        )

        return root


MirazOS().run()
