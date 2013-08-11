#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from peacock.model import ModelBase


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)


class Image(ModelBase, TimestampMixin):

    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    relative_path = Column(String(252), unique=True)
    content_type = Column(String(32))
