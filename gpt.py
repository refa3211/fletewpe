import asyncio
import flet
import flet as ft


class MainApp:
    def __init__(self):
        self.page = None
        self.b = None
        self.elements = {}

    async def button_clicked(self, e):
        t = self.elements['text']
        pb = self.elements['progress_bar']
        b = self.elements['button']

        t.value = "Doing something..."
        pb.visible = True
        b.disabled = True
        self.page.update()

        async def perform_async_task():
            for i in range(0, 101):
                pb.value = i * 0.01
                await asyncio.sleep(0.1)

            t.value = "Click the button..."
            pb.visible = False
            b.disabled = False
            self.page.update()

        asyncio.create_task(perform_async_task())

    def main(self, page: ft.Page):
        self.page = page
        page.theme_mode = 'light'
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        hello = ft.Text(value="Ac Control APP", color="#4CAF50", size=50, text_align=ft.TextAlign.CENTER)
        page.add(hello)

        self.elements['text'] = ft.Text(value="Click the button")
        page.add(self.elements['text'])

        self.elements['progress_bar'] = ft.ProgressBar(width=400, value=0)
        page.add(self.elements['progress_bar'])
        self.elements['progress_bar'].visible = False  # Initially hide the progress bar

        b = ft.FilledTonalButton("Start", on_click=self.button_clicked)
        page.add(b)
        self.elements['button'] = b

        return ft.Column(
            [
                ft.Text("Linear progress indicator", style=ft.TextThemeStyle.HEADLINE_SMALL),
                ft.Column([self.elements['text'], self.elements['progress_bar']]),
                ft.Text("Indeterminate progress bar", style=ft.TextThemeStyle.HEADLINE_SMALL),
                ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee"),
                b,
            ],
            width=400,
            height=400,
        )

    def run(self):
        flet.app(target=self.main)


if __name__ == "__main__":
    app = MainApp()
    app.run()
