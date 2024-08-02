# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from math import copysign


class PosConfig(models.Model):
    _inherit = 'pos.config'

    expense_management = fields.Boolean(string='Gestion des Dépenses')