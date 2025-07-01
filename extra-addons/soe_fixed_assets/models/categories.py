from odoo import models, fields, api

class Category(models.Model):
    _name = 'soe_fixed_assets.category'
    _description = 'soe_fixed_assets.category'

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Escriba el nombre de la categoria"
    )
    lifespan = fields.Integer(
        string="Años de vida util",
        required=True,
        help="Años de vida util del activo fijo"
    )
    coefficient = fields.Float(
        string="Coeficiente de depreciacion",
        decimal=2,
        required=True
    )
    group_id = fields.One2many(
        "soe_fixed_assets.group",
        'category_id',
        string="Grupo"
    )