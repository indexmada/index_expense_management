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
    
    @api.model
    def call_action_journal_caisse(self):
        dict_context = dict(self._context)
        active_model_pos_session = self.env['pos.session'].search([('id', '=', dict_context['active_id'])])
        statement_lines = active_model_pos_session.statement_ids
        journal_list = []
        journal_dict_list = []
        for state in statement_lines:
            for line in state.line_ids:
                dict_line = {
                    'date' : line.date,
                    'label' : line.name,
                    'partner_name' : line.partner_id.name,
                    'ref' : line.ref,
                    'amount' : line.amount,
                }
                final_dict = {
                    'date' : dict_line['date'],
                    'label' : dict_line['label'],
                    'partner' : dict_line['partner_name'],
                    'reference'  : dict_line['ref'],
                    'input' : 0.0,
                    'output' : 0.0,
                    'balance' : 0.0
                }
                if dict_line['amount'] < 0:
                    final_dict['output'] = dict_line['amount'] * (-1)
                elif dict_line['amount'] > 0:
                    final_dict['input'] = dict_line['amount']
                journal_dict_list.append(final_dict)
                # journal_list.append((0, 0, final_dict))
        dict_values = {
            'name' : 'name_{}'.format(active_model_pos_session.cash_register_id.name),
            'date' : fields.Date.today(),
            'journal_reference' : active_model_pos_session.cash_register_id.name,
            'initial_balance' : active_model_pos_session.cash_register_balance_start,
            # 'final_balance' : active_model_pos_session.cash_register_balance_end_real,
            # 'journal_box_aggregate_ids' : journal_list
        }
        if journal_dict_list:
            journal_dict_list[0]['balance'] = active_model_pos_session.cash_register_balance_start + journal_dict_list[0]['input'] - journal_dict_list[0]['output']
            for i in range(1, len(journal_dict_list)):
                previous_elem = journal_dict_list[i - 1]
                journal_dict_list[i]['balance'] = previous_elem['balance'] + journal_dict_list[i]['input'] - journal_dict_list[i]['output']
            for journal in journal_dict_list:
                journal_list.append((0, 0, journal))
            dict_values['final_balance'] = journal_dict_list[-1]['balance']
            dict_values['journal_box_aggregate_ids'] = journal_list

        wizard = self.env['journal.cashier.wizard'].create(dict_values)
        context = {}
        return {
            'name': 'Journal caisses',
            # 'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'journal.cashier.wizard',
            'res_id': wizard.id,
            # 'view_id': self.env.ref('index_expense_management.view_journal_cashier_wizard_form').id,
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new'
        }