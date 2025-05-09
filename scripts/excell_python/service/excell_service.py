import pandas as pd
import re
import os

class ExcelService:
    """
    Class to handle Excel file operations.
    """

    def xml_fields_to_text(self, input_file, output_file, input_column, output_column):
        """
        Function to transform XML string to plain text.
        """

        # Regex pattern to match xml closing tags
        pattern = r'\</(.*?)\>'

        # Read the Excel file
        try:
            dataframe = self._read_excel(input_file)
        except Exception as e:
            print(f'Error leyendo el archivo Excel: {e}')
            return

        # Read the column that contains the data to be modified
        columns = dataframe[input_column]

        # Change to plain text
        try:
            for index, column in enumerate(columns):
                # Ensure the column value is not null
                if pd.notna(column):
                    regex_results = re.findall(pattern, str(column))
                    extracted_value = ''
                    for result in regex_results:
                        extracted_value = extracted_value + f'{result}: {column.split(f'<{result}>')[1].split(f'</{result}>')[0]} \n'

                    dataframe.at[index, output_column] = extracted_value
                else:
                    dataframe.at[index, output_column] = '[Empty]'
        except Exception as e:
            print(f'Unexpected error processing excel file: {e}')

            # Save contents to Excel file
            dataframe.to_excel(output_file, index=False)
            print("Excel file updated successfully.")

    def list_columns(self, input_file):
        """
        Function to list the columns of an Excel file.
        :param input_file:
        """
        try:
            dataframe = self._read_excel(input_file)
            for column in dataframe.columns:
                print(column)
        except Exception as e:
            print(f'Error leyendo el archivo Excel: {e}')
            return

    def _read_excel(self, input_file):
        """
        Read the Excel file and return a DataFrame.
        """
        # Validate file extension
        if not input_file.endswith(('.xls', '.xlsx')):
            raise ValueError("El archivo no es un archivo de Excel válido.")
        elif not os.path.exists(input_file):
            raise FileNotFoundError("El archivo no existe.")
        dataframe = pd.read_excel(input_file)

        return dataframe
