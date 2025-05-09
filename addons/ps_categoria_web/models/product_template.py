# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class product_category(models.Model):
    _inherit = 'product.public.category'

    @api.model
    def create_model(self):
        categorias_productos = self.env['product.category'].search([])
        categorias_web = self.env['product.public.category'].search([])

        for categoria in categorias_web:
            if categoria['name'] not in categorias_productos.mapped('name'):
                _logger.info(f"no se ha encontrado la categoria {categoria['name']} en productos, procediendo a crearla")
                self.env['product.category'].create({
                    'name': categoria['name'],
                })