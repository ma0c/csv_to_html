#!/usr/bin/env python

import argparse
import csv
import itertools
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())


def generate_html(input_file_path, output_file_path=None, row=1):
    with open(input_file_path) as input_file:
        reader = csv.reader(input_file)
        header = next(reader)
        interested_line = next(itertools.islice(reader, row-1, None))
        html_content = ""
        for title, response in zip(header, interested_line):
            html_content += f"""
<h3>{title}</h3>
<br/>
<pre>{response}</pre>
"""

        if output_file_path is None:
            print(html_content)
        else:
            with open(output_file_path, "w+") as output_file:
                output_file.write(html_content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("""
The objective of this script is to transform a given row of a CSV into an HTML, that could be printed via a browser  Example.

csv_to_html.py file.csv --output output.html --row 1
    """)
    parser.add_argument("input")
    parser.add_argument("--output", help="If not defined, output will appear on console")
    parser.add_argument("--row", type=int, help="If not defined default is 1", default=1)
    parser.add_argument("--debug", default="ERROR")
    args = vars(parser.parse_args())
    generate_html(args["input"], args["output"], args["row"])

