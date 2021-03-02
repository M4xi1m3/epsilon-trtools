#!/bin/env python3

import argparse
import sys

from common import *

parser = argparse.ArgumentParser(description='Transform i18n to CSV for editing.')
parser.add_argument('file', help='Input file, without the langage part.')
args = parser.parse_args()

data, langs = load_i18n(args.file)

if (data, langs) == (None, None):
    print("Invalid input " + args.file)
    sys.exit(1)

data, langs = clean_data(data, langs)

save_csv(args.file + ".csv", data, langs)

