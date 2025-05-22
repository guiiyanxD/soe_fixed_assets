# -*- coding: utf-8 -*-
# from odoo import http


# class SoeFixedAssets(http.Controller):
#     @http.route('/soe_fixed_assets/soe_fixed_assets', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/soe_fixed_assets/soe_fixed_assets/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('soe_fixed_assets.listing', {
#             'root': '/soe_fixed_assets/soe_fixed_assets',
#             'objects': http.request.env['soe_fixed_assets.soe_fixed_assets'].search([]),
#         })

#     @http.route('/soe_fixed_assets/soe_fixed_assets/objects/<model("soe_fixed_assets.soe_fixed_assets"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('soe_fixed_assets.object', {
#             'object': obj
#         })

