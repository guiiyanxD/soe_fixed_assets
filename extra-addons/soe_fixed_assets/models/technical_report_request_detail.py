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
    asset_code = fields.Char(
        related = 'asset_id.code',
        string="Codigo",
        required=True,
        readonly=True
    )
    asset_brand = fields.Char(
        related = 'asset_id.brand',
        string="Marca",
        required=True,
        readonly=True

    )
    asset_description = fields.Char(
        related = 'asset_id.description',
        string="Descripcion",
        required=True,
        readonly=True

    )
    asset_quality = fields.Char(
        related = 'asset_id.quality_id.name',
        string="Calidad",
        required=True,
        readonly=True

    )
    technical_report_request_id = fields.Many2one(
        "soe_fixed_assets.technical_report_requests",
        string="Solicitud de Informe Tecnico",
        required=False,
    )
    technical_report_request_id_nro_cite = fields.Char(
        related= "technical_report_request_id.nro_cite_request",
        string="Nro Cite de la Solicitud de Informe Tecnico",
        readonly=True,
    )
    technical_report_status_id = fields.Many2one(
        "soe_fixed_assets.technical_report_request_detail_status",
        string="Estado de la solicitud de informe tecnico",
        required=True,
    )
    comments = fields.Text(string="Comentarios", required=True)

    _sql_constraints = [
        ('unique_asset',
         'unique(asset_id, technical_report_request_id)',
         'Este activo ya existe en esta solicitud'
         ),
    ]

    @api.constrains('request_id', 'asset_id')
    def _check_duplicate_assets(self):
        for record in self:
            duplicates = self.search([
                ('technical_report_request_id', '=', record.technical_report_request_id.id),
                ('asset_id', '=', record.asset_id.id),
                ('id', '!=', record.id),
            ])
            if duplicates:
                raise ValidationError("No puedes añadir el mismo activo más de una vez en la misma solicitud.")


    def action_ver_solicitud(self):
        """
        Este método abre la vista formulario del acta de recepción relacionada con el activo fijo.
        """
        self.ensure_one()  # Asegura que self es un solo registro
        return {
            'type': 'ir.actions.act_window',
            'name': 'Solciitud Informe Tecnico',
            'view_mode': 'form',
            'res_model': 'soe_fixed_assets.technical_report_requests',
            'res_id': self.technical_report_request_id.id,  # Abre el registro específico del acta
            'target': 'current',  # La vista se abre en la misma ventana
        }

    def action_recibir_informe(self):
        """
        Este método abre la vista formulario del acta de recepción relacionada con el activo fijo.
        """
        self.ensure_one()  # Asegura que self es un solo registro
        return {
            'type': 'ir.actions.act_window',
            'name': 'Solciitud Informe Tecnico',
            'view_mode': 'form',
            'res_model': 'soe_fixed_assets.technical_report_requests',
            'res_id': self.technical_report_request_id.id,  # Abre el registro específico del acta
            'target': 'current',  # La vista se abre en la misma ventana
        }