#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import testinfo_blueprint
from api_1_0.testInfoResource.testInfoResource import TestInfoResource
from api_1_0.testInfoResource.testInfoOtherResource import TestInfoOtherResource

api = Api(testinfo_blueprint)

api.add_resource(TestInfoResource, '/testInfo/<RecordID>', '/testInfo', endpoint='testInfo')


# get_excel
@testinfo_blueprint.route('/test/get_excel', methods=['GET'], endpoint='get_excel')
def Test_query():
    return TestInfoOtherResource.get_excel()


# joint query
@testinfo_blueprint.route('/test/query', methods=['GET'], endpoint='test_query')
def Test_query():
    return TestInfoOtherResource.joint_query()


# joint query
@testinfo_blueprint.route('/test/delete', methods=['POST'], endpoint='test_delete')
def Test_query():
    return TestInfoOtherResource.test_delete()


