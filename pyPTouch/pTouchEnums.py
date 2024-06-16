from enum import IntEnum


class ErrorInfo1(IntEnum):
    NoError = 0
    NoMedia = 0x1
    EndOfMedia = 0x2
    CutterJam = 0x4
    WeakBatteries = 0x8
    PrinterInUse = 0x10
    PrinterOff = 0x20
    HighVoltageAdaptor = 0x40
    FanMotorError = 0x80


class ErrorInfo2(IntEnum):
    NoError = 0
    WrongMedia = 0x1
    ExpansionBufferFull = 0x2
    CommunicationError = 0x4
    CommunicationBufferFull = 0x8
    CoverOpen = 0x10
    Overheating = 0x20
    BlackMarkNotFound = 0x40
    SystemError = 0x80


class MediaType(IntEnum):
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


class DynamicMode(IntEnum):
    ESC_P = 0x0
    Raster = 0x1
    P_Touch_Template = 0x3


class StatusType(IntEnum):
    Reply_To_Status = 0x0
    PrintComplete = 0x1
    Error = 0x2
    ExitIF = 0x3
    Off = 0x4
    Notification = 0x5
    PhaseChange = 0x6
    SendAdvanceData = 0xf0


class PhaseType(IntEnum):
    Editing = 0x0
    Printing = 0x1


class NotificationType(IntEnum):
    NotAvailable = 0x0
    CoverOpen = 0x1
    CoverClosed = 0x2
    CoolingStart = 0x3
    CoolingFinish = 0x4
    WaitingForPeeling = 0x5


class TapeColor(IntEnum):
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


class TextColor(IntEnum):
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


class BatteryLevel(IntEnum):
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


class ExtendedError(IntEnum):
    NoError = 0x0
    FleTapeEnd = 0x10
    HighRes_DraftPrintError = 0x1d
    AdapterPullInsertError = 0x1e
    IncompatibleMedia = 0x21


class ModelCode(IntEnum):
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


class SeriesCode(IntEnum):
    """
    Series Codes Used when decoding Printer Status Information Messages
    """
    PT = 0x30
    RJ = 0x37


class ValidFlags(IntEnum):
    PI_Kind = 0x2
    PI_Width = 0x4
    PI_Length = 0x8
    PI_Quality = 0x40
    PI_Recover = 0x80


class PrintSettings(IntEnum):
    AutoCut = 0x40
    MirrorPrinting = 0x80


class AdvancedPrintSettings(IntEnum):
    NotChainPrinting = 0x8
    SpecialTape = 0x10
    NoBufferClearing = 0x80


class CompressionModes(IntEnum):
    NoCompression = 0x0
    TIFF = 0x2
