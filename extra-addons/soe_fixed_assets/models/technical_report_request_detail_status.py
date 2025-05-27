from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TechnicalReportRequestDetailStatus(models.Model):
    _name = 'soe_fixed_assets.technical_report_request_detail_status'
    _description = 'Estado de la solicitud de informe tecnico'

    name = fields.Char(string="Nombre", required=True)
    description = fields.Text(string="Descripcion")