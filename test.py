# Import necessary modules and classes for working with the PTouch printer
from pyPTouch.pTouchEnums import PrintSettings, AdvancedPrintSettings
from pyPTouch.pTouchPrinter import PTouchPrinter


def generate_chevrons(num_rows=8, width=16):
    """
    Generate a chevron pattern from random binary data.

    :param num_rows: Number of rows to generate.
    :param width: Number of bytes per row (fixed at 16 for 128 bits).
    :return: Chevron pattern as a list of bytes objects.
    """
    chevrons = []  # List to store each row of the chevron pattern
    indent = 0  # Initial indentation for the chevron pattern
    indent_step = 1  # Step size for changing the indent, affecting the sharpness of the chevron

    for _ in range(num_rows):
        row = b'\xff' * 16  # Create a row filled with 0xff (all bits set)

        # Create a new row with the current indent
        chevron_row = (
            b'\x00' * indent +                # Add leading indentation
            row[:width - indent] +            # Add the main part of the row with adjusted width
            row[:width - indent] +            # Duplicate the main part for the chevron effect
            b'\x00' * indent                  # Add trailing indentation
        )
        chevrons.append(chevron_row)  # Add the row to the chevrons list

        # Update the indentation for the chevron pattern, wrapping within the width limit
        indent = (indent + indent_step) % width

    return chevrons  # Return the generated chevron pattern


if __name__ == '__main__':
    # Open a PTouchPrinter instance as 'printer' using a context manager
    with PTouchPrinter() as printer:
        # Fetch and print the printer's current information for the user
        info = printer.get_information()
        print(info)

        # Configure the print settings for the current print job
        printer.tape_width = info.MediaWidth         # Set the tape width based on the printer's media width
        printer.tape_length = 0                      # Set tape length (0 typically means auto length)
        printer.media_type = info.MediaType          # Set media type based on printer's media type
        printer.print_settings = PrintSettings.AutoCut       # Enable automatic cutting after printing
        printer.advanced_settings = AdvancedPrintSettings.NotChainPrinting  # Disable chain printing mode

        line_count = 128  # Define the number of lines to be printed

        # Generate the raster data (chevron pattern) to be printed
        raster = generate_chevrons(line_count, 8)

        # Print the generated raster data with specified parameters
        printer.print(b''.join(raster), line_count, (14, 0))
