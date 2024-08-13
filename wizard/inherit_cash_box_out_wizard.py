from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.account.wizard.pos_box import CashBox
import logging
from datetime import date


class InheritCashBox(CashBox):
    _register = False

    category_id = fields.Many2one("expense.category")
    journal_id = fields.Many2one("account.journal", string="Journal")
    # journal_id = fields.Many2one("account.journal", string="Journal", domain="[('type', 'in', ('cash', 'bank'))]")

    @api.model
    def default_get(self, fields):
        res = super(InheritCashBox, self).default_get(fields)
        # Get the active POS session
        pos_session = self.env['pos.session'].browse(self.env.context.get('active_id'))
        # Get the journal_ids from the config_id
        if pos_session and pos_session.config_id:
            journals = pos_session.config_id.journal_ids
            if journals:
                res['journal_id'] = journals[0].id  # Set default journal if needed
        return res

    @api.onchange('journal_id')
    def _onchange_journal_id(self):
        if self.journal_id:
            # Set the domain dynamically based on the selected journal
            return {'domain': {'journal_id': [('id', 'in', self.env['pos.session'].browse(self.env.context.get('active_id')).config_id.journal_ids.ids)]}}

    @api.multi
    def run(self):
        active_model = self.env.context.get('active_model', False)
        active_ids = self.env.context.get('active_ids', [])

        if active_model == 'pos.session':
            if not self.journal_id:
                raise ValidationError(_("Le champ Journal ne doit pas être vide."))
            values = {
                'date' : date.today(),
                'name' : self.name,
                'category_id' : self.category_id.id,
                'amount' : self.amount,
                'journal_id' : self.journal_id.id
            }
            active_sessions = self.env[active_model].browse(active_ids)
            if active_sessions:
                values['pos_session_id'] = active_sessions.id
            self.env['expense.journal'].create(values)
        return super(InheritCashBox, self).run()


class CashBoxOut(InheritCashBox):
    _inherit = 'cash.box.out'

