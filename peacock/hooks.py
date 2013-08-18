#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

from pecan import conf
from pecan.hooks import PecanHook
import pika

class AMQPHook(PecanHook):

    def before(self, state):
        credentials = pika.PlainCredentials(conf.amqp.user, conf.amqp.password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(conf.amqp.host, conf.amqp.port,
                                      credentials=credentials))
        channel = connection.channel()

        channel.exchange_declare(exchange=conf.amqp.queue, type='direct',
                                 durable=True, auto_delete=False)

        state.request.channel = channel
