from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AssetsLoan(models.Model):
    _name = 'soe_fixed_assets.asset_loans'
    _description = 'soe_fixed_assets.asset_loans'

    nro_cite = fields.Char(
        string="Nro Cite",
        required=True
    )

    loan_date = fields.Date(
        string="Fecha de prestamo",
        required=True,
        help="Fecha de prestamo del activo fijo"
    )

    return_date = fields.Date(
        string="Fecha de devolucion",
        help="Fecha de devolucion del activo fijo"
    )
    destiny = fields.Char(
        string="Destino del prestamo",
        required=True
    )

    manager = fields.Char(
        string="Persona que recibe",
        required=True
    )

    asset_loans_detail_ids = fields.One2many(
        "soe_fixed_assets.asset_loans_detail",
        "asset_loans_id",
        string="Detalles del prestamo",
        copy=True
    )

#    @api.model
#    def create(self, vals):
        # if vals.get('name', _('Nuevo')) == _('Nuevo'):
        #     vals['name'] = self.env['ir.sequence'].next_by_code('soe.fixed.assets.loan.sequence') or _(
        #         'Nuevo')

    @api.constrains('loan_date', 'return_date')
    def _check_return_date(self):
        for record in self:
            if record.return_date and record.loan_date and record.return_date <= record.loan_date:
                    raise UserError(_("⚠️ La fecha de devolución no puede ser anterior a la fecha de préstamo."))

    def print_asset_loan_report(self):
        self.ensure_one()
        return self.env.ref('soe_fixed_assets.action_report_asset_loan').report_action(self)
