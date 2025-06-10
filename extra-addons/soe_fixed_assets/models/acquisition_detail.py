from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class AcquisitionDetail(models.Model):
    _name = 'soe_fixed_assets.acquisition_detail'
    _description = 'Detail of Acquisition'

    name = fields.Char(string='Acquisition Name')

    asset_id = fields.Many2one(
        'soe_fixed_assets.asset',
        string='Activo Fijo',
        required=True,
        ondelete='restrict',
        help='Seleccione el activo fijo asociado a este detalle.',
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
    can_add_multiple_assets = fields.Boolean(
        compute="_compute_can_add_multiple_assets",
        store=False,
        string="Permitir Múltiples Activos",
    )

    _sql_constraints = [
        ('unique_asset_per_acquisition', 'unique(acquisition_id, code)',
         'Este activo ya está listado en este Acta de Recepción.'),
    ]

    @api.depends('acquisition_id.acquisition_type')
    def _compute_can_add_multiple_assets(self):
        for rec in self:
            # Si hay una adquisición vinculada y su tipo es 'reasignacion', entonces True
            rec.can_add_multiple_assets = False  # Valor por defecto
            if rec.acquisition_id and rec.acquisition_id.acquisition_type == 'reasignacion':
                rec.can_add_multiple_assets = True

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
                # 'default_name': self.acquisition_id.nro_cite,  # ← importante
            }

        }

