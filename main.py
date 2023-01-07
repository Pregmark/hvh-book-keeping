from datetime import datetime
import datetime
import csv
from os import walk

financial_year_start = datetime.datetime(datetime.date.today().year - 2, 10, 1)
financial_year_end = datetime.datetime(datetime.date.today().year - 1, 9, 30)


def parse_bank_statements():
    with open(r'C:\Users\Samuel\Downloads\bank_statements_' + str(financial_year_end.year) + '.csv', 'r') \
            as statement_file:
        reader = csv.reader(statement_file)

        bank_statement_list = []

        for rows in reader:
            current_row = rows[0]
            if verify_bank_statement_date(current_row):
                bank_statement_list.append(current_row)

        return bank_statement_list


def verify_bank_statement_date(bank_statement):
    # First row contains headers not containing dates, disregard
    if not bank_statement[0].isdigit():
        return False

    # Convert date str to datetime object
    bank_statement_datetime = datetime_from_statement_date(bank_statement[0:10])

    # If the date is not within the current financial year being evaluated, return false
    if bank_statement_datetime < financial_year_start or bank_statement_datetime > financial_year_end:
        return False

    return True


def parse_receipts():
    receipts_list = []

    for(dir_path, dir_names, file_names) in walk(r'C:\Users\Samuel\Downloads\receipts_' + str(financial_year_end.year)):
        for file_name in file_names:
            if file_name and file_name[0].isdigit():
                # Only take the date from the file name
                receipts_list.append(file_name.split(" ", 1)[0])

    return receipts_list


def datetime_from_statement_date(date):
    trimmed_month = date[5:7]

    # datetime takes months without the starting 0, remove if present
    if trimmed_month.startswith('0'):
        trimmed_month = trimmed_month[1]

    # Pick out the year, month and day from the str
    return datetime.datetime(int(date[0:4]), int(trimmed_month), int(date[8:10]))


def find_missing_receipts(bank_statements, receipts):
    matched_statements = []

    bank_statements_formatted = [format_bank_statement(d) for d in bank_statements]
    receipts_formatted = [format_receipt(d) for d in receipts]

    # If no matching receipt is found for a statement, print out the statement
    for u, uf in zip(bank_statements, bank_statements_formatted):
        if uf not in receipts_formatted:
            print(u)

    return matched_statements


def format_bank_statement(date):
    date_stripped = date.split(';')[0]
    return datetime.datetime.strptime(date_stripped, '%Y-%m-%d')


def format_receipt(date):
    return datetime.datetime.strptime(date, '%y%m%d')


if __name__ == '__main__':
    bank_statement_list = parse_bank_statements()
    receipt_list = parse_receipts()
    find_missing_receipts(bank_statement_list, receipt_list)
