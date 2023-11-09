from time import sleep
from flet import Page
import flet as ft
from ewpe import search_devices, bind_device  # Commented for demonstration

# function


page = ft.Page()


def minus_click(e):
    global page
    mock_temperature.value = str(int(mock_temperature.value) - 1)
    page.update()


def plus_click(e):
    global page
    mock_temperature.value = str(int(mock_temperature.value) + 1)
    page.update()


def toggle_icon_button(e):
    global page
    e.control.selected = not e.control.selected
    e.control.update()


# Search button to search for AC devices
def button_clicked(e):
    global page
    pb.visible = True
    page.update()
    t.tabs.clear()

    # Using a mock loop for demonstration
    # for device in range(1, 5):
    #     sleep(0.1)

    for device in search_devices():
        print(device.name, device.ip, )

        decrease_button = ft.IconButton(
            icon=ft.icons.REMOVE, icon_size=50, icon_color='#FFC107', on_click=minus_click(page))
        increase_button = ft.IconButton(
            icon=ft.icons.ADD, icon_size=50, icon_color='#FFC107', on_click=plus_click)

        toggleonoff = ft.IconButton(
            icon=ft.icons.POWER_SETTINGS_NEW,
            selected_icon=ft.icons.POWER_SETTINGS_NEW,
            on_click=toggle_icon_button,
            selected=False,
            icon_size=50,
            style=ft.ButtonStyle(bgcolor={"selected": ft.colors.LIGHT_BLUE_50, "": ft.colors.WHITE}),
        )

        ac_column = ft.Column(
            controls=[
                ft.Text(f"AC-IP: {device.ip}, AC ID: {device.id}, AC Name: {device.name}", size=20,
                        text_align=ft.alignment.center),
                ft.Row(controls=[dd], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(controls=[decrease_button, mock_temperature, increase_button],
                       alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(controls=[toggleonoff], alignment=ft.MainAxisAlignment.CENTER),
            ],
            spacing=20
        )

        page.update()

        tab = ft.Tab(text=str(device.ip), content=ac_column)
        t.tabs.append(tab)

    t.selected_index = 0
    pb.visible = False
    page.update()


if __name__ == '__main__':
    page.window_width = 500

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
        # width=440,
        indicator_tab_size=True,
        scrollable=False,
        tabs=[]
    )
    page.add(t)

    mock_temperature = ft.TextField(value=f'25', border_width=0,
                                    text_size=25, width=55, text_align=ft.TextAlign.CENTER)

    dd = ft.Dropdown(text_size=20, width=75, hint_text='Mode',
                     height=60, border_width=0.2,
                     options=[
                         ft.dropdown.Option("Auto"),
                         ft.dropdown.Option("Dry"),
                         ft.dropdown.Option("Cool"),
                         ft.dropdown.Option("Heat"),
                     ])
    ft.app()
