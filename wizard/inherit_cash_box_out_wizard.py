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
        active_model = self.env.context.get('active_model', False)
        active_ids = self.env.context.get('active_ids', [])

        if active_model == 'pos.session':
            values = {
                'date' : date.today(),
                'name' : self.name,
                'category_id' : self.category_id.id,
                'amount' : self.amount
            }
            active_sessions = self.env[active_model].browse(active_ids)
            logging.error('___________________active_sessions___{}__________'.format(active_sessions))
            if active_sessions:
                values['pos_session_id'] = active_sessions.id
            self.env['expense.journal'].create(values)
        return super(InheritCashBox, self).run()


