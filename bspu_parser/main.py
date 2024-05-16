from bspuparser import BspuParser
import logging

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

bspu_parser = BspuParser()
bspu_parser.parse_college()
bspu_parser.parse_university()