from odoo import models, fields, api

class Subsidiary(models.Model):
    _name = 'soe_fixed_assets.subsidiary'
    _description = 'soe_fixed_assets.subsidiary'

    name = fields.Char(string="Nombre", required=True, help="Escriba el nombre de la medida")
    address = fields.Char(string="Direccion", required=True, help="Escriba la direccion")
    id_manager = fields.Char(string="Encargado", required=True, help="Nombre del encargado de la sucursal")
    area_id = fields.One2many("soe_fixed_assets.area", 'subsidiary_id', string="Area",)