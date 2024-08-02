# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class ExpenseDetailWizard(models.Model):
    _name = 'expense.detail.wizard'

    expense_journal_lines_ids = fields.One2many('expense.journal', 'expense_journal_id', string='Lignes journal dépenses')