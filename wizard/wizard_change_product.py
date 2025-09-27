# -*- coding:utf-8 -*-
from  odoo import  models, fields , api

class WizardChange(models.TransientModel):
    _name = "wizard.change.product"


    order_id = fields.Many2one("sale.order",string="Pedido de venta")

    line_ids = fields.One2many("wizard.change.lines",
                               "wizard_product_id"
                               ,string="Lineas de la orden")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if active_id:
            res['order_id'] = active_id
            order = self.env['sale.order'].browse(active_id)

            lineas = []
            for linea in order.order_line:
                if linea.product_id.type == 'consu':  
                    lineas.append((0, 0, {
                        "product_id": linea.product_id.id,
                        "product_uom_qty": linea.product_uom_qty,
                        "price_unit": linea.price_unit,
                    }))
            res['line_ids'] = lineas
        return res


    def change_lines(self, order):
        for wizard_line in self.line_ids:
            producto_final = wizard_line.product_change_id or wizard_line.product_id
            self.env["sale.order.line"].create({
                "order_id": order,
                "product_id": producto_final.id,
                "product_uom_qty": wizard_line.product_uom_qty,
                "price_unit": wizard_line.price_unit,
                "name": producto_final.name,
            })

    def action_confirmar(self):
        self.ensure_one()
        order = self.order_id

        if order.state != "draft":
            if order.state != "cancel":
                order._action_cancel()
                order.action_draft()

        for wizard_line in self.line_ids.filtered(lambda l: l.product_change_id):
            lineas_a_reemplazar = order.order_line.filtered(
                lambda l: l.product_id.id == wizard_line.product_id.id
            )

            lineas_a_reemplazar.unlink()

            producto_final = wizard_line.product_change_id
            descripcion = producto_final.get_product_multiline_description_sale() or producto_final.display_name

            self.env["sale.order.line"].create({
                "order_id": order.id,
                "product_id": producto_final.id,
                "product_uom_qty": wizard_line.product_uom_qty,
                "price_unit": wizard_line.price_unit,
                "name": descripcion,
            })

        if order.state == 'draft':
            order.action_confirm()



class WizardChangeLines(models.TransientModel):
    _name = "wizard.change.lines"
    _description = "Líneas con posibilidad de cambio"

    wizard_product_id = fields.Many2one("wizard.change.product", string="Wizard")
    product_id = fields.Many2one("product.product", string="Producto original")
    product_change_id = fields.Many2one("product.product", string="Producto nuevo (opcional)")
    product_uom_qty = fields.Float("Cantidad")
    price_unit = fields.Float("Precio unitario")

