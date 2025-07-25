from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class TechnicalReportRequestDetail(models.Model):
    _name = 'soe_fixed_assets.technical_report_request_detail'
    _description = 'Detalles de la solicitud de informe tecnico'

    asset_id = fields.Many2one(
        "soe_fixed_assets.asset",
        string="Activo fijo",
        required=True,
        domain="[('availability', '=', 'available')]",
    )

    technical_report_request_id = fields.Many2one(
        "soe_fixed_assets.technical_report_requests",
        string="Solicitud de Informe Tecnico",
        required=False,
    )

    technical_report_status = fields.Selection(
        [
            ('requested', 'Solicitado'),
            ('received', 'Recibido'),
        ],
        required=True,
        string="Estado de solicitud",
        default="requested"
    )

    pdf_file = fields.Binary(
        string='Archivo PDF',
        # required=True,
        attachment=True
    )
    pdf_name = fields.Char(
        string="Respuesta del informe técnico ",
        # required=True,
        help="Cargue el informe tecnico recibido del activo fijo"
    )

    conclusion = fields.Selection(
        [
            ('pending', 'pendiente'),
            ('to maintenance', 'requiere mantenimiento'),
            ('to unavailable', 'requiere dar de baja'),
        ],
        string="Conclusion del informe técnico",
        default="pending"
    )


    comments = fields.Text(
        string="Comentarios",
        required=True
    )

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


    def generate_report(self):
        """Genera el reporte según la selección del usuario."""
        if self.conclusion == 'pending':
            raise UserError("Debes seleccionar una conclusion antes de generarlo.")

        report_action = False
        if self.conclusion == 'to maintenance':
            report_action = self.action_to_maintenance()
        elif self.conclusion == 'to unavailable':
            report_action = self.action_to_unavailable()

        return report_action

    def action_to_unavailable(self):
        self.ensure_one()
        for record in self:
            if record.technical_report_status == 'requested' and record.conclusion == 'pending':
                raise ValidationError("Solo puedes dar de baja activos que tienen pendiente una respuesta tecnica.")

            if not record.asset_id:
                raise ValidationError("No hay un activo asociado a la solicitud")

            if record.asset_id.availability == 'available':
                raise ValidationError("El activo no se encuentra disponible en la unidad")

            record.write({
                'conclusion': 'to unavailable',
                'technical_report_status': 'received',
            })

            record.asset_id.write({
                'availability': 'unavailable',
            })

            report_action = (self.env
                             .ref('soe_fixed_assets.action_unavailable_report')
                             .report_action(self))

            return report_action

    def action_to_maintenance(self):
        self.ensure_one()
        for record in self:
            if record.technical_report_status == 'requested' and record.conclusion == 'pending':
                raise ValidationError("Solo puedes dar de baja activos que tienen pendiente una respuesta tecnica.")

            if record.asset_id.availability == 'available':
                raise ValidationError("El activo no se encuentra disponible en la unidad")

            if not record.asset_id:
                raise ValidationError("No hay un activo asociado a la solicitud")

            record.write({
                'conclusion': 'to maintenance',
                'technical_report_status': 'received',
            })
            record.asset_id.write({
                'availability': 'maintenance',
            })
            report_action = (self.env
                             .ref('soe_fixed_assets.action_maintenance_report')
                             .report_action(self))
            return report_action