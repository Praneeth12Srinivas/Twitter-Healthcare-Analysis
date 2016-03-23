from tweepy.streaming import StreamListener
import os
import json
import jsonpickle
from datetime import datetime
from utility import byteify

class CustomListener(StreamListener):

    def __init__(self, index, data_dir, main_program_file_path, logger):
        self.index = index
        self.data_dir = data_dir
        self.main_program_file_path = main_program_file_path
        self.logger = logger
        super(CustomListener, self).__init__()

    def on_data(self, raw_data):
        today = datetime.utcnow().date()
        dir = self.data_dir + '/' + today.strftime('%Y-%m-%d')
        if not os.path.exists(dir):
            os.makedirs(dir)
        master = open('{0}/{1}_{2}.json'.format(dir, 'master', str(self.index)), 'a')
        data = byteify(json.loads(raw_data))
	try:
		print data['text']
		master.write(jsonpickle.encode(data, unpicklable=False)+'\n')
		master.close()
	except (AttributeError,KeyError):
		master.close()

    def on_error(self, status_code):
        if status_code == 420 or status_code == 503:
            # Restart and disconnect
            os.system(self.main_program_file_path)
            return False  # Disconnects the stream
        self.logger.log(status_code, self.index, None)
