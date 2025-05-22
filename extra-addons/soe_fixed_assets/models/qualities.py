from odoo import models, fields, api

class Quality(models.Model):
    _name = 'soe_fixed_assets.quality'
    _description = 'soe_fixed_assets.quality'

    name = fields.Char(string="Nombre",required=True, help="Escriba el nombre de la calidad")
    description = fields.Text(string="Descripcion", required=True, help="Describa el nivel de calidad")
    created_by = fields.Char(string="Creado por", required=True, help="El usuario que registro la calidad")
    asset_id = fields.One2many("soe_fixed_assets.asset", 'quality_id', string="Activo fijo",)

#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

