import flet as ft
from ewpe import search_devices, bind_device


def main(page: ft.Page):
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

    # Container for Tabs
    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[],
        expand=1
    )
    page.add(t)

    mock_temperature = ft.TextField(value="25", text_align=ft.TextAlign.RIGHT, width=50)

    # Mock function to increase/decrease temperature
    def adjust_temperature(value):
        return value

    def minus_click(e):
        mock_temperature.value = str(int(mock_temperature.value) - 1)
        print(mock_temperature.value)
        page.update()

    def plus_click(e):
        mock_temperature.value = str(int(mock_temperature.value) + 1)
        print(mock_temperature.value)
        page.update()

    # Search button to search for AC devices
    def button_clicked(e):
        # Clear existing tabs
        t.tabs.clear()

        # Iterate through devices and add information to tabs
        for device in search_devices():
        # for device in range(1, 5):
            # temperature = mock_temperature.value

            # Decrease temperature button
            decrease_button = ft.IconButton(
                icon=ft.icons.REMOVE,
                icon_color='#FFC107',
                on_click=minus_click
            )

            # Increase temperature button
            increase_button = ft.IconButton(
                icon=ft.icons.ADD,
                icon_color='#FFC107',
                on_click=plus_click
            )

            # AC Controls
            ac_column = ft.Column(
                controls=[
                    ft.Text(
                        f"AC-IP: {device.ip}, AC ID: {device.id}, AC Name: {device.name}",
                        # f"AC-IP: {device}, AC ID: {device}, AC Name: {device}",
                        size=20,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    # ft.Text(
                    #     f"Temperature: {mock_temperature.value}°C",
                    #     size=24,
                    #     text_align=ft.TextAlign.CENTER,
                    # ),

                    #add text filed
                    mock_temperature,

                    #add icon button
                    ft.Row(
                        controls=[decrease_button, increase_button],
                        alignment=ft.alignment.center
                    )
                ],
                alignment=ft.alignment.center,
                spacing=20
            )

            # tab = ft.Tab(text=device, icon=ft.icons.AC_UNIT, content=ac_column)


            tab = ft.Tab(text=device.name, icon=ft.icons.AC_UNIT, content=ac_column)
            t.tabs.append(tab)
            page.update()

        t.selected_index = 0
        page.update()

    search_button = ft.ElevatedButton(  # Keeping this as an ElevatedButton as it has a text label
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
