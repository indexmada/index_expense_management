# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from math import copysign
import logging


class PosSession(models.Model):
    _inherit = 'pos.session'

    config_id = fields.Many2one('pos.config', string='POS Config')
    expense_management = fields.Boolean(compute='_compute_expense', string='Gestion des dépenses')
    total_input = fields.Monetary(
        string='Total entrée',
        currency_field='currency_id',
        readonly=True,
        default=lambda self: self._get_total_input_value(),
        help="Total de toutes les entrées")
    total_journal_expenses = fields.Monetary(
        string='Total dépenses',
        currency_field='currency_id',
        readonly=True,
        default=lambda self: self._get_total_expense_value(),
        help="Total de toutes les dépenses")
    currency_id = fields.Many2one('res.currency', related='config_id.currency_id', string="Currency", readonly=False)

    def _get_total_input_value(self):
        pos_order_id = self.env['pos.order'].search([('session_id', '=', self.id)])
        pos_order_id_lines_ids = []
        total_expenses = 0
        if pos_order_id:
            for order in pos_order_id:
                values_dict = {
                    'name' : order.name,
                    'date' : order.date_order,
                    'amount' : order.amount_total,
                }
                pos_order_id_lines_ids.append((values_dict))
        if pos_order_id_lines_ids:
            total_expenses = sum(elem['amount'] for elem in pos_order_id_lines_ids)
        return total_expenses

    def _get_total_expense_value(self):
        expense_journal_id = self.env['expense.journal'].search([('pos_session_id', '=', self.id)])
        expense_journal_lines_ids = []
        total_expenses = 0
        if expense_journal_id:
            for journal in expense_journal_id:
                values_dict = {
                    'name' : journal.name,
                    'date' : journal.date,
                    'amount' : journal.amount,
                    'category_id' : journal.category_id.id,
                    'pos_session_id' : journal.pos_session_id.id,
                }
                expense_journal_lines_ids.append((values_dict))
        if expense_journal_lines_ids:
            total_expenses = sum(elem['amount'] for elem in expense_journal_lines_ids)
        return total_expenses

    @api.multi
    def action_report_journal_cashier_button(self):
        # here the body
        pass

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