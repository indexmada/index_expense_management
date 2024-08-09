# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class JournalBoxAggregate(models.Model):
    _name = 'journal.box.aggregate'

    date = fields.Date(string='Date')
    label = fields.Char(string='Libellé')
    partner = fields.Char(string='Partnenaire')
    reference = fields.Char(string='Référence')
    input = fields.Float(string='Entrée')
    output = fields.Float(string='Sortie')
    balance = fields.Float(string='Solde')
    journal_cashier_wizard_id = fields.Many2one('journal.cashier.wizard', string='Journal caisse')


class ExpenseJournal(models.Model):
    _name = "expense.journal"

    name = fields.Char("Libellé")
    date = fields.Date("Date")
    amount = fields.Float("Montant")
    category_id = fields.Many2one("expense.category", string='Catégorie')
    pos_session_id = fields.Many2one("pos.session", string='Session')
    expense_journal_id = fields.Many2one('expense.detail.wizard', string="Journal")

    @api.model
    def create(self, vals):
        expense = super(ExpenseJournal, self).create(vals)
        if 'pos_session_id' in vals:
            expense_journal_id = self.env['expense.journal'].search([('pos_session_id', '=', vals.get('pos_session_id'))])
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
                    expense_journal_lines_ids.append((values_dict))
            if expense_journal_lines_ids:
                total_expenses = sum(elem['amount'] for elem in expense_journal_lines_ids)
                pos_session_id = self.env['pos.session'].search([('id', '=', vals.get('pos_session_id'))])
                pos_session_id.write({'total_journal_expenses' : total_expenses})
        return expense


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
