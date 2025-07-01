from odoo import models, fields, api

class Group(models.Model):
    _name = 'soe_fixed_assets.group'
    _description = 'soe_fixed_assets.group'

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Escriba el nombre del grupo"
    )
    category_id = fields.Many2one(
        "soe_fixed_assets.category",
        string="Categoria",
        help="Seleccione la categoria a la que pertenece este grupo"
    )
    asset_id = fields.One2many(
        "soe_fixed_assets.asset",
        'group_id',
        string="Activo fijo"
    )