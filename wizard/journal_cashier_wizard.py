# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

import logging

class JournalCashierWizard(models.Model):
    _name = 'journal.cashier.wizard'
    _description = 'journal cashier wizard'

    name = fields.Char(string='Nom')
    date = fields.Date(string='Date du journal')
    journal_reference = fields.Char(string='Référence du journal')
    initial_balance = fields.Float(string='Solde initial')
    final_balance = fields.Float(string='Solde final')
    journal_box_aggregate_ids = fields.One2many('journal.box.aggregate', 'journal_cashier_wizard_id', string='Lignes journal caisse')

    @api.multi
    def print_journal_cashier(self):
        """ print jouranl box """
        # self.ensure_one()
        return self.env.ref('index_expense_management.action_report_journal_cashier').report_action(self)