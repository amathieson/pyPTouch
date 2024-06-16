import enum
import struct
from dataclasses import dataclass

import usb.backend.libusb1
from ctypes import c_void_p, c_int


class ErrorInfo1(enum.IntEnum):
    NoError = 0
    NoMedia = 0x1
    EndOfMedia = 0x2
    CutterJam = 0x4
    WeakBatteries = 0x8
    PrinterInUse = 0x10
    PrinterOff = 0x20
    HighVoltageAdaptor = 0x40
    FanMotorError = 0x80


class ErrorInfo2(enum.IntEnum):
    NoError = 0
    WrongMedia = 0x1
    ExpansionBufferFull = 0x2
    CommunicationError = 0x4
    CommunicationBufferFull = 0x8
    CoverOpen = 0x10
    Overheating = 0x20
    BlackMarkNotFound = 0x40
    SystemError = 0x80


class MediaType(enum.IntEnum):
    NoMedia = 0x0
    LaminatedTape = 0x1
    NonLaminatedTape = 0x3
    FabricTape = 0x4
    HGTape = 0x9
    HeatShrinkHS2_1 = 0x11
    FleTape = 0x13
    FlexIDTape = 0x14
    SatinTape = 0x15
    HeatShrinkHS3_1 = 0x17
    ContinuousLengthTape = 0x4a
    DieCutLabels = 0x4b
    Incompatible = 0xff


class DynamicMode(enum.IntEnum):
    ESC_P = 0x0
    Raster = 0x1
    P_Touch_Template = 0x3


class StatusType(enum.IntEnum):
    Reply_To_Status = 0x0
    PrintComplete = 0x1
    Error = 0x2
    ExitIF = 0x3
    Off = 0x4
    Notification = 0x5
    PhaseChange = 0x6
    SendAdvanceData = 0xf0


class PhaseType(enum.IntEnum):
    Editing = 0x0
    Printing = 0x1


class NotificationType(enum.IntEnum):
    NotAvailable = 0x0
    CoverOpen = 0x1
    CoverClosed = 0x2
    CoolingStart = 0x3
    CoolingFinish = 0x4
    WaitingForPeeling = 0x5


class TapeColor(enum.IntEnum):
    White = 0x01
    Other = 0x02
    Clear = 0x03
    Red = 0x04
    Blue = 0x05
    Yellow = 0x06
    Green = 0x07
    Black = 0x08
    ClearWhiteText = 0x09
    MatteWhite = 0x20
    MatteClear = 0x21
    MatteSilver = 0x22
    SatinGold = 0x23
    SatinSilver = 0x24
    BlueD = 0x30
    RedD = 0x31
    FluorescentOrange = 0x40
    FluorescentYellow = 0x41
    BerryPinkS = 0x50
    LightGrayS = 0x51
    LimeGreenS = 0x52
    YellowF = 0x60
    PinkF = 0x61
    BlueF = 0x62
    WhiteHeatShrinkTube = 0x70
    WhiteFlexId = 0x90
    YellowFlexId = 0x91
    Cleaning = 0xF0
    Stencil = 0xF1
    Incompatible = 0xFF


class TextColor(enum.IntEnum):
    White = 0x01
    Red = 0x04
    Blue = 0x05
    Black = 0x08
    Gold = 0x0A
    Blue_F = 0x62
    Clearing = 0xF0
    Stencil = 0xF1
    Other = 0x02
    Incompatible = 0xFF


class BatteryLevel(enum.IntEnum):
    Full = 0x0
    Half = 0x1
    Low = 0x2
    NeedCharging = 0x3
    UsingAC = 0x4
    Unknown = 0xFF
    FullP910 = 0x20
    OverCharged_P910 = 0x21
    Half_P910 = 0x22
    Low_P910 = 0x23
    NeedCharging_P910 = 0x24
    Full_ACConnected_P910 = 0x30
    OverCharged_ACConnected_P910 = 0x31
    Half_ACConnected_P910 = 0x32
    Low_ACConnected_P910 = 0x33
    NeedCharging_ACConnected_P910 = 0x34
    BatteryNotInstalled_ACConnected_P910 = 0x37


class ExtendedError(enum.IntEnum):
    NoError = 0x0
    FleTapeEnd = 0x10
    HighRes_DraftPrintError = 0x1d
    AddapterPullInsertError = 0x1e
    IncompatibleMedia = 0x21


