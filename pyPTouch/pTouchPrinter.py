import struct
import usb.core
import usb.util
import usb.backend.libusb1
from usb.core import Device
from ctypes import c_void_p, c_int
import io
from .pTouchEnums import (
    ModelCode, BatteryLevel, ExtendedError, ErrorInfo1, ErrorInfo2, MediaType,
    DynamicMode, StatusType, PhaseType, NotificationType, TapeColor, TextColor,
    CompressionModes, ValidFlags, PrintSettings, AdvancedPrintSettings
)
from pyPTouch.pTouchStatusInformation import StatusInformation


class PTouchPrinter:
    _tape_width: int
    _tape_length: int
    _device: Device
    _ep_in: io.BytesIO
    _ep_out: io.BytesIO
    _media_type: MediaType
    _print_settings: PrintSettings
    _advanced_settings: AdvancedPrintSettings

    def __enter__(self) -> 'PTouchPrinter':
        """
        Enter the runtime context related to this object. This is used by the with statement.

        :return: The PTouchPrinter instance
        """
        self._start_printer()
        return self

    def __exit__(self, type, value, traceback) -> bool:
        """
        Exit the runtime context related to this object. This is used by the with statement.

        :param type: The exception type
        :param value: The exception value
        :param traceback: The traceback object
        :return: False, indicating any exception is propagated
        """
        usb.util.dispose_resources(self._device)
        return False

    def get_information(self) -> StatusInformation:
        """
        Get the status information from the printer.

        :return: The status information as a StatusInformation object
        :raises ValueError: If the device is not initialized
        """
        if self._device is None:
            raise ValueError('Device not initialized')

        # Define a command to send
        command = b'\0' * 100 + b'\x1b@\x1biS'

        # Send the command to the OUT endpoint
        self._ep_out.write(command)

        # Read the response from the IN endpoint
        response = self._ep_in.read(64)  # Adjust the size according to your device's response size

        # Convert the response to a string (assuming it is text data)
        unpacked_data = struct.unpack('<BBBBBBBBBBBBBBBBBBBBHBBBBIBB', response)

        return StatusInformation(
            HeadMark=unpacked_data[0],
            Size=unpacked_data[1],
            BrotherCode=unpacked_data[2],
            SeriesCode=unpacked_data[3],
            ModelCode=ModelCode(unpacked_data[4]),
            CountryCode=unpacked_data[5],
            BatteryLevel=BatteryLevel(unpacked_data[6]),
            ExtendedError=ExtendedError(unpacked_data[7]),
            ErrorInfo1=ErrorInfo1(unpacked_data[8]),
            ErrorInfo2=ErrorInfo2(unpacked_data[9]),
            MediaWidth=unpacked_data[10],
            MediaType=MediaType(unpacked_data[11]),
            NumberColours=unpacked_data[12],
            Fonts=unpacked_data[13],
            JapaneseFonts=unpacked_data[14],
            Mode=DynamicMode(unpacked_data[15]),
            Density=unpacked_data[16],
            MediaLength=unpacked_data[17],
            StatusType=StatusType(unpacked_data[18]),
            PhaseType=PhaseType(unpacked_data[19]),
            PhaseNumber=unpacked_data[20],
            NotificationType=NotificationType(unpacked_data[21]),
            ExpansionArea=unpacked_data[22],
            TapeColour=TapeColor(unpacked_data[23]),
            TextColour=TextColor(unpacked_data[24]),
            HardwareSettings=unpacked_data[25],
            Reserved3=unpacked_data[26],
            Reserved4=unpacked_data[27],
        )

    def print(self, raster_image: bytes, line_count: int, margins: tuple[int, int]) -> None:
        """
        Send a print command to the printer.

        :param raster_image: The raster image data to print
        :param line_count: The number of lines in the raster image
        :param margins: The margins for the print job (width, length)
        :raises ValueError: If the device is not initialized
        """
        if self._device is None:
            raise ValueError('Device not initialized')
        command = (
            self._reset_printer_command() + self._mode_selection_command() +
            self._printer_configuration_command(ValidFlags.PI_Recover | ValidFlags.PI_Width, line_count, False) +
            self._print_settings_command() +
            self._margins_command(margins[0], margins[1]) +
            self._compression_command(CompressionModes.NoCompression) +
            self._graphics_command(raster_image, line_count) +
            b'\x1a'
        )
        self._ep_out.write(command)

    def _start_printer(self) -> None:
        """
        Initialize the printer device and set up the endpoints.

        :raises ValueError: If the device is not found
        """
        backend = usb.backend.libusb1.get_backend(find_library=lambda x: "libusb-1.0.dll")
        backend.lib.libusb_set_option.argtypes = [c_void_p, c_int]
        self._device = usb.core.find(idVendor=0x04F9, idProduct=0x2061, backend=backend)

        # Check if the device is found
        if self._device is None:
            raise ValueError("Device not found")

        # Set the active configuration. With no arguments, the first configuration will be the active one
        self._device.set_configuration()

        # Get an endpoint instance
        cfg = self._device.get_active_configuration()
        intf = cfg[(0, 0)]

        # Find the OUT endpoint
        self._ep_out = usb.util.find_descriptor(
            intf,
            # Match the first OUT endpoint
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )

        # Find the IN endpoint
        self._ep_in = usb.util.find_descriptor(
            intf,
            # Match the first IN endpoint
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )

        assert self._ep_out is not None
        assert self._ep_in is not None

    def _reset_printer_command(self) -> bytes:
        """
        Generate the reset printer command.

        :return: The reset command as bytes
        """
        return b'\0' * 100 + b'\x1b@'

    def _mode_selection_command(self) -> bytes:
        """
        Generate the mode selection command.

        :return: The mode selection command as bytes
        """
        return b'\x1bia\x01'

    def _printer_configuration_command(self, valid_flags: ValidFlags, line_count: int, first_page: bool) -> bytes:
        """
        Generate the printer configuration command.

        :param valid_flags: Flags the printer should check when printing
        :param line_count: Number of lines to print
        :param first_page: Flag indicating if this is the first page
        :return: The printer configuration command as bytes
        """
        return (b'\x1biz'
                + struct.pack('<BBBBI?B', valid_flags, self._media_type, self._tape_width, self._tape_length,
                              line_count, first_page, 0))

    def _print_settings_command(self) -> bytes:
        """
        Generate the print settings command.

        :return: The print settings command as bytes
        """
        return (b'\x1biM' + struct.pack("B", self._print_settings) +
                b'\x1biK' + struct.pack("B", self._advanced_settings))

    def _margins_command(self, margin_width: int, margin_length: int) -> bytes:
        """
        Generate the margins command.

        :param margin_width: The margins along the width of the label
        :param margin_length: The margins along the length of the label
        :return: The margins command as bytes
        """
        return b'\x1bid' + struct.pack("BB", margin_width, margin_length)

    def _compression_command(self, compression_mode: CompressionModes) -> bytes:
        """
        Generate the compression command.

        :param compression_mode: The compression mode
        :return: The compression command as bytes
        """
        return b'M' + struct.pack("B", compression_mode)

    def _graphics_command(self, raster_image: bytes, line_count: int) -> bytes:
        """
        Generate the graphics command.

        :param raster_image: The raster image data
        :param line_count: The number of lines in the raster image
        :return: The graphics command as bytes
        :raises AssertionError: If the raster image length is incorrect
        """
        assert len(raster_image) == 16 * line_count
        buff = []
        for i in range(line_count):
            buff.append(struct.pack("BBBBBBBBBBBBBBBB", *raster_image[i * 16:i * 16 + 16]))
        return b'G\x10\x00' + b'G\x10\x00'.join(buff)

    @property
    def tape_width(self) -> int:
        """
        Width of Tape in mm - This should be rounded to the nearest int.

        Standard TZe tapes listed below:
        3.5mm -> `4`
        6mm   -> `6`
        9mm   -> `9`
        12mm  -> `12`
        18mm  -> `18`
        24mm  -> `24`

        :return: Tape width in mm
        """
        return self._tape_width

    @tape_width.setter
    def tape_width(self, value: int) -> None:
        """
        Set the tape width - This should be rounded to the nearest int.

        Standard TZe tapes listed below:
        3.5mm -> `4`
        6mm   -> `6`
        9mm   -> `9`
        12mm  -> `12`
        18mm  -> `18`
        24mm  -> `24`

        :param value: The tape width in mm
        """
        self._tape_width = round(value)

    @property
    def tape_length(self) -> int:
        """
        Length of the tape in mm - for laminated continuous tape set to 0mm

        :return: Length of the tape in mm
        """
        return self._tape_length

    @tape_length.setter
    def tape_length(self, value: int) -> None:
        """
        Set the tape length.

        :param value: The tape length in mm
        """
        self._tape_length = round(value)

    @property
    def media_type(self) -> MediaType:
        """
        Media type of the printer

        :return: Media Type
        """
        return self._media_type

    @media_type.setter
    def media_type(self, value: MediaType) -> None:
        """
        Set the media type.

        :param value: MediaType
        """
        self._media_type = value

    @property
    def print_settings(self) -> PrintSettings:
        """
        Printer Settings - Generally includes details for Automatic Cutting, and Mirror Printing, etc.

        :return: Printer Settings
        """
        return self._print_settings

    @print_settings.setter
    def print_settings(self, value: PrintSettings) -> None:
        """
        Set the print settings.

        :param value: PrintSettings
        """
        self._print_settings = value

    @property
    def advanced_settings(self) -> AdvancedPrintSettings:
        """
        Printer Advanced Settings - Generally includes details for Chain Printing, Special tape (no Cutting),
        and Buffer Clearing, etc.

        :return: Printer Advanced Settings
        """
        return self._advanced_settings

    @advanced_settings.setter
    def advanced_settings(self, value: AdvancedPrintSettings) -> None:
        """
        Set the advanced settings.

        :param value: AdvancedPrintSettings
        """
        self._advanced_settings = value
