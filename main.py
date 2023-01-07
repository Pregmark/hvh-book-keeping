import csv
from datetime import datetime
from os import walk

financial_year_start = datetime(datetime.today().year - 2, 10, 1)
financial_year_end = datetime(datetime.today().year - 1, 9, 30)


def parse_bank_statements():
    with open(r'C:\Users\Samuel\Downloads\bank_statements_' + str(financial_year_end.year) + '.csv', 'r') \
            as statement_file:
        reader = csv.reader(statement_file)
        # Skip first line containing headers
        next(reader)

        # Only return statements within the financial year
        bank_statement_list = [row[0] for row in reader if verify_bank_statement_date(row[0])]

        return bank_statement_list


def verify_bank_statement_date(bank_statement):
    # Convert date str to datetime object
    bank_statement_datetime = format_bank_statement(bank_statement[0:10])

    # Returns true if the statement date is within the financial year
    return bank_statement_datetime < financial_year_start or bank_statement_datetime > financial_year_end


def parse_receipts():
    receipts_list = []

    for (dir_path, dir_names, file_names) in walk(
            r'C:\Users\Samuel\Downloads\receipts_' + str(financial_year_end.year)):
        for file_name in file_names:
            if file_name and file_name[0].isdigit():
                # Only take the date from the file name
                receipts_list.append(file_name.split(" ", 1)[0])

    return receipts_list


def find_missing_receipts(bank_statements, receipts):
    bank_statements_formatted = [format_bank_statement(d) for d in bank_statements]
    receipts_formatted = [format_receipt(d) for d in receipts]

    # If no matching receipt is found for a statement, print out the statement
    for u, uf in zip(bank_statements, bank_statements_formatted):
        if uf not in receipts_formatted:
            print(u)


def format_bank_statement(date):
    date_stripped = date.split(';')[0]
    return datetime.strptime(date_stripped, '%Y-%m-%d')


def format_receipt(date):
    return datetime.strptime(date, '%y%m%d')


if __name__ == '__main__':
    bank_statement_list = parse_bank_statements()
    receipt_list = parse_receipts()
    find_missing_receipts(bank_statement_list, receipt_list)
