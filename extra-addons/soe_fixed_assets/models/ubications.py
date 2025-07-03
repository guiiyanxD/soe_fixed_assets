from odoo import models, fields, api

class Ubications(models.Model):
    _name = 'soe_fixed_assets.ubications'
    _description = 'soe_fixed_assets.ubications'

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Escriba el nombre de la medida"
    )

    address = fields.Char(
        string="Dirección",
        required=True,
        help="Escriba la dirección"
    )

    manager_id = fields.Many2one(
        'res.users',
        string="Encargado",
        required=True,
        help="Seleccione el encargado de la sucursal"
    )

    area_id = fields.One2many(
        "soe_fixed_assets.area",
        'ubication_id',
        string="Area"
    )
