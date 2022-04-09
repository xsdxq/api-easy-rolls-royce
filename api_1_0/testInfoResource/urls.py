#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_restful import Api

from . import testinfo_blueprint
from api_1_0.testInfoResource.testInfoResource import TestInfoResource
from api_1_0.testInfoResource.testInfoOtherResource import TestInfoOtherResource

api = Api(testinfo_blueprint)

api.add_resource(TestInfoResource, '/testInfo/<RecordID>', '/testInfo', endpoint='testInfo')


# joint query
@testinfo_blueprint.route('/task/query', methods=['GET'], endpoint='task_query')
def Task_query():
    return TestInfoOtherResource.joint_query()


