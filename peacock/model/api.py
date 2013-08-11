#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from peacock.model.image import Image
from peacock.model import get_session
from sqlalchemy.orm import exc as sql_exc
from peacock import exception
import logging

logger = logging.getLogger(__name__)


def create_image(**kwargs):
    session = get_session()
    image = Image(**kwargs)
    session.add(image)
    session.flush()
    logger.debug('image.id = %s' % image.id)
    return image.id


def get_image_by_id(image_id):
    session = get_session()
    query = session.query(Image).filter_by(id=image_id)
    try:
        return query.one()
    except sql_exc.NoResultFound:
        raise exception.ImageNotFound(reference=image_id)


def get_image_by_relative_path(relative_path):
    session = get_session()
    query = session.query(Image).filter_by(relative_path=relative_path)
    try:
        return query.one()
    except sql_exc.NoResultFound:
        raise exception.ImageNotFound(reference=relative_path)

def get_image_list(start, stop):
    session = get_session()
    query = session.query(Image).order_by(Image.created_at.desc())
    return query.slice(start, stop).all()


def delete_image_by_relative_path(relative_path):
    session = get_session()
    query = session.query(Image).filter_by(relative_path=relative_path)
    try:
        session.delete(query.one())
    except sql_exc.NoResultFound:
        raise exception.ImageNotFound(reference=relative_path)
