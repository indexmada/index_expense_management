# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class ExpenseCategory(models.Model):
    _name = "expense.category"

    name = fields.Char("Nom", required=True)


class ExpenseManagement(models.Model):
    _name = 'expense.management'
    _description = "Expense management"

    date = fields.Date("Date", required=True, default=date.today())
    name = fields.Char("Libellé", required=True)
    category_id = fields.Many2one("expense.category", required=True)
    partner_id = fields.Many2one("res.partner", "Partenaire", required=False)
    payment_journal_id = fields.Many2one('account.journal', string='Journal',
                                         domain=[('type', 'in', ('bank', 'cash'))], required=True)
    amount = fields.Float("Montant", required=True)

    bank_statement_id = fields.Many2one("account.bank.statement", string="Relevé", required=False)
