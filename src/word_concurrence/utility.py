import os
import argparse

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def remove_all_duplicates(dir):
	for root, dirs, files in os.walk(dir):
		for file in files:
			remove_duplicates(os.path.join(root,file))

def main(args):
	if args.rd is True:
		if not args.path:
			print 'Supply a path to remove duplicates'
		else:
			if args.path_type == 'directory':
				remove_all_duplicates(args.path)
			elif args.path_type == 'file':
				remove_duplicates(args.path)
			else:
				print 'Specify a path type'

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Utility tools')
	parser.add_argument('-r','--remove_duplicates', dest='rd', action="store_true", help='Remove duplicate lines from file')
	parser.add_argument('-p','--path', dest='path', help='Path used by the tool')
	parser.add_argument('-t','--path_type', dest='path_type', help='directory or file')
	args = parser.parse_args()
	main(args)
