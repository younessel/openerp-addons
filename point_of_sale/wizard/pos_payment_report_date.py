# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv
from osv import fields
import time


class pos_payment_report_date(osv.osv_memory):
    '''
    Open ERP Model
    '''
    _name = 'pos.payment.report.date'
    _description = 'POS Payment Report according to date'
    def print_report(self, cr, uid, ids, context=None):

        """
             To get the date and print the report
             @param self: The object pointer.
             @param cr: A database cursor
             @param uid: ID of the user currently logged in
             @param context: A standard dictionary
             @return : retrun report
        """
        datas = {'ids': context.get('active_ids', [])}
        res = self.read(cr, uid, ids, ['date_start', 'date_end', 'user_id'])
        res = res and res[0] or {}
        datas['form'] = res

        return {
                'type': 'ir.actions.report.xml',
                'report_name': 'pos.payment.report.date',
                'datas': datas,
        }

    _columns = {
            'date_start': fields.date('Start Date', required=True),
            'date_end': fields.date('End Date', required=True),
            'user_id': fields.many2many('res.users', 'res_user_sale', 'user_id', 'sale_id', 'Salesman')
    }
    _defaults = {
            'date_start': lambda *a: time.strftime('%Y-%m-%d'),
            'date_end': lambda *a: time.strftime('%Y-%m-%d'),
    }

pos_payment_report_date()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

