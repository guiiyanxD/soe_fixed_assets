from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.fields import One2many, Many2many, Many2one


class Asset(models.Model):
    _name = 'soe_fixed_assets.asset'
    _rec_name = 'code'
    _description = 'soe_fixed_assets.asset'

    code = fields.Char(
        string="Código",
        required=True,
        help="Escriba el código del activo fijo"
    )

    acquisition_detail_id = fields.Many2one(
        "soe_fixed_assets.acquisition_detail",
        string = "Detalle del Acta",
        ondelete='restrict',
    )

    area_id = fields.Many2one(
        "soe_fixed_assets.area",
        string="Area",
        help="Seleccione el area",
        required=True
    )

    group_id = fields.Many2one(
        "soe_fixed_assets.group",
        string="Grupo",
        help="Seleccione el grupo",
        required=True
    )

    measure_id = fields.Many2one(
        "soe_fixed_assets.measure",
        string="Medida",
        help="Seleccione la medida",
        required=True
    )

    physical_status_id = fields.Many2one(
        "soe_fixed_assets.physical_status",
        string="Estado Físico",
        help="Seleccione el estado físico",
        required=True
    )

    manager_id = fields.Char(
        string="Encargado",
        required=True,
        help="Seleccione el encargado del activo fijo"
    )

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Escriba el nombre del activo fijo"
    )

    description = fields.Char(
        string="Descripcion",
        required=True,
        help="Escriba la descripcion del activo fijo"
    )

    brand = fields.Char(
        string="Marca",
        required=True,
        help="Escriba la marca del activo fijo"
    )

    cost = fields.Float(
        string="Costo",
        required=True,
        help="Escriba el costo del activo fijo"
    )

    availability = fields.Selection(
        [
        ('available', 'Disponible'),
        ('loaned', 'Prestado'),
        ('unavailable', 'Baja'),
        ],
        required=True,
        string="Disponibilidad",
        default="available"
    )

    loan_detail_id = fields.One2many(
        'soe_fixed_assets.asset_loans_detail',
        'asset_id',
        string="Préstamo Asociado"
    )


    _sql_constraints = [
        ('unique_code', 'unique(code)', 'El Código del Activo Fijo debe ser único.'),
        ('unique_acquisition_detail', 'unique(acquisition_detail_id)', 'Este detalle ya está asignado a otro activo.'),
        ('unique_loan_detail', 'unique(loan_detail_id)', 'Este detalle de prestamo ya esta asignado a otro activo')
    ]

    def action_return_asset(self):
        self.ensure_one()
        asset_loan = self.loan_detail_id.filtered(
            lambda l: l.loan_detail_status == 'loaned'
        )
        asset_loan_expired = self.loan_detail_id.filtered(
            lambda l: l.loan_detail_status == 'expired'
        )
        if self.loan_status == 'unavailable' and (asset_loan or asset_loan_expired):
            self.write({'loan_status': 'available'})
            asset_loan.write({'loan_detail_status': 'returned'})
        else:
            raise ValidationError("Este activo no está prestado")

    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)

    def write(self, vals):
        """
        Sobrescribe el métod o write para evitar problemas de herencia y recursividad.
        """
        super().write(vals)
        return True

    def action_ver_acta(self):
        """
        Este mé todo abre la vista formulario del acta de recepción relacionada con el activo fijo.
        """
        self.ensure_one()  # Asegura que self es un solo registro
        if self.acquisition_detail_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Acta de Recepción',
                'view_mode': 'form',
                'res_model': 'soe_fixed_assets.acquisition',
                'res_id': self.acquisition_detail_id.acquisition_id.id,  # Abre el registro específico del acta
                'target': 'current',  # La vista se abre en la misma ventana
            }
        else:
            raise ValidationError("El activo no esta vinculado a ningun acta de recepcion.")