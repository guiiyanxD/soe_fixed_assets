from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TechnicalReportRequests(models.Model):
    _name = 'soe_fixed_assets.technical_report_requests'
    _description = 'Solicitudes de Informe Tecnico'

    nro_cite_request = fields.Char(
        string="Nro Cite Solicitud",
        required=True,
        help="Escriba el numero de cite de la solicitud del informe tecnico"
    )
    pdf_file_request = fields.Binary(
        string='Archivo PDF',
        required=True,
        attachment=True
    )
    pdf_name_request = fields.Char(
        string="Nombre del archivo PDF",
        required=True,
        help="Escriba el nombre del archivo PDF"
    )
    created_at = fields.Date(
        string="Fecha de carga",
        required=True,
        help="Fecha de creacion del archivo PDF",
        default=fields.Date.today
    )



    _sql_constraints = [
        ('unique_cite', 'unique(nro_cite)', 'El Nro de Cite debe ser unico'),
    ]