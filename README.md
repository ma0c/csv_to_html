# CSV to HTML

The objective of this script is to transform a given row of a CSV into an HTML, that could be printed via a browser.

## Usage

```bash
python csv_to_html.py --input file.csv --output output.html --row 1
```

Remember that row 0 is the header of the CSV file


Also we prepare a new script to export each row using a plain text template

`template.txt`:

```text
My name is {{name}} and my last name is {{last_name}}
```

`example.csv`:

```csv
name,last_name
Ma0,Collazos
Karla,Alzate
```


```bash
python csv_to_html_with_template.py --input file.csv --template template.txt --output output.txt --row 1
```

## Contributing

This software is licensed under the MIT LICENSE.

To begin contributing please create a virtual environment

```bash
python -m venv csv_to_html_venv
source csv_to_html_venv/bin/activate
# En windows
# csv_to_html_venv\Scripts\activate 
pip install -r requirements.txt
```

To generate executable in windows execute

```bash
pyinstaller --onefile csv_to_html.py
```
