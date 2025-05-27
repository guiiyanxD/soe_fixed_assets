from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TechnicalReportRequestDetail(models.Model):
    _name = 'soe_fixed_assets.technical_report_request_detail'
    _description = 'Detalles de la solicitud de informe tecnico'

    asset_id = fields.Many2one(
        "soe_fixed_assets.asset",
        string="Activo fijo",
        required=True
    )
    technical_report_request_id = fields.Many2one(
        "soe_fixed_assets.technical_report_requests",
        string="Solicitud de Informe Tecnico",
        required=True,
    )
    comments = fields.Text(string="Comentarios")
