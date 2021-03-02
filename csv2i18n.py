#!/bin/env python3

import argparse
import sys

from common import *

parser = argparse.ArgumentParser(description='Transform CSV to i18n for use in epsilon.')
parser.add_argument('file', help='Input file, without the langage part.')
args = parser.parse_args()

data, langs = load_csv(args.file + ".csv")

if (data, langs) == (None, None):
    print("Invalid input " + args.file)
    sys.exit(1)

data, langs = clean_data(data, langs)

print(data, langs)

save_i18n(args.file, data, langs)

