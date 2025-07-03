from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import date


class AssetsLoanDetail(models.Model):
    _name = 'soe_fixed_assets.asset_loans_detail'
    _description = 'Detalle del prestamo del activo fijo'

    comments = fields.Text(string="Comentarios")

    asset_code = fields.Char(
        related='asset_id.code',
        string='Codigo',
        readonly=True
    )

    asset_name = fields.Char(
        related='asset_id.name',
        string='Nombre',
        readonly=True
    )

    asset_brand = fields.Char(
        related='asset_id.brand',
        string='Marca',
        readonly=True
    )
    asset_description = fields.Char(
        related='asset_id.description',
        string='Descripcion',
        readonly=True
    )
    asset_physical_status = fields.Char(
        related='asset_id.physical_status_id.name',
        string='Calidad',
        readonly=True
    )

    asset_id = fields.Many2one(
        "soe_fixed_assets.asset",
        string="Activo fijo",
        required=True,
        ondelete='restrict',
        domain="[('availability', '=', 'available')]"
    )

    asset_loans_id = fields.Many2one(
        "soe_fixed_assets.asset_loans",
        string="Activos fijos en calidad de préstamo",
        ondelete="cascade"
    )

    loan_detail_status = fields.Selection(
        [
            ('loaned', 'Prestado'),
            ('returned', 'Devuelto'),
            ('expired', 'Préstamo Expirado')
        ],
        string="Estado del préstamo",
        default="loaned"
    )

    _sql_constraints = [
        ('asset_unique_per_loan', 'UNIQUE(asset_id, id, asset_loan_id)', '¡Este activo fijo ya existe en este préstamo!'),
    ]

    @api.onchange('asset_id')
    def _onchange_asset_id(self):
        if self.asset_id == 'available':
            self.asset_id.availability = 'loaned'
        elif self.asset_id == 'loaned':
            self.asset_id.availability = 'available'
        else:
            raise ValidationError("El activo fijo no esta prestado")

    @api.model
    def create(self, vals):
        record = super(AssetsLoanDetail, self).create(vals)
        if record.asset_id:
            record.asset_id.write({'availability': 'loaned'})
        return record

    def unlink(self):
        for rec in self:
            if rec.loan_detail_status == 'expired':
                raise UserError("No puedes eliminar activos de un préstamo vencido.")
            rec.asset_id.availability = 'available'
        return super(AssetsLoanDetail, self).unlink()

    @api.constrains('asset_id')
    def _check_asset_not_already_loaned(self):
        for rec in self:
            if not rec.asset_loans_id.return_date:  # solo si el préstamo sigue activo
                domain = [
                    ('asset_id', '=', rec.asset_id.id),
                    ('id', '!=', rec.id),
                    ('asset_loans_id.return_date', '=', False)
                ]
                existing = self.search(domain, limit=1)
                if existing:
                    raise ValidationError("Este activo ya está prestado y no ha sido devuelto.")

    def _check_expired_loans(self):
        hoy = date.today()
        prestamos_vencidos = self.search([
            ('loan_detail_status', '=', 'loaned'),
            ('asset_loans_id.return_date', '<', hoy)
        ])
        prestamos_vencidos.write({'loan_detail_status': 'expired'})
