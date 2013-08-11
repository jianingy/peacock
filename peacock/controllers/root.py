from pecan import conf, expose, redirect, override_template, abort
from peacock import util
from peacock.model import api as db_api
from peacock import exception
from webob.exc import status_map
from os.path import join as path_join, splitext, exists
from os import makedirs
import short_url
import pecan
import logging

logger = logging.getLogger(__name__)


class RootController(object):

    @expose(template='index.html')
    def index(self):

        def _htmldata(x):
            return {'original': '/i/%s' % short_url.encode_url(x.id),
                    'thumbnail': '/t/%s' % short_url.encode_url(x.id)}
        images = map(_htmldata, db_api.get_image_list(0, 20))
        return dict(images=images)

    @expose(generic=True)
    def create(self):
        abort(403)

    @expose('json')
    @create.when(method='POST')
    def create_post(self, image):

        unused, extname = splitext(image.filename)
        extname = extname.lower()[1:]

        if not hasattr(conf.image.allowed_extensions, extname):
            raise exception.NotAllowedImageExtension(extname=extname)

        content = image.file.read()
        content_type = getattr(conf.image.allowed_extensions, extname)
        saved, relative_path = util.save_image(content, extname)

        resp = dict()
        if saved:

            image_id = db_api.create_image(relative_path=relative_path,
                                           content_type=content_type)

            surl = short_url.encode_url(image_id)
            resp = {'message': 'success', 'reason': 'created'}
        else:
            try:
                image = db_api.get_image_by_relative_path(relative_path)
                surl = short_url.encode_url(image.id)
                resp = {'message': 'success', 'reason': 'exists'}
            except exception.ImageNotFound:
                image_id = db_api.create_image(relative_path=relative_path,
                                               content_type=content_type)
                surl = short_url.encode_url(image_id)
                resp = {'message': 'success', 'reason': 'created'}

        if pecan.request.path.endswith('.html'):
            return redirect('/')
        else:
            return resp

    @expose()
    def i(self, short):
        try:
            image_id = short_url.decode_url(short)
        except ValueError:
            raise exception.ImageNotFound(reference=short)
        image = db_api.get_image_by_id(image_id=image_id)
        saved_path = path_join(conf.app.static_root,
                               image.relative_path.encode('UTF-8'))
        with file(saved_path) as fh:
            content = fh.read()
        override_template(None, content_type='image/png')
        return content

    @expose()
    def t(self, short):
        try:
            image_id = short_url.decode_url(short)
        except ValueError:
            raise exception.ImageNotFound(reference=short)

        image = db_api.get_image_by_id(image_id=image_id)
        relative_path = image.relative_path.encode('UTF-8')
        thumbnail_path = util.generate_thumbnail_path(relative_path)
        saved_path = path_join(conf.app.static_root, thumbnail_path)

        if not exists(saved_path):
            logger.debug('generating thumbnail on accessing: %s' % \
                         saved_path)
            util.save_thumbnail(saved_path)

        with file(saved_path) as fh:
            content = fh.read()

        override_template(None, content_type='image/jpeg')
        return content

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)
