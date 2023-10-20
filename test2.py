import flet as ft

def main(page: ft.Page):
    page.theme_mode = 'light'
    page.add(ft.Text('this is text'))
    # add/update controls on Page


    def newtab(i):
    tab = ft.Tab(text=f"this is tab {i}", content=ft.Container(content=ft.Text('this is the content of tab')))




ft.app(target=main)