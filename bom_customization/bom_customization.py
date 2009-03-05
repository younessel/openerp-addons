# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2009 Smile.fr. All Rights Reserved
#    authors: Raphaël Valyi, Xavier Fernandez
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
from osv import fields, osv

class bom_customization_groups(osv.osv):
    _name = "bom_customization.bom_customization_groups"
    
    _columns = {
                'name': fields.char('Group Name', size=64, select=1),
                'key_ids': fields.one2many("bom_customization.bom_customization_keys", 'group_id', "Keys"),
                'value_ids': fields.one2many("bom_customization.bom_customization_values", 'group_id', "Values"),
    }
bom_customization_groups()

class bom_customization_keys(osv.osv):
    _name = "bom_customization.bom_customization_keys"
    
    _columns = {
                'name': fields.char('Key Name', size=64, select=1),
                'group_id': fields.many2one('bom_customization.bom_customization_groups', "Customization Group", required = True),
    }
bom_customization_keys()

class bom_customization_values(osv.osv):
    _name = "bom_customization.bom_customization_values"
    
    _columns = {
                'name': fields.char('Value Name', size=64, select=1),
                'group_id': fields.many2one('bom_customization.bom_customization_groups', "Customization Group", required = True),
    }
bom_customization_values()


class bom_customization(osv.osv):
    _name = "bom_customization.bom_customizations"
    
    #TODO get rid of name
    _columns = {
                'name': fields.char('Useless Field', size=64),
                'bom_ids': fields.many2many('mrp.bom','mrp_bom_bom_customizations_rel','bom_id','bom_customization_id',"BoM's"),
                'customization_value_id': fields.many2one('bom_customization.bom_customization_values', 'Customization Value'),
                'customization_key_id': fields.many2one('bom_customization.bom_customization_keys', 'Customization Key'),
    }
bom_customization()
