import pika
import logging
import os
from luckycat import f3c_global_config

logger = logging.getLogger(os.path.basename(__file__).split(".")[0])


class WorkQueue(object):

    def __init__(self, host=None):
        if host:
            self._host = host
        else:
            self._host = f3c_global_config.queue_host

    def queue_exists(self, queue_name):
        conn = pika.BlockingConnection(pika.ConnectionParameters(self._host))
        channel = conn.channel()
        logger.debug("Checking if queue %s exists." % queue_name)
        try:
            channel.queue_declare(queue=queue_name, passive=True)
            conn.close()
            return True
        except:
            conn.close()
            return False

    def create_queue(self, prefix):
        conn = pika.BlockingConnection(pika.ConnectionParameters(self._host))
        channel = conn.channel()
        logger.debug("Creating queue %s." % prefix)
        try:
            channel.queue_declare(queue=prefix)
            channel.queue_bind(exchange='luckycat', queue=prefix)
            conn.close()
            logger.info("Queue created.")
        except:
            conn.close()
            logger.error("Could not create queue %s" % prefix)

    def get_jobs_in_queue(self, prefix):
        conn = pika.BlockingConnection(pika.ConnectionParameters(self._host))
        channel = conn.channel()
        try:
            res = channel.queue_declare(queue=prefix, passive=True)
            messages = res.method.message_count
            conn.close()
            logger.debug("Messages in queue: %d" % res.method.message_count)
            return messages
        except:
            conn.close()
            logger.error("Could not get queue info for %s" % prefix)
            raise

    def queue_is_full(self, prefix, maximum):
        value = self.get_jobs_in_queue(prefix)
        logger.debug("Total of %d job(s) in queue %s with a maximum of %d" % (value, prefix, maximum))
        return value > maximum - 1

    def queue_is_empty(self, prefix):
        value = self.get_jobs_in_queue(prefix)
        logger.debug("Total of %d job(s) in queue" % value)
        return value == 0

    def get_pending_elements(self, prefix, maximum):
        value = self.get_jobs_in_queue(prefix)
        logger.debug("Total of %d job(s) in queue" % value)
        return maximum - value

    def publish(self, queue_name, body):
        conn = pika.BlockingConnection(pika.ConnectionParameters(self._host))
        channel = conn.channel()
        channel.basic_publish(exchange='luckycat',
                              routing_key=queue_name,
                              body=body.encode('utf-8'))
        conn.close()

    def get_channel(self):
        conn = pika.BlockingConnection(pika.ConnectionParameters(self._host))
        channel = conn.channel()
        return channel
