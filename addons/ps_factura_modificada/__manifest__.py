{
    'name': 'PS Campos Personalizados para Factura MATA Y MARGOLLES',
    'version': '1.0',
    'summary': 'Añade campos x_total y x_entregado a líneas de factura',
    'description': 'Este módulo añade campos personalizados a las líneas de factura y los muestra en vistas y reportes',
    'category': 'Accounting',
    'author': 'Tu Nombre',
    'depends': ['account'],
    'data': [
        'report/invoice_report_templates.xml',
        'report/external_layout_mod.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
