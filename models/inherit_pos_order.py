# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from math import copysign
import logging


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create(self, values):
        if 'session_id' in values:
            pos_order_id = self.env['pos.order'].search([('session_id', '=', values.get('session_id'))])
            pos_order_id_lines_ids = []
            if pos_order_id:
                for order in pos_order_id:
                    values_dict = {
                        'name' : order.name,
                        'date' : order.date_order,
                        'amount' : order.amount_total,
                    }
                    pos_order_id_lines_ids.append((values_dict))
            if pos_order_id_lines_ids:
                total_order = sum(elem['amount'] for elem in pos_order_id_lines_ids)
                pos_session_id = self.env['pos.session'].search([('id', '=', values.get('session_id'))])
                pos_session_id.write({'total_input' : total_order})
        return super(PosOrder, self).create(values)