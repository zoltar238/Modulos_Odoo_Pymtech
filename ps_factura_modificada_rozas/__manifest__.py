{
    'name': 'Campos Personalizados para La Factura de Rozas y Tapados Alba',
    'version': '1.0',
    'summary': 'Añade campos x_total y x_entregado a líneas de factura',
    'description': 'Este módulo añade campos personalizados a las líneas de factura y los muestra en vistas y reportes',
    'category': 'Accounting',
    'author': 'Tu Nombre',
    'depends': ['account'],
    'data': [
        'views/account_move_views.xml',
        'report/invoice_body.xml',
        'report/invoice_header.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
