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
        ondelete='restrict',
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

    @api.depends('acquisition_id.nro_cite', 'asset_id.code')
    def _compute_name(self):
        for record in self:
            acta = record.acquisition_id.nro_cite or ''
            # Asegúrate que hay al menos un asset
            if record.asset_id:
                # Solo uno por diseño, usamos el primero
                asset_code = record.asset_id[0].code or ''
                record.name = f"{acta} - {asset_code}"
            else:
                record.name = acta