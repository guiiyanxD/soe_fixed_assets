from odoo import models, fields, api

class Area(models.Model):
    _name = 'soe_fixed_assets.area'
    _description = 'soe_fixed_assets.area'


    name = fields.Char(
        string="Nombre",
        required=True,
        help="Escriba el nombre del area"
    )
    description = fields.Char(
        string="Descripcion",
        required=True,
        help="Escriba la descripción del area"
    )
    ubication_id = fields.Many2one(
        "soe_fixed_assets.ubications",
        string="Ubicación",
        help="Seleccione la sucursal",
        required=True)

    manager_id = fields.Char(
        string="Encargado",
        required=True,
        help="Seleccione el encargado del area"
    )
    asset_id = fields.One2many(
        "soe_fixed_assets.asset",
        'area_id',
        string="Activos fijos asociados"
    )

