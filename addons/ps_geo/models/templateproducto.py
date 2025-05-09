# -*- coding: utf-8 -*-
from odoo import models, fields, api


class productos_addons(models.Model):
    _inherit = 'hr.attendance'

    x_latitude = fields.Float(string='Latitud', store=True)
    x_longitude = fields.Float(string='Longitud', store=True)

    def _no_action(self):
        print("hola")

