from nicegui import ui

from ..services.server_service import check_server_status

server_status = check_server_status('194.164.164.122')


def open_add_server_dialog():
    with ui.dialog() as dialog, ui.card():
        ui.label('Añadir server')
        ui.textarea(label="IP")
        ui.textarea()

    dialog.open()
    # Consider moving ui.notify into the dialog logic or after a successful add
    # ui.notify('Añadido') # This will show immediately when the button is clicked


ui.button('Añadir servidor', on_click=open_add_server_dialog)

with ui.row():
    with ui.card().tight():
        ui.image('../../resources/images/placeholder.png')
        with ui.card_section():
            ui.label(f'{server_status}')
    ui.label(f'{server_status}')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
    ui.label('This is a new label')
ui.run(port=9090)
