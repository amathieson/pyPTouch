# pyPTouch Library

pyPTouch is a Python library to interface with Brother PTouch label printers. It allows you to get printer status information and send print commands.

## Installation

To install the required dependencies, use the following command:

```bash
pip install pyusb
```

## Usage

### Initialization and Cleanup

Use the `PTouchPrinter` class with a context manager to ensure proper initialization and cleanup of the printer device.

```python
from pyPTouch.pTouchPrinter import PTouchPrinter

with PTouchPrinter() as printer:
    # Use the printer instance here
```

### Getting Printer Information

Retrieve the status information of the printer.

```python
status_info = printer.get_information()
print(status_info)
```

### Printing

Send a print command to the printer with raster image data, line count, and margins.

```python
raster_image = b'...'  # Your raster image data
line_count = 10  # Number of lines in the raster image
margins = (10, 10)  # Margins (left, right)

printer.print(raster_image, line_count, margins)
```

### Properties

- **tape_width**: Width of the tape in mm.
- **tape_length**: Length of the tape in mm.
- **media_type**: Media type of the printer.
- **print_settings**: Print settings of the printer.
- **advanced_settings**: Advanced print settings of the printer.

### Example

```python
from pyPTouch.pTouchPrinter import PTouchPrinter, MediaType, PrintSettings, AdvancedPrintSettings

with PTouchPrinter() as printer:
    printer.tape_width = 12  # 12mm tape
    printer.tape_length = 0  # Continuous tape
    printer.media_type = MediaType.Laminated
    printer.print_settings = PrintSettings.AutomaticCutting
    printer.advanced_settings = AdvancedPrintSettings.ChainPrinting

    # Get printer information
    status_info = printer.get_information()
    print(status_info)

    # Send print command
    raster_image = b'...'  # Your raster image data
    line_count = 10  # Number of lines in the raster image
    margins = (10, 10)  # Margins (left, right)
    printer.print(raster_image, line_count, margins)
```

## Class and Method Documentation

### `PTouchPrinter`

#### Methods

- `__enter__() -> PTouchPrinter`
  - Enter the runtime context related to this object. This is used by the `with` statement.

- `__exit__(type, value, traceback) -> bool`
  - Exit the runtime context related to this object. This is used by the `with` statement.

- `get_information() -> StatusInformation`
  - Get the status information from the printer.

- `print(raster_image: bytes, line_count: int, margins: tuple[int, int]) -> None`
  - Send a print command to the printer.

#### Properties

- `tape_width: int`
  - Width of Tape in mm. Possible values: 4, 6, 9, 12, 18, 24.

- `tape_length: int`
  - Length of the tape in mm. For laminated continuous tape, set to 0 mm.

- `media_type: MediaType`
  - Media type of the printer.

- `print_settings: PrintSettings`
  - Print settings of the printer.

- `advanced_settings: AdvancedPrintSettings`
  - Advanced print settings of the printer.

### `StatusInformation`

Check the `StatusInformation` class in the `pyPTouch.pTouchStatusInformation` module for detailed information on the status fields.

## License

This library is provided under the LGPL License.