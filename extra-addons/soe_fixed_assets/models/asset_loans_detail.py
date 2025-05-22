from odoo import models, fields, api



class AssetsLoanDetail(models.Model):
    _name = 'soe_fixed_assets.asset_loans_detail'
    _description = 'soe_fixed_asset.asset_loans_detail'

    asset_name = fields.Char(related='asset_id.name', string='Nombre del Activo', readonly=True)
    comments = fields.Text(string="Comentarios")

    asset_id = fields.Many2one(
        "soe_fixed_assets.asset",
        string="Activo fijo",
        required=True,
        ondelete='restrict')

    asset_loans_id = fields.Many2one(
        "soe_fixed_assets.asset_loans",
        string="Prestamo",
        required=True,
        ondelete="cascade")


