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
        required=True,
        attachment=True
    )
    pdf_name = fields.Char(
        string="Respuesta del informe técnico ",
        required=True,
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

    def action_to_maintenance(self):
        self.ensure_one()
        for record in self:
            if (record.technical_report_status == 'requested' and record.conclusion == 'pending'):
                if (record.asset_id.availability == 'available'):
                    record.write({
                        'conclusion': 'to maintenance',
                        'technical_report_status': 'received',
                    })

                    if record.asset_id:
                        record.asset_id.write({
                            'availability': 'maintenance',
                        })
                    else:
                        raise ValidationError("El activo fijo no se encuentra Disponible.")
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': 'El activo ha sido enviado a mantenimiento correctamente.',
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                raise ValidationError("Solo puedes enviar a mantenimiento activos que tienen pendiente una respuesta tecnica.")
        return True

    def action_generate_specific_report(self):
        return True

    def action_to_unavailable(self):
        self.ensure_one()
        for record in self:
            #Que el detalle aun este solicitado, que la conclusion ste pendiente y que el activo se encuentre available
            if (record.technical_report_status == 'requested' and record.conclusion == 'pending'):
                if (record.asset_id.availability == 'available'):
                    record.write({
                        'conclusion': 'to unavailable',
                        'technical_report_status': 'received',
                    })

                    if record.asset_id:
                        record.asset_id.write({
                            'availability': 'unavailable',
                        })
                else:
                    raise ValidationError("El activo fijo no se encuentra Disponible.")

                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': 'El activo ha sido dado de baja correctamente.',
                        'type': 'success',
                        'sticky': True,
                    }
                }
            else:
                raise ValidationError("Solo puedes dar de baja activos que tienen pendiente una respuesta tecnica.")
        return True