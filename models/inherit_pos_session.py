# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from math import copysign
import logging


class PosSession(models.Model):
    _inherit = 'pos.session'

    config_id = fields.Many2one('pos.config', string='POS Config')
    expense_management = fields.Boolean(compute='_compute_expense', string='Gestion des dépenses')

    @api.depends('config_id')
    def _compute_expense(self):
        for session in self:
            session.expense_management = False
            if session.config_id.expense_management:
                session.expense_management = True

    def get_all_expenses(self):
        expense_journal_id = self.env['expense.journal'].search([('pos_session_id', '=', self.id)])
        expense_journal_lines_ids = []
        if expense_journal_id:
            for journal in expense_journal_id:
                values_dict = {
                    'name' : journal.name,
                    'date' : journal.date,
                    'amount' : journal.amount,
                    'category_id' : journal.category_id.id,
                    'pos_session_id' : journal.pos_session_id.id,
                }
                expense_journal_lines_ids.append((0, 0, values_dict))
        context = {
            'default_expense_journal_lines_ids' : expense_journal_lines_ids
        }
        return {
            'name': _('Détail de dépenses'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'expense.detail.wizard',
            'view_id': self.env.ref('index_expense_management.view_expense_detail_wizard_form').id,
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new'
        }
        # pass

    @api.multi
    def save_expense(self):
        context = dict(self._context)
        return {
            'name': _('Dépense'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'expense.management.wizard',
            'view_id': self.env.ref('index_expense_management.view_expense_management_wiz_form').id,
            'type': 'ir.actions.act_window',
            # 'context': context,
            'target': 'new'
        }