#!/usr/bin/env python

import pecan
from webtest import TestApp
from peacock import model


class command(pecan.commands.BaseCommand):
    '''Initialize database.'''

    def run(self, args):
        super(command, self).run(args)
        self.load_app()
        model.init_model()
        model.start()
        model.db_sync()
