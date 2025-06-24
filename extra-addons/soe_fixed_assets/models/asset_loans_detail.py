from odoo import models, fields, api
from odoo.exceptions import ValidationError


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
    asset_quality = fields.Char(
        related='asset_id.quality_id.name',
        string='Calidad',
        readonly=True
    )

    asset_id = fields.Many2one(
        "soe_fixed_assets.asset",
        string="Activo fijo",
        required=True,
        ondelete='restrict',
        domain="[('loan_status', '=', 'available')]"
    )

    asset_loans_id = fields.Many2one(
        "soe_fixed_assets.asset_loans",
        string="Prestamo",
        ondelete="cascade"
    )

    loan_detail_status = fields.Selection(
        [
            ('loaned', 'Prestado'),
            ('returned', 'Devuelto'),
            ('expired', 'Expirado')
        ],
        string="Estado del prestamo",
        default="loaned"
    )

    _sql_constraints = [
        ('asset_unique', 'UNIQUE(asset_id)', '¡Este activo ya está prestado!'),
    ]

    @api.onchange('asset_id')
    def _onchange_asset_id(self):
        if self.asset_id:
            self.asset_id.loan_status = 'unavailable'

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

    # @api.depends('asset_id.quality_id.name')
    # def _compute_campo_relacionado(self):
    #     for record in self:
    #         record.asset_id = record.modelo_b_id.campo_b or "Sin valor"