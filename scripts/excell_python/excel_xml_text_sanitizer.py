import pandas as pd
import re
import argparse

parser = argparse.ArgumentParser("Utility to extract XML tags from an Excel file and save the results to a new Excel file.")
parser.add_argument('-i', '--input_file', help='Path to the input Excel file to be modified.')
parser.add_argument('-o', '--output_file', help='Save path to of the modified Excel file.')
parser.add_argument('-m', '--modified_column', help='Save path to of the modified Excel file.')
parser.add_argument('-c', '--columns', action='store_true', help='Print all the columns in the input file.')
parser.add_argument('-v', '--version', action='version', version='%(prog)s Version: 1.0')
args = parser.parse_args()

if not args.input_file:
    parser.error("Input file path is required.")
else:
    try:
        dataframe = pd.read_excel(args.input_file)
    except Exception as e:
        print(f"Error reading the input file: {e}")
        exit(1)
    if args.columns:
        for column in dataframe.columns:
            print(column)
    elif args.modified_column and not args.output_file:
        parser.error("Output file path is required.")
    elif args.output_file and not args.modified_column:
        parser.error("Modified column is required.")
    elif args.modified_column and args.output_file:
        columns = dataframe[args.modified_column]
        # Regex pattern to match xml closing tags
        pattern = r'\</(.*?)\>'

        # Change to plain text
        try:
            for index, column in enumerate(columns):
                # Ensure the column value is not null
                if pd.notna(column):
                    regex_results = re.findall(pattern, str(column))
                    extracted_value = ''
                    for result in regex_results:
                        extracted_value = extracted_value + f'{result}: {column.split(f'<{result}>')[1].split(f'</{result}>')[0]} \n'

                    dataframe.at[index, args.modified_column] = extracted_value
                else :
                    dataframe.at[index, args.modified_column] = '[Empty]'
        except Exception as e:
            print(f'Unexpected error processing excel file: {e}')

        # Save contents to Excel file
        dataframe.to_excel(args.output_file, index=False)

        print("Excel file updated successfully.")




