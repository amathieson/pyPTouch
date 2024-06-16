from dataclasses import dataclass
from .pTouchEnums import *


@dataclass
class StatusInformation:
    HeadMark: int
    Size: int
    BrotherCode: int
    SeriesCode: int
    ModelCode: ModelCode
    CountryCode: int
    BatteryLevel: BatteryLevel
    ExtendedError: int
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

    def __repr__(self):
        buff = []
        for k, v in self.__dict__.items():
            if isinstance(v, IntEnum):
                buff.append(f'{k}: {v.name} ({hex(v)})')
            else:
                buff.append(f'{k}: {hex(v)}')
        return "StatusInformation {\n\t" + '\n\t'.join(buff) + "\n}"

    def __str__(self):
        return self.__repr__()
