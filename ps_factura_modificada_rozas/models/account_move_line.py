from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    x_total = fields.Float(string='Total Pedido', compute='_compute_x_total', store=True)
    x_entregado = fields.Float(string='Total Certificado', compute='_compute_x_entregado', store=True)

    @api.depends('sale_line_ids', 'sale_line_ids.product_uom_qty')
    def _compute_x_total(self):
        for line in self:
            line.x_total = sum(line.sale_line_ids.mapped('product_uom_qty'))

    @api.depends('sale_line_ids', 'sale_line_ids.qty_delivered')
    def _compute_x_entregado(self):
        for line in self:
            line.x_entregado = sum(line.sale_line_ids.mapped('qty_delivered'))
