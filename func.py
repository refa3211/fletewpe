import


def minus_click(e):
    mock_temperature.value = str(int(mock_temperature.value) - 1)
    page.update()

def plus_click(e):
    mock_temperature.value = str(int(mock_temperature.value) + 1)
    page.update()

def toggle_icon_button(e):
    e.control.selected = not e.control.selected
    e.control.update()

