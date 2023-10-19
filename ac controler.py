import flet as ft
import socket
from flet_core import text, Text, KeyboardEvent, TextAlign, TextField

from ewpe import search_devices, bind_device, get_param


def main(page: ft.Page):
    def on_hover(e):
        e.control.bgcolor = "blue" if e.data == "true" else "red"
        e.control.update()

    def long_press(e):
        e.control.bgcolor = "yellow" if e.data == "true" else "green"
        e.control.update()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # add hello text
    hello: Text = Text(value="Hello, world!", color="green", size=50, text_align=ft.TextAlign.RIGHT)
    page.add(hello)

    # add text filed for broadcast ip
    broadcast: TextField = TextField(label='broadcast', text_align=ft.TextAlign.LEFT, width=200)
    page.add(broadcast)

    # function activated by button
    def button_clicked(e):
        page.add(ft.Text(broadcast.value))
        page.add(ft.Row(controls=[ft.TextField(label="Choose AC")], alignment=ft.MainAxisAlignment.CENTER))

        page.add(ft.Column(
            [
                ft.Container(
                    content=ft.Text("click Container4"),
                    margin=10,
                    padding=10,
                    width=200,
                    height=200,
                    alignment=ft.alignment.center,
                    on_click=None,
                    on_hover=on_hover,
                    bgcolor='green',
                    on_long_press=long_press)
            ]))

        for i in search_devices():
            page.controls.append(ft.Text(f"AC-IP: {i.ip}, AC ID: {i.id}, AC Name: {i.name}"))
            page.controls.append(ft.Text(f"bind_device: {bind_device(i)}\n"))

            # create button get param

            page.add(ft.ElevatedButton(text=f"{i.ip}", width=150, height=70,
                                       icon=ft.icons.AC_UNIT,
                                       on_click=get_param(i.id, bind_device(i), i.ip)))

        page.scroll = "always"
        page.update()

    # the button
    page.add(ft.ElevatedButton(text="Search AC's", width=130, height=70,
                               icon=ft.icons.AC_UNIT, on_click=button_clicked))

    page.scroll = "always"
    page.update()


ft.app(target=main, port=7818)