class ModelCode(enum.IntEnum):
    RJ_4030 = 0x31
    RJ_4040 = 0x32
    RJ_3050 = 0x33
    RJ_3150 = 0x34
    RJ_4030Ai = 0x35
    RJ_2030 = 0x36
    RJ_2050 = 0x37
    RJ_2140 = 0x38
    RJ_2150 = 0x39
    RJ_4230B = 0x43
    RJ_4250WB = 0x44
    RJ_3230B = 0x45
    RJ_3250WB = 0x46

    PT_9800PCN = 0x61
    PT_9700PC = 0x62
    PT_H500 = 0x64
    PT_E500 = 0x65
    PT_P700 = 0x67
    PT_P900W = 0x69
    PT_P950NW = 0x70
    PT_P900 = 0x71
    PT_P910BT = 0x78


class SeriesCode(enum.IntEnum):
    PT = 0x30
    RJ = 0x37


@dataclass
class StatusInformation:
    HeadMark: int
    Size: int
    BrotherCode: int
    SeriesCode: int
    ModelCode: ModelCode
    CountryCode: int
    BatteryLevel: BatteryLevel  # Newer Printer
    ExtendedError: int  # Newer Printer
    ErrorInfo1: ErrorInfo1
    ErrorInfo2: ErrorInfo2
    MediaWidth: int
    MediaType: MediaType
    NumberColours: int
    Fonts: int
    JapaneseFonts: int
    Mode: DynamicMode
    Density: int
    MediaLength: int
    StatusType: StatusType
    PhaseType: PhaseType
    PhaseNumber: int
    NotificationType: NotificationType
    ExpansionArea: int
    TapeColour: TapeColor
    TextColour: TextColor
    HardwareSettings: int
    Reserved3: int
    Reserved4: int


backend = usb.backend.libusb1.get_backend(find_library=lambda x: "libusb-1.0.dll")
backend.lib.libusb_set_option.argtypes = [c_void_p, c_int]
dev = usb.core.find(idVendor=0x04F9, idProduct=0x2061, backend=backend)

# Check if the device is found
if dev is None:
    raise ValueError("Device not found")

# Set the active configuration. With no arguments, the first configuration will be the active one
dev.set_configuration()

# Get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0, 0)]

# Find the OUT endpoint
ep_out = usb.util.find_descriptor(
    intf,
    # Match the first OUT endpoint
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
)

# Find the IN endpoint
ep_in = usb.util.find_descriptor(
    intf,
    # Match the first IN endpoint
    custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
)

assert ep_out is not None
assert ep_in is not None

# Define a command to send
command = b'\0' * 100 + b'\x1b@\x1biS'

# Send the command to the OUT endpoint
ep_out.write(command)

# Read the response from the IN endpoint
response = ep_in.read(64)  # Adjust the size according to your device's response size

# Convert the response to a string (assuming it is text data)
response_str = ' '.join([hex(x) for x in response])
unpacked_data = struct.unpack('<BBBBBBBBBBBBBBBBBBBBHBBBBIBB', response)

response_obj = StatusInformation(
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
for k, v in response_obj.__dict__.items():
    if isinstance(v, enum.IntEnum):
        print(f'{k}: {v.name} ({hex(v)})')
    else:
        print(f'{k}: {hex(v)}')


# Define a command to send
command = (
        b'\0'*100 + b'\x1b@\x1bia\x01' +                        # RESET Printer & Initialize, Set Mode to Raster
        b'\x1biz\x84\x01\x12\x00\x73\x00\x00\x00\x00\x00' +     # Printer Configuration - PI_WIDTH | PI_RECOVER, Laminated tape, 18mm x 0mm, 115 Lines, On First Page, ZERO
        b'\x1biM\x40' +                                         # Configure Auto Cutting
        b'\x1biK\x08' +                                         # Adv. Config No Chain Printing
        b'\x1bid\x0e\x00' +                                     # Margin 14pt x 0pt
        b'M\x00' +                                              # Compression Mode - None
        (b'G\x10\x00' + b'\x55' * 16) * 115 +                   # Graphics Data
        b'\x1a'                                                 # End Of Transmission
)

# Send the command to the OUT endpoint
ep_out.write(command)

# Release the device
usb.util.dispose_resources(dev)
