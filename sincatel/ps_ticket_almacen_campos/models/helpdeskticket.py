import tempfile
import sys
sys.path.insert(0, '/opt/whisper_env/lib/python3.12/site-packages')
import whisper
import base64
from odoo import models, fields, api
from datetime import datetime

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    x_warehouse = fields.Many2one(
        'stock.warehouse', 
        string="Almacén", 
        compute='_compute_x_warehouse',
        readonly=True,
        store=False,
        help="Este almacén se asigna automáticamente según el usuario asignado al ticket."
    )

    x_support_user1 = fields.Many2one(
        'res.users',
        string="Usuario Soporte 1"
    )
    x_support_user2 = fields.Many2one(
        'res.users',
        string="Usuario Soporte 2"
    )
    x_support_user3 = fields.Many2one(
        'res.users',
        string="Usuario Soporte 3"
    )

    audio_file = fields.Binary(string="Archivo de audio", attachment=True)
    audio_filename = fields.Char(string="Nombre audio")
    transcription_text = fields.Text(string="Transcripción")

    def transcribe_audio(self):
        for record in self:
            if not record.audio_file:
                continue

            # Guardar temporalmente el archivo
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp.write(base64.b64decode(record.audio_file))
                tmp_path = tmp.name

            # Cargar el modelo Whisper (pequeño por rendimiento)
            model = whisper.load_model("base",device="cpu")
            result = model.transcribe(tmp_path)

            record.transcription_text = result.get("text", "")


    x_firma_cliente = fields.Binary('Firma del cliente')

    x_visibility_tick_empezar = fields.Boolean('x_visibility_tick_empezar', default=True)
    x_visibility_tick_salida = fields.Boolean('x_visibility_tick_salida', default=False)
    x_visibility_firma = fields.Boolean('x_visibility_firma', default=False)

    def action_empezar_actuacion(self, *args, **kwargs):
        self.ensure_one()
        for ticket in self:
            ticket.fecha_aviso = fields.Datetime.now()
            ticket.x_visibility_tick_empezar = False
            ticket.x_visibility_tick_salida = True

    def action_salida_actuacion(self, *args, **kwargs):
        self.ensure_one()
        for ticket in self:
            ticket.fecha_salida = fields.Datetime.now()
            ticket.x_visibility_tick_salida = False
            ticket.x_visibility_firma = True


    def action_crear_presupuesto(self):
        self.ensure_one()

        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'ticket_id': self.id,
            'warehouse_id': self.x_warehouse.id,
        })

        for ticket in self:
            ticket.fecha_salida = fields.Datetime.now() 

        return {
            'type': 'ir.actions.act_window',
            'name': 'Presupuesto',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': sale_order.id,
            'target': 'current',
        }
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('user_id'):
                user = self.env['res.users'].browse(vals['user_id'])
                vals['x_warehouse'] = user.property_warehouse_id.id or False
        return super().create(vals_list)

    def write(self, vals):
        if 'user_id' in vals:
            user = self.env['res.users'].browse(vals['user_id'])
            vals['x_warehouse'] = user.property_warehouse_id.id or False
        return super().write(vals)

    @api.depends('user_id')
    def _compute_x_warehouse(self):
        for ticket in self:
            ticket.x_warehouse = ticket.user_id.property_warehouse_id

    # Geolocalización

    latitude = fields.Float('Latitude', string='Latitud')
    longitude = fields.Float('Longitude', string='Longitud')

    