#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import admin_blueprint
from api_1_0.adminResource.adminResource import AdminResource
from api_1_0.adminResource.adminOtherResource import AdminOtherResource

api = Api(admin_blueprint)

api.add_resource(AdminResource, '/admin/<AutoID>', '/admin', endpoint='admin')


# 管理员登录
@admin_blueprint.route('/admin/login', methods=['POST'], endpoint="adminLogin")
def admin_login():
    return AdminOtherResource.admin_login()

@admin_blueprint.route('/admin/reset', methods=['POST'], endpoint="adminreset")
def admin_reset():
    return AdminOtherResource.admin_reset()
