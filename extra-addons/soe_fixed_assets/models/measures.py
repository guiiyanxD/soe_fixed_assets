from odoo import models, fields, api

class Measure(models.Model):
    _name = 'soe_fixed_assets.measure'
    _description = 'soe_fixed_assets.measure'

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Escriba el nombre de la medida"
    )
    description = fields.Char(
        string="Descripcion",
        required=True,
        help="Escriba la descripcion de la medida"
    )
    abbreviation = fields.Char(
        string="Abreviacion",
        required=True,
        help="Escriba la abreviacion de la medida"
    )
    asset_id = fields.One2many(
        "soe_fixed_assets.asset",
        'measure_id',
        string="Activos fijos asociados"
    )
