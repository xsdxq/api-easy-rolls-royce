#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .apiVersionResource import apiversion_blueprint
from .BatchResource import batch_blueprint
from .adminResource import admin_blueprint
from .testInfoResource import testinfo_blueprint
from .weixinappResource import weixinapp_blueprint


def init_router(app):
    from api_1_0.apiVersionResource import apiversion_blueprint
    app.register_blueprint(apiversion_blueprint, url_prefix="/api_1_0")

    # Batch blueprint register
    from api_1_0.BatchResource import batch_blueprint
    app.register_blueprint(batch_blueprint, url_prefix="/api_1_0")
    
    # admin blueprint register
    from api_1_0.adminResource import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/api_1_0")
    
    # testInfo blueprint register
    from api_1_0.testInfoResource import testinfo_blueprint
    app.register_blueprint(testinfo_blueprint, url_prefix="/api_1_0")

    from api_1_0.weixinappResource import weixinapp_blueprint
    app.register_blueprint(weixinapp_blueprint, url_prefix="/api_1_0")

    from api_1_0.userTokenResource import usertoken_blueprint
    app.register_blueprint(usertoken_blueprint, url_prefix="/api_1_0")
