from pyPTouch.pTouchEnums import PrintSettings, AdvancedPrintSettings
from pyPTouch.pTouchPrinter import PTouchPrinter

with PTouchPrinter() as printer:
    info = printer.get_information()
    print(info)
    printer.tape_width = info.MediaWidth
    printer.tape_length = 0
    printer.media_type = info.MediaType
    printer.print_settings = PrintSettings.AutoCut
    printer.advanced_settings = AdvancedPrintSettings.NotChainPrinting

    printer.print(b'\x55'*(16*115), 115, (14, 0), )

