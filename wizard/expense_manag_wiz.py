# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class ExpenseManagementWizard(models.TransientModel):
    _name = 'expense.management.wizard'

    date = fields.Date("Date", required=True, default=date.today())
    name = fields.Char("Name", required=True)
    category_id = fields.Many2one("expense.category", required=True)
    partner_id = fields.Many2one("res.partner", "Partenaire", required=False)
    payment_journal_id = fields.Many2one('account.journal', string='Journal',
                                         domain=[('type', 'in', ('bank', 'cash'))], required=True)
    amount = fields.Float("Montant", required=True)

    bank_statement_id = fields.Many2one("account.bank.statement", string="Relevé", required=False)

    def create_expense(self):
        """Create new expense"""
        expense_obj = self.env['expense.management']
        val_expense = {
            "date": self.date,
            "name": self.name,
            "category_id": self.category_id.id,
            "partner_id": self.partner_id.id,
            "payment_journal_id": self.payment_journal_id.id,
            "amount": self.amount,
            "bank_statement_id": self.bank_statement_id.id
        }
        expense_obj.create(val_expense)

