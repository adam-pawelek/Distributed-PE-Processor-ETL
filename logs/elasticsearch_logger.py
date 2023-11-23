import logging
import os
import socket
import json
import time

class LogstashHandler(logging.Handler):
    def __init__(self, host, port):
        logging.Handler.__init__(self)
        self.host = host
        self.port = port

    def emit(self, record):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        log_entry = self.format(record)
        s.sendall(log_entry.encode('utf-8'))
        s.close()

    def format(self, record):
        data = {
            "@timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "message": record.getMessage(),
            "level": record.levelname,
        }
        return json.dumps(data) + "\n"


