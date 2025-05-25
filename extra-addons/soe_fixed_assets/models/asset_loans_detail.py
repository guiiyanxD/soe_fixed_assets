from odoo import models, fields, api
from odoo.exceptions import ValidationError



class AssetsLoanDetail(models.Model):
    _name = 'soe_fixed_assets.asset_loans_detail'
    _description = 'Detalle del prestamo del activo fijo'

    asset_name = fields.Char(
        related='asset_id.name',
        string='Nombre del Activo',
        readonly=True
    )
    comments = fields.Text(string="Comentarios")

    asset_id = fields.Many2one(
        "soe_fixed_assets.asset",
        string="Activo fijo",
        required=True,
        ondelete='restrict'
    )

    asset_loans_id = fields.Many2one(
        "soe_fixed_assets.asset_loans",
        string="Prestamo",
        required=True,
        ondelete="cascade"
    )



@api.constrains('asset_id')
def _check_asset_not_already_loaned(self):
    for rec in self:
        if not rec.asset_loans_id.loan_date_end:  # solo si el préstamo sigue activo
            domain = [
                ('asset_id', '=', rec.asset_id.id),
                ('id', '!=', rec.id),
                ('asset_loans_id.loan_date_end', '=', False)
            ]
            existing = self.search(domain, limit=1)
            if existing:
                raise ValidationError("Este activo ya está prestado y no ha sido devuelto.")
