from email.policy import default

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # Total de unidades que tiene el pedido
    x_total_unidades_pedido = fields.Float(string='Unidades Pedido', compute='_calculo_unidades_totales_pedido', store=True)
    # Cantidad total de productos entregados
    x_total_unidades_entregadas = fields.Float(string='Unidades', compute='_calculo_unidades_totales_entregadas', store=True, default=0)
    # Precio total de todos los productos entregados
    x_precio_total_unidades_entregadas = fields.Float(string='Precio Total Entregado', compute='_calculo_total_unidades_entregadas', store=True)
    # Cantidad de unidades certificadas previamente a la creación de la factura
    x_unidades_certificadas = fields.Float(string='Total Certificado', compute='_compute_x_entregado', store=True, default=0)
    x_precio_unidades_certificadas = fields.Float(string='Cantidad Certificada', compute='_compute_x_cantidad_certificada', store=True)

    # Calcula el total de unidades del pedido
    @api.depends('sale_line_ids', 'sale_line_ids.product_uom_qty')
    def _calculo_unidades_totales_pedido(self):
        for line in self:
            line.x_total_unidades_pedido = sum(line.sale_line_ids.mapped('product_uom_qty'))

    # Calcula el total de unidades entregadas
    @api.depends('sale_line_ids', 'sale_line_ids.product_uom_qty')
    def _calculo_unidades_totales_entregadas(self):
        for line in self:
            if line.x_total_unidades_entregadas == 0:
                line.x_total_unidades_entregadas = sum(line.sale_line_ids.mapped('qty_delivered'))

    # Calcula el precio del total de unidades entregadas
    @api.depends('sale_line_ids', 'sale_line_ids.qty_delivered')
    def _calculo_total_unidades_entregadas(self):
        for line in self:
            line.x_precio_total_unidades_entregadas = line.x_total_unidades_entregadas * line.price_unit

    # Calcula las unidades certificadas previamente a la creación de la factura
    @api.depends('sale_line_ids', 'sale_line_ids.qty_delivered')
    def _compute_x_entregado(self):
        for line in self:
            if line.x_unidades_certificadas == 0:
                certificado = sum(line.sale_line_ids.mapped('qty_delivered')) - line.quantity
                if certificado < 0:
                    certificado = 0
                line.x_unidades_certificadas = certificado

    # Calcula precio de las unidades certificadas previamente a la creación de la factura
    @api.depends('sale_line_ids', 'sale_line_ids.qty_delivered')
    def _compute_x_cantidad_certificada(self):
        for line in self:
            line.x_precio_unidades_certificadas = line.x_unidades_certificadas*line.price_unit


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_numero_certifiacion = fields.Integer(string='Número de Certificación', store=True, compute='_compute_x_numero_certifiacion')

    @api.depends('invoice_line_ids', 'invoice_line_ids.sale_line_ids')
    def _compute_x_numero_certifiacion(self):
        for move in self:


            # Obtener las órdenes de venta relacionadas con esta factura
            sale_orders = move.invoice_line_ids.mapped('sale_line_ids.order_id')
            if not sale_orders:
                move.x_numero_certifiacion = 0
                continue

            # Para simplificar, tomamos la primera orden de venta relacionada
            main_sale_order = sale_orders[0]

            # Obtener todas las facturas relacionadas con esta orden de venta
            related_invoices = self.env['account.move'].search([
                ('move_type', 'in', ['out_invoice', 'out_refund']),
                ('invoice_line_ids.sale_line_ids.order_id', '=', main_sale_order.id),
                ('state', '!=', 'cancel')
            ], order='invoice_date, id')

            # Encontrar la posición de la factura actual en la secuencia
            position = 0
            for i, inv in enumerate(related_invoices, 1):
                if inv.id == move.id:
                    position = i
                    break

            move.x_numero_certifiacion = position
