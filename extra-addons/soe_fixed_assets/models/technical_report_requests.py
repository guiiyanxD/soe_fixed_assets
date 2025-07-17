from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TechnicalReportRequests(models.Model):
    _name = 'soe_fixed_assets.technical_report_requests'
    _rec_name = 'nro_cite_request'
    _description = 'Solicitudes de Informe Técnico'

    nro_cite_request = fields.Char(
        string="Nro Cite Solicitud",
        required=True,
        help="Escriba el numero de cite de la solicitud del informe tecnico"
    )

    date_request = fields.Date(
        string="Fecha de solicitud",
        required=True,
        help="Fecha de solicitud",
        default=fields.Date.today
    )

    technical_report_request_detail_ids = fields.One2many(
        "soe_fixed_assets.technical_report_request_detail",
        "technical_report_request_id",
        string="Detalles de la solicitud de informe técnico",
        copy=True,
        required=True,
    )



    _sql_constraints = [
        ('unique_cite_request', 'unique(nro_cite_request)', 'El Nro de Cite debe ser unico'),
    ]

    def print_technical_report_request(self):
        return True