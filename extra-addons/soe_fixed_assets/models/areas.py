from odoo import models, fields, api

class Area(models.Model):
    _name = 'soe_fixed_assets.area'
    _description = 'soe_fixed_assets.area'

    # example = fields.Char(required=True),
    name = fields.Char(string="Nombre", required=True, help="Escriba el nombre del area")
    description = fields.Char(string="Descripcion", required=True, help="Escriba la descripcion del area")
    subsidiary_id = fields.Many2one("soe_fixed_assets.subsidiary", string="Sucursal",
        help="Seleccione la sucursal", required=True)
    manager_id = fields.Char(string="Encargado", required=True, help="Seleccione el encargado del area")

    asset_id = fields.One2many("soe_fixed_assets.asset", 'area_id', string="Activo fijo",)

