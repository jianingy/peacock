from pecan.hooks import TransactionHook
from pecan import make_app
from peacock import model


def setup_app(config):

    model.init_model()

    return make_app(
        config.app.root,
        static_root=config.app.static_root,
        template_path=config.app.template_path,
        default_renderer=config.app.default_renderer,
        logging=getattr(config, 'logging', {}),
        debug=getattr(config.app, 'debug', False),
        hooks = [
            TransactionHook(
                model.start,
                model.start_read_only,
                model.commit,
                model.rollback,
                model.clear)],
        force_canonical=getattr(config.app, 'force_canonical', True),
        guess_content_type_from_ext=getattr(
            config.app,
            'guess_content_type_from_ext',
            True),
    )
