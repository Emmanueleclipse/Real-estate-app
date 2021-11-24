import logging
import pika

""" Sometimes we are just given the channel and do not have the queue object to reference """

def channel_send(channel, queue_name, message):
	channel.basic_publish(exchange='',routing_key=queue_name,body=message,properties=pika.BasicProperties(delivery_mode = 2, )) # make message persistent

""" Class that allows adding a string to a named queue. Currently RabbitMQ, add new classes for other backends. (c) BienFacile 2013 """

class ScraperQueue:

	def __init__(self):
	# Set up connection to RabbitMQ
		logging.basicConfig(level = logging.WARNING) # Stop pika from throwing up exception upon closing connection
		credentials = pika.PlainCredentials('classifieds', 'nTW7LM7QS0Ikt468')
		self.parameters = pika.ConnectionParameters('188.226.165.134', 5672, 'classifieds', credentials)
		self.rabbitmq_link = pika.BlockingConnection(self.parameters)
		self.channel = self.rabbitmq_link.channel()

	def open(self, queue_name):
		self.channel.queue_declare(queue=queue_name, durable=True)

	def sleep(self, seconds):
		self.rabbitmq_link.sleep(seconds)

	def ensureopen(self, queue_name):
		while self.rabbitmq_link.is_closed:
			print "Reopening link"
			self.rabbitmq_link = pika.BlockingConnection(self.parameters)
			self.rabbitmq_link.connect()
		while self.channel.is_closed:
			print "Opening queue"
			self.channel.open()
			self.channel.queue_declare(queue=queue_name, durable=True)

	def send(self, queue_name, message):
		try:
			sent = self.channel.basic_publish(exchange='',routing_key=queue_name,body=message,properties=pika.BasicProperties(delivery_mode = 2, )) # make message persistent
# Work out why it always returns false, no matter what
#			if not sent:
#				print "Rabbitmq unable to send to queue: %s" % queue_name
		except pika.exceptions.ConnectionClosed as exc:
			print "Rabbitmq interrupted trying to send to queue: %s" % queue_name

	def worker(self, queue_name, callback_func):
		print "Starting: %s" % queue_name
		self.worker = self.rabbitmq_link.channel()
		self.worker.basic_qos(prefetch_count=1)
		self.open(queue_name)
		self.worker.basic_consume(callback_func, queue=queue_name)
		self.worker.start_consuming()

	def empty(self, queue_name):
		self.channel.queue_purge()

	def close(self):
		self.channel.close()
		self.rabbitmq_link.close()

	def ping(self):
		print "PING!"
