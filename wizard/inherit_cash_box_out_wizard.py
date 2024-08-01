from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.addons.account.wizard.pos_box import CashBox
import logging
from datetime import date


class InheritCashBox(CashBox):
    _register = False

    category_id = fields.Many2one("expense.category", required=True)

    @api.multi
    def run(self):
        self.env['expense.journal'].create({
            'date' : date.today(),
            'name' : self.name,
            'amount' : self.amount
        })
        return super(InheritCashBox, self).run()


class CashBoxOut(InheritCashBox):
    _inherit = 'cash.box.out'

