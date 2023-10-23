from time import sleep
import matplotlib.pyplot as plt

import flet as ft


# from ewpe import search_devices, bind_device  # Commented for demonstration


def main(page: ft.Page):
    page.window_width = 450

    # Configure the page
    page.theme_mode = 'light'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Greeting Text
    hello = ft.Text(value="Ac Control APP", color="#4CAF50", size=50, text_align=ft.TextAlign.CENTER)
    page.add(hello)

    # Input field for Broadcast IP
    broadcast = ft.TextField(
        label='broadcast',
        text_align=ft.TextAlign.CENTER,
        width=300,
        height=40,
        color='#4CAF50'
    )
    page.add(broadcast)

    # ProgressBar
    pb = ft.ProgressBar(width=300, height=10, color='#4CAF50')
    page.add(pb)
    pb.visible = False  # Initially hide the progress bar

    # Container for Tabs
    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        width=440,
        indicator_tab_size=True,
        scrollable=True,
        tabs=[]
    )
    page.add(t)

    mock_temperature = ft.TextField(value=f'25', border_width=0,
                                    text_size=25, text_align=ft.TextAlign.CENTER)

    dd = ft.Dropdown(text_size=20, options=[
        ft.dropdown.Option("Cool"),
        ft.dropdown.Option("Heat"),
        ft.dropdown.Option("Dry"),
    ])

    def minus_click(e):
        mock_temperature.value = str(int(mock_temperature.value) - 1)
        page.update()

    def plus_click(e):
        mock_temperature.value = str(int(mock_temperature.value) + 1)
        page.update()

    def toggle_icon_button(e):
        e.control.selected = not e.control.selected
        e.control.update()

    # Search button to search for AC devices
    def button_clicked(e):
        pb.visible = True
        page.update()
        t.tabs.clear()

        # Using a mock loop for demonstration
        for device in range(1, 5):
            sleep(0.1)
            sw = ft.Switch(value=False)
            decrease_button = ft.IconButton(icon=ft.icons.REMOVE, icon_size=50, icon_color='#FFC107',
                                            on_click=minus_click)
            increase_button = ft.IconButton(icon=ft.icons.ADD, icon_size=50, icon_color='#FFC107', on_click=plus_click)
            toggleonoff = ft.IconButton(
                icon=ft.icons.POWER_SETTINGS_NEW,
                selected_icon=ft.icons.POWER_SETTINGS_NEW,
                on_click=toggle_icon_button,
                selected=False,
                icon_size=50,
                style=ft.ButtonStyle(bgcolor={"selected": ft.colors.BLUE_200, "": ft.colors.WHITE}),
            )

            ac_column = ft.Column(
                controls=[

                    ft.Text(f"AC-IP: {device}, AC ID: {device}, AC Name: {device}", size=20,
                            text_align=ft.alignment.center),
                    ft.Row(controls=[mock_temperature], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[decrease_button, increase_button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(controls=[toggleonoff], alignment=ft.MainAxisAlignment.CENTER),

                ],
                spacing=20
            )

            page.update()

            tab = ft.Tab(text=str(device), icon=ft.icons.AC_UNIT, content=ac_column)
            t.tabs.append(tab)

        t.selected_index = 0
        pb.visible = False
        page.update()

    search_button = ft.ElevatedButton(
        text="Search AC's",
        width=150,
        height=60,
        icon=ft.icons.AC_UNIT,
        color='#4CAF50',
        on_click=button_clicked
    )
    page.add(search_button)
    page.update()


ft.app(target=main)
