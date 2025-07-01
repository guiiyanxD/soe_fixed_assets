from odoo import models, fields, api

class PhysicalStatus(models.Model):
    _name = 'soe_fixed_assets.physical_status'
    _description = 'soe_fixed_assets.physical_status'

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Escriba el nombre del estado fisico"
    )
    description = fields.Text(
        string="Descripcion",
        required=True,
        help="Describa el estado fisico"
    )
    # created_by = fields.Char(
    #     string="Creado por",
    #     required=True,
    #     help="El usuario que registro la calidad"
    # )
    asset_id = fields.One2many(
        "soe_fixed_assets.asset",
        'physical_status_id',
        string="Activo fijo"
    )


