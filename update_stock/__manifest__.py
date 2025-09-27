# -*- coding: utf-8 -*-
{
    "name": "Update Stock",
    "version": "1.0",
    "summary": "Módulo para actualizar stock",
    "description": (
        "Este módulo permite gestionar y actualizar el stock de productos "
        "de forma sencilla dentro de Odoo."
    ),
    "author": "RUTIVERSOTECH",
    "website": "",
    "category": "Inventory/Stock",
    "depends": ["stock","sale_management"],
    "data": [
        "views/list_form.xml",
        "views/menu.xml",
        "views/sale_custom.xml",
        "wizard/view_wizard_product.xml",
        "security/ir.model.access.csv",
        "data/data.xml"
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
