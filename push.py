import fileinput
import json

import common


def main():
    args = common.args
    worksheet_name = args.worksheet_name
    spreadsheet_key = args.sheet_key
    spreadsheet = common.gc.open_by_key(spreadsheet_key)

    existing_worksheets = [x.title for x in spreadsheet.worksheets()]
    print(f"{spreadsheet_key=} {worksheet_name=}")
    first, cnt, headers, to_upload = True, 0, [], []
    
    for line in fileinput.input(files=args.files if len(args.files) > 0 else ("-",)):
        if line.strip():
            record = json.loads(line)
            if first:
                headers = list(record.keys())
                to_upload.append(headers)
                first = False
            to_upload.append(list(record.values()))

    if worksheet_name not in existing_worksheets:
        worksheet = spreadsheet.add_worksheet(
            worksheet_name, len(to_upload), len(headers)
        )
    else:
        worksheet = spreadsheet.worksheet(worksheet_name)
    worksheet.append_rows(to_upload)
    url = worksheet.url.replace(
        'https://sheets.googleapis.com/v4/spreadsheets/', 'https://docs.google.com/spreadsheets/d/'
    )
    print(f"Saved {len(to_upload)} rows with headers: {headers}\nURL: {url}")


if __name__ == "__main__":
    main()
