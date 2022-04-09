#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
from utils.response_code import RET
from .datas import add_datas,get_datas,delete_datas,update_datas,addlist_datas
from controller.BatchController import BatchController


@pytest.mark.controller
def test_add():
    for data in add_datas:
        result = BatchController.add(**data)
        assert result['code'] == RET.OK


@pytest.mark.controller
def test_get():
    for data in get_datas:
        result = BatchController.get(**data)
        assert result['code'] == RET.OK


@pytest.mark.controller
def test_delete():
    for data in delete_datas:
        result = BatchController.delete(**data)
        assert result['code'] == RET.OK


@pytest.mark.controller
def test_update():
    for data in update_datas:
        result = BatchController.update(**data)
        assert result['code'] == RET.OK


@pytest.mark.controller
def test_addlist():
    for data in addlist_datas:
        result = BatchController.add_list(**data)
        assert result['code'] == RET.OK