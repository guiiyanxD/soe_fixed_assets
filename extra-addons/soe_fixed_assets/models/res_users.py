from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    activos_role = fields.Selection(
        [('director', 'Director'),
         ('jefe_area', 'Jefe de Área'),
         ('operador', 'Operador')],
        string="Rol en Activos Fijos",
    )
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

    @api.onchange('activos_role')
    def _onchange_activos_role(self):
        group_director = self.env.ref('soe_fixed_assets.group_admin_activos')
        group_jefe = self.env.ref('soe_fixed_assets.group_manager_area')
        group_operador = self.env.ref('soe_fixed_assets.group_operator')

        # Limpiar grupos previos
        self.groups_id -= group_director | group_jefe | group_operador

        # Asignar grupo según selección
        if self.activos_role == 'director':
            self.groups_id += group_director
        elif self.activos_role == 'jefe_area':
            self.groups_id += group_jefe
        elif self.activos_role == 'operador':
            self.groups_id += group_operador

    class ResUsers(models.Model):
        _inherit = 'res.users'

        @api.model_create_multi
        def create(self, vals_list):
            # Eliminar 'base.group_user' de los valores iniciales si existe
            for vals in vals_list:
                if 'groups_id' in vals:
                    # Filtrar para excluir 'base.group_user'
                    group_user_id = self.env.ref('base.group_user').id
                    vals['groups_id'] = [
                        (4, group_id)
                        for group_id in vals['groups_id'][0][2]
                        if group_id != group_user_id
                    ]
            return super().create(vals_list)
