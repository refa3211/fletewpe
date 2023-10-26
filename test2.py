import flet
import fontTools.varLib.iup
import flet as ft
from flet import Dropdown, Page, colors, dropdown


def main(page: Page):
    page.theme_mode = 'light'
    page.padding = 50
    page.add(
        Dropdown(
            options=[
                dropdown.Option("a", "Item A"),
                dropdown.Option("b", "Item B"),
                dropdown.Option("c", "Item C"),
                dropdown.Option(f'{ft.icons.BED}'),
            ],
            border_radius=30,
            filled=True,
            width=100,
            border_color=colors.TRANSPARENT,
            bgcolor=colors.BLACK12,
            focused_bgcolor=colors.BLUE_100,
            icon=ft.icons.BED
            # color=colors.TRANSPARENT
        )
    )


flet.app(target=main)