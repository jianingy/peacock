#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4


class PicoException(Exception):

    message = 'An unknown exception occured'

    def __init__(self, **kwargs):

        try:
            self.kwargs = kwargs
            self._error_string = self.message % kwargs
        except:
            self._error_string = self.message


    def __str__(self):
        return self._error_string


class NotAllowedImageExtension(PicoException):
    message = 'The file extension "%(extname)s" is not allowed'


class ImageNotFound(PicoException):
    message = 'Image %(reference)s not found'
