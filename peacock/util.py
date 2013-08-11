#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from pecan import conf
from os.path import join as path_join
from os.path import exists
from os.path import dirname
from os.path import splitext
from os import makedirs
import hashlib
import logging
import Image

logger = logging.getLogger(__name__)


def generate_image_path(content, extname):
    hexdigest = hashlib.md5(content).hexdigest()
    parent_path = path_join("user",
                            "images",
                            hexdigest[:2],
                            hexdigest[2:4])
    return "%s.%s" % (path_join(parent_path, hexdigest), extname)


def generate_thumbnail_path(image_path):
    path, unused = splitext(image_path)
    thumbnail_path = "%s_thumbnail.jpg" % path
    return thumbnail_path


def save_image(content, extname):
    relative_path = generate_image_path(content, extname)
    saved_path = path_join(conf.app.static_root, relative_path)
    content_type = getattr(conf.image.allowed_extensions, extname)

    # make parent directories
    parent_path = dirname(saved_path)
    if not exists(parent_path):
        makedirs(parent_path)

    # save original image
    if not exists(saved_path):

        with file(saved_path, 'w+') as fh:
            fh.write(content)

        save_thumbnail(saved_path)

        logger.debug('saved %s', saved_path)

        return True, relative_path

    return False, relative_path

def save_thumbnail(image_path):

    thumbnail_path = generate_thumbnail_path(image_path)
    width, height = conf.image.thumbnail_size

    im = Image.open(image_path)

    if im.size[0] >= im.size[1]:
        im = im.resize((height * im.size[0]/im.size[1], height))
        im = im.crop(((im.size[0] - width)/2, 0, (im.size[0] + width)/2, height))
    else:
        im = im.resize((width, width * im.size[1]/im.size[0]))
        im = im.crop((0, (im.size[1] - height)/2, width, (im.size[1] + height)/2))

    im.save(thumbnail_path, 'JPEG')
