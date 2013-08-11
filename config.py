# Server Specific Configurations
server = {
    'port': '8080',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'peacock.controllers.root.RootController',
    'modules': ['peacock'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/peacock/templates',
    'default_renderer': 'jinja',
    'debug': True,
    'errors': {
        404: '/error/404',
        '__force_dict__': True
    }
}

logging = {
    'loggers': {
        'root': {'level': 'INFO', 'handlers': ['console']},
        'peacock': {'level': 'DEBUG', 'handlers': ['console']}
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       '[%(threadName)s] %(message)s')
        }
    }
}

# Bindings and options to pass to SQLAlchemy's ``create_engine``
sqlalchemy = {
    'url'           : 'sqlite:///peacock.db',
    'echo'          : 'debug',
    'echo_pool'     : False,
    'pool_recycle'  : 3600,
    'encoding'      : 'utf-8'
}

image = {
    'allowed_extensions': {
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'gif': 'image/gif',
    },
    'thumbnail_size': (177, 180),
}
# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf
