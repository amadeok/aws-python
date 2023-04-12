
import logging

import argparse, distro
parser = argparse.ArgumentParser()
parser.add_argument("--log_to_file", help="log to file", default=False)
parser.add_argument("--log_level", help="log level", default=logging.DEBUG )

args = parser.parse_args()

pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)

if args.log_to_file:
    logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=args.log_level)
else: 
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

ubuntu_ver = distro.info()["version"]