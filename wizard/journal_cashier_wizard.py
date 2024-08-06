# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class JournalCashierWizard(models.TransientModel):
    _name = 'journal.cashier.wizard'
    _description = 'journal cashier wizard'

    x_field = fields.Char(string='Xxx')