##############################################################################
#
# Copyright (c) 2004-2006 TINY SPRL. (http://tiny.be) All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import fields, osv

class portal_factory(osv.osv):
	"""
	Object associating a model to several restricted views (at least
	one tree or one form), to a menuotem and to a access rule.
	
	The resulting table will contain all the available models for a
	portal. When a user want to add a menu item in the portal an
	'activate' button enable the model with his setup : menu, view and
	access (Some combinaison way not be meaningful).

	- restricted views because we don't want the customer to see all
      the details.
	
	- the access controls will prevent the user from editing stuff and
      the ir_rules will prevent them to see data of other customers.
	"""
	
	_name = "portal.factory"
	_description = "Portal Factory"
	_columns = {
		'name': fields.char('Name',size=64, required=True,states={'enabled':[('readonly',True)]}),
		'model_id': fields.many2one('ir.model','Model',required=True,states={'enabled':[('readonly',True)]}),
		'view_id': fields.many2one('ir.ui.view','View',states={'enabled':[('readonly',True)]}),
		#'rule_id': fields.many2one('ir.rule','Rule', help="Rule use to restrict acces to the associated document.", required=True),
		'menu_name': fields.char('Menu Name',size=64, required=True,states={'enabled':[('readonly',True)]}),
		'parentmenu_id': fields.many2one('ir.ui.menu','Parent Menu',states={'enabled':[('readonly',True)]}, required=True),
		'template_action_id': fields.many2one('ir.actions.act_window','Action',states={'enabled':[('readonly',True)]}, required=True),
		'state': fields.selection([('enabled','Enabled'),('disabled','Disabled')],'State', readonly=True),
		'created_menu_id': fields.many2one('ir.ui.menu','Created Menu', readonly=True),
		'created_action_id': fields.many2one('ir.actions.act_window','Action',states={'enabled':[('readonly',True)]}),
		'created_value_id': fields.many2one('ir.values','Value',states={'enabled':[('readonly',True)]}),
	}

	_defaults={
		'state': lambda *a: 'disabled',
		}

	def enable(self,cr,uid,ids,context):
		factories= self.pool.get('portal.factory').browse(cr,uid,ids)
		for f in factories:
			m_id = self.pool.get('ir.model').search(cr,uid,[('model','=',f.template_action_id.res_model)])
			if f.model_id.id not in m_id:
				raise osv.except_osv('Error','Model type mismatch: The choosen action and model are not compatible.')

			menu_id=self.pool.get('ir.ui.menu').create(cr, uid, {
				'name': f.menu_name,
				'parent_id': f.parentmenu_id.id,
				'icon': 'STOCK_NEW'
				})
			
			action_id = self.pool.get('ir.actions.act_window').create(cr,uid, {
				'name': f.template_action_id.name,
				'res_model': f.model_id.model,
				'domain': f.template_action_id.domain,
				'view_type': 'form',
				'view_mode': f.template_action_id.view_mode,
				'view_id': f.view_id.id,
				})
			print {
				'name': f.template_action_id.name,
				'res_model': f.model_id.model,
				'domain': f.template_action_id.domain,
				'view_type': 'form',
				'view_mode': f.template_action_id.view_mode,
				'view_id': f.view_id.id,
				}
			value_id = self.pool.get('ir.values').create(cr, uid, {
				'name': 'TEST',
				'key2': 'tree_but_open',
				'model': 'ir.ui.menu',
				'res_id': menu_id,
				'value': 'ir.actions.act_window,%d'%action_id,
				'object': True
				})
			print {
				'name': 'TEST',
				'key2': 'tree_but_open',
				'model': 'ir.ui.menu',
				'res_id': menu_id,
				'value': 'ir.actions.act_window,%d'%action_id,
				'object': True
				}

			#TODO : create rules and access
		return self.write(cr,uid,ids,{'state':'enabled',"created_menu_id": menu_id,"created_action_id": action_id,"created_value_id": value_id})

	def disable(self,cr,uid,ids,context):
		factories= self.pool.get('portal.factory').browse(cr,uid,ids)
		for f in factories:
			self.pool.get('ir.ui.menu').unlink(cr,uid,[f.created_menu_id])
			self.pool.get('ir.actions.act_window').unlink(cr,uid,[f.created_action_id])
			self.pool.get('ir.values').unlink(cr,uid,[f.created_value_id])
		return self.write(cr,uid,ids,{'state':'disabled',})
		
portal_factory()
