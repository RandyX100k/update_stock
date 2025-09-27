# -*- coding:utf-8 -*-
from  odoo import  models , fields

class SaleCustom(models.Model):
    _inherit = "sale.order"

    def open_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Cambiar Producto",
            "res_model": "wizard.change.product",
            "view_mode": "form",
            "target": "new",
            "context": {
                'active_id': self.id,
                'active_model': 'sale.order',
            },
        }
