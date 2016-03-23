from auth_manager import AuthManager
from tag_manager import TagManager
from logger import Logger
from custom_listener import CustomListener
from custom_stream import CustomStream
import os
import sys

MAIN_PROGRAM_FILE_PATH = 'stream_tweets_main.py'


if __name__ == '__main__':
    if len(sys.argv) != 4:
		print "$ stream_tweets_main [destinationFolder] [credentials] [tagList]"
		quit()
    try:
        DATA_DIRECTORY = os.path.join(sys.argv[1])
        LOG_FILE_DIRECTORY = os.path.join(sys.argv[1],'log')
        CREDENTIALS_FILE_PATH = os.path.join(sys.argv[2])
        TAG_FILE_PATH = os.path.join(sys.argv[3])
        if not os.path.exists(DATA_DIRECTORY):
            os.makedirs(DATA_DIRECTORY)
        if not os.path.exists(LOG_FILE_DIRECTORY):
            os.makedirs(LOG_FILE_DIRECTORY)

        auth_manager = AuthManager(CREDENTIALS_FILE_PATH)
        num_handlers = len(auth_manager.auth_handlers)
        tag_manager = TagManager(TAG_FILE_PATH, num_handlers)
        logger = Logger(LOG_FILE_DIRECTORY)

        for i in xrange(num_handlers):
            listener = CustomListener(i, DATA_DIRECTORY, sys.argv[0], logger)
            stream = CustomStream(listener, auth_manager.auth_handlers[i], tag_manager.distributed_tag_list[i])
            stream.stream(async=True)
    except IOError:
        print '{0} stopped running...'.format(sys.argv[0])
    except:
        logger.log(500, 0, 'Some run-time error has occurred. Restarting...')
        os.system('python {0} {1} {2} {3}'.format(sys.argv[0],sys.argv[1],sys.argv[2],sys.argv[3]))

