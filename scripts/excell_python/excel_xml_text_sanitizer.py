import click

from .service.excell_service import ExcelService


@click.group()
@click.version_option(version='1.0', prog_name='excel_xml_text_sanitizer.py')
def cli():
    """Herramienta de línea de comando para realizar diferentes operaciones."""
    pass


@cli.command(name="excel")
@click.option('-i', '--input_file',
              required=True,
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help='Path to the input Excel file to be modified.')
@click.option('-o', '--output_file',
              type=click.Path(dir_okay=False, writable=True),
              help='Save path of the modified Excel file.')
@click.option('-ic', '--input_column',
              help='Name of the column in the input file to process.')
@click.option('-m', '--output_column',
              help='Name of the column in the output file where results will be saved.')
@click.option('-c', '--columns',
              is_flag=True,
              help='Print all the columns in the input file.')

def excel(input_file, output_file, input_column, output_column, columns):
    """Operaciones sobre archivos Excel."""
    excel_service = ExcelService()

    if columns:
        click.echo(f"Listing columns for: {input_file}")
        excel_service.list_columns(input_file)
        return

    is_processing_attempt = any([input_column, output_column, output_file])

    if not is_processing_attempt and not columns:
        raise click.UsageError(
            "Se especificó --input-file, pero se requiere una operación adicional para 'excel': "
            "--columns, o el conjunto completo de (--input-column, --output-column, --output-file)."
        )

    if is_processing_attempt:
        all_processing_args_defined = all([
            input_column,
            output_column,
            output_file
        ])
        if not all_processing_args_defined:
            missing = []
            if not input_column: missing.append("--input-column (-ic)")
            if not output_column: missing.append("--output-column (-m)")
            if not output_file: missing.append("--output-file (-o)")
            raise click.UsageError(
                "Para la operación de procesamiento de Excel, faltan los siguientes argumentos obligatorios: "
                f"{', '.join(missing)}."
            )
        else:
            click.echo(f"Processing file: {input_file}")
            click.echo(f"Input column: {input_column}")
            click.echo(f"Output column: {output_column}")
            click.echo(f"Saving to: {output_file}")
            # Placeholder for actual processing logic
            excel_service.xml_fields_to_text(input_file, output_file, input_column, output_column)
            return


if __name__ == '__main__':
    cli()
