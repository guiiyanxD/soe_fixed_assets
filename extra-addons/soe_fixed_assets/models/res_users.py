from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'
    _rec = 'card_number'

    card_number = fields.Char(
        string="Carne Identidad",
        required=True,
    )
    asset_ids = fields.One2many(
        'soe_fixed_assets.asset',
        'manager_id',
        string='Activos asignados'
    )
    area_id = fields.One2many(
        'soe_fixed_assets.area',
        'manager_id',
        string='Area asignada',
        required=True
    )
    ubication_id = fields.One2many(
        'soe_fixed_assets.ubication',
        'manager_id',
        string='Ubicacion asignada',
    )

    _sql_constraints = [
        ('unique_card_number', 'unique(card_number)', 'El numero de CI debe ser unico.'),

    ]