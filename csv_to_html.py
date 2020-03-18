#!/usr/bin/env python

import argparse
import csv
import itertools
import logging
import os

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.StreamHandler())


def generate_html(input_file_path, output_file_path=None, row=1):
    with open(input_file_path) as input_file:
        reader = csv.reader(input_file)
        header = next(reader)
        interested_line = next(itertools.islice(reader, row-1, None))
        html_content = ""
        for title, response in zip(header, interested_line):
            if response:
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


class Application(tk.Frame):
    _file_name = ""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select CSV").grid(row=0)
        self.select_csv = tk.Button(self)
        self.select_csv["text"] = "Select CSV"
        self.select_csv["command"] = self.open_dialog
        self.select_csv.grid(row=0, column=1)
        tk.Label(self, text="Selected CSV").grid(row=1)
        self.selected_csv = tk.Label(self)
        self.selected_csv.grid(row=1, column=1)
        tk.Label(self, text="Output File").grid(row=2)
        self.output_file = tk.Entry(self)
        self.output_file.insert(tk.END, "output.html")
        self.output_file.grid(row=2, column=1)

        tk.Label(self, text="Row").grid(row=3)
        self.row = tk.Entry(self)
        self.row.insert(tk.END, "1")
        self.row.grid(row=3, column=1)

        self.process = tk.Button(self, text="Process", command=self.execute_script)
        self.process.grid(row=4)

    def open_dialog(self):
        self._file_name = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        self.selected_csv["text"] = self._file_name

    def execute_script(self):
        try:
            generate_html(self._file_name, self.output_file.get(), int(self.row.get()))
            messagebox.showinfo("File created successfully", f"File created: {self.output_file.get()}")
        except UnicodeDecodeError as ude:
            LOGGER.error(ude)
            messagebox.showerror("Error", "Unable to open file")
        except ValueError as ve:
            LOGGER.error(ve)
            messagebox.showerror("Error", "Row needs to be a number")
        except FileNotFoundError as fnf:
            LOGGER.error(fnf)
            messagebox.showerror("Error", "File not found")


def launch_gui():
    root = tk.Tk()
    root.title("CSV to HTML")
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser("""
The objective of this script is to transform a given row of a CSV into an HTML, that could be printed via a browser  Example.

csv_to_html.py file.csv --output output.html --row 1
    """)
    parser.add_argument("--input", help="Input file to process")
    parser.add_argument("--output", help="If not defined, output will appear on console")
    parser.add_argument("--row", type=int, help="If not defined default is 1", default=1)
    parser.add_argument("--debug", default="ERROR")
    parser.add_argument("--no_gui", default=False, action='store_true')
    args = vars(parser.parse_args())
    if args['no_gui']:
        generate_html(args["input"], args["output"], args["row"])
    else:
        launch_gui()
