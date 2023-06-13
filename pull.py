import json
import sys
from csv import DictWriter

from pydash import py_

import common


def main():
    def get_records_from_worksheet(key, name):
        spreadsheet = common.gc.open_by_key(key)
        ws = spreadsheet.worksheet(name)
        header, *rows = ws.get_all_values()
        return [dict(zip(header, row)) for row in rows]

    format_types = ["json", "jsonlines", "csv"]
    assert (
        common.args.output_format in format_types
    ), f"Output format type not implemented: {common.args.output_format}"

    data = get_records_from_worksheet(common.args.sheet_key, common.args.worksheet_name)

    if common.args.output_format == "jsonlines":
        for doc in data:
            print(json.dumps(doc))
    elif common.args.output_format.output_format == "json":
        print(json.dumps(data))
    elif common.args.output_format == "csv":
        fields = list(py_.head(data).keys())
        writer = DictWriter(sys.stdout, fieldnames=fields)
        writer.writeheader()
        for record in data:
            writer.writerow(record)


if __name__ == "__main__":
    main()
