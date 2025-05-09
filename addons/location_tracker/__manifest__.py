# -*- coding: utf-8 -*-
{
    'name': 'Rastreador de Ubicación Simple',
    'version': '1.0',
    'summary': 'Obtiene y muestra la geolocalización cada 10 segundos en la consola.',
    'description': """
Este módulo utiliza la API de geolocalización del navegador para obtener
las coordenadas del usuario cada 10 segundos y las imprime en la consola
del desarrollador del navegador.
    """,
    'author': 'Tu Nombre',
    'website': 'Tu Sitio Web (Opcional)',
    'category': 'Tools',
    'depends': ['web'],  # Dependencia del módulo web de Odoo
    'data': [
        # No necesitamos vistas de datos, modelos o seguridad para este ejemplo simple
    ],
    'assets': {
        'web.assets_backend': [
            # Asegúrate de que la ruta coincide con tu estructura
            'static/src/js/geolocation.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
