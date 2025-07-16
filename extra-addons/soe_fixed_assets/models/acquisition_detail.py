from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class AcquisitionDetail(models.Model):
    _name = 'soe_fixed_assets.acquisition_detail'
    _description = 'Detail of Acquisition'

    name = fields.Char(string="Nombre Detalle", compute="_compute_name", store=True)

    asset_id = fields.One2many(
        "soe_fixed_assets.asset",
        "acquisition_detail_id",
        string="Activo Fijo asociado",
        help='Seleccione el activo fijo asociado a este detalle.',
        required=True,
    )

    acquisition_id = fields.Many2one(
        "soe_fixed_assets.acquisition",
        string="Acta de Recepcion",
        required=True,
        ondelete='cascade',
    )
    comments = fields.Char(
        string="Comentarios",
    )

    _sql_constraints = [
        ('unique_asset_per_acq', 'unique(acquisition_id, id)',
         'Este detalle ya está listado en este Acta de Recepción.'),
    ]


    def open_acquisition_modal(self):
        if self.acquisition_id:
            raise UserError("Ya existe un documento de alta relacionado a este detalle.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Nuevo Documento de Alta',
            'res_model': 'soe_fixed_assets.acquisition',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_acquisition_detail_id': self.id,
            }

        }

    @api.depends('acquisition_id.nro_cite', 'asset_id.code')
    def _compute_name(self):
        for record in self:
            acta = record.acquisition_id.nro_cite or ''

            if record.asset_id:

                asset_code = record.asset_id[0].code or ''
                record.name = f"{acta} - {asset_code}"
            else:
                record.name = acta