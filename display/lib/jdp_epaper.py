from micropython import const
from machine import UART, Pin
from ustruct import pack #, unpack
from time import sleep_ms
import png

# C O N S T A N T S

# Display resolution
EPD_DISPLAY_WIDTH  = const(800)
EPD_DISPLAY_HEIGHT = const(600)

# pin values
EPD_PIN_LOW = const(0)
EPD_PIN_HIGH = const(1)

# storage
EPD_STORAGE_NAND_FLASH = const(0x00)
EPD_STORAGE_MICRO_SD = const(0x01)

# font size
EPD_FONT_SIZE_32 = const(0x01)
EPD_FONT_SIZE_48 = const(0x02)
EPD_FONT_SIZE_64 = const(0x03)

# display direction
EPD_DISPLAY_ROTATION_NORMAL = const(0x00)
EPD_DISPLAY_ROTATION_90     = const(0x01)
EPD_DISPLAY_ROTATION_180    = const(0x03)
EPD_DISPLAY_ROTATION_270    = const(0x04)

# color
EPD_COLOR_BLACK              = const(0x00)
EPD_COLOR_DARK_GRAY          = const(0x01)
EPD_COLOR_LIGHT_GRAY         = const(0x02)
EPD_COLOR_WHITE              = const(0x03)

# commands
EPD_CMD_HANDSHAKE             = const(0x00)
EPD_CMD_SET_BAUD_RATE         = const(0x01)
EPD_CMD_GET_BAUD_RATE         = const(0x02)
EPD_CMD_GET_STORAGE_AREA      = const(0x06)
EPD_CMD_SET_STORAGE_AREA      = const(0x07)
EPD_CMD_SLEEP                 = const(0x08)
EPD_CMD_REFRESH               = const(0x0A)
EPD_CMD_GET_DISPLAY_ROTATION  = const(0x0C)
EPD_CMD_SET_DISPLAY_ROTATION  = const(0x0D)
EPD_CMD_IMPORT_FONT           = const(0x0E)
EPD_CMD_IMPORT_IMAGE          = const(0x0F)
EPD_CMD_SET_COLOR             = const(0x10)
EPD_CMD_GET_COLOR             = const(0x11)
EPD_CMD_GET_ENGLISH_FONT_SIZE = const(0x1C)
EPD_CMD_GET_CHINESE_FONT_SIZE = const(0x1D)
EPD_CMD_SET_ENGLISH_FONT_SIZE = const(0x1E)
EPD_CMD_SET_CHINESE_FONT_SIZE = const(0x1F)
EPD_CMD_DRAW_PIXEL            = const(0x20)
EPD_CMD_DRAW_LINE             = const(0x22)
EPD_CMD_FILL_RECTANGLE        = const(0x24)
EPD_CMD_DRAW_RECTANGLE        = const(0x25)
EPD_CMD_DRAW_CIRCLE           = const(0x26)
EPD_CMD_FILL_CIRCLE           = const(0x27)
EPD_CMD_DRAW_TRIANGLE         = const(0x28)
EPD_CMD_FILL_TRIANGLE         = const(0x29)
EPD_CMD_CLEAR                 = const(0x2E)
EPD_CMD_DISPLAY_TEXT          = const(0x30)
EPD_CMD_DISPLAY_IMAGE         = const(0x70)
#EPD_CMD_XXX = const(0x40)
#EPD_CMD_XXX = const(0x50)

# E X C E P T I O N S

class ePaperException(Exception):
    pass

# E P A P E R  D E V I C E

def printhex(s):
    print(type(s),len(s),":".join("{:02x}".format(c) for c in s))
    #print(s)

class ePaper(object):

    def __init__(self, uartnr, baudrate, tx, rx, wakeup, reset):
        self._uart = UART(uartnr, baudrate = baudrate, tx = tx, rx = rx)
        self._wakeup = Pin(wakeup, Pin.OUT)
        self._reset = Pin(reset, Pin.OUT)
        
        self.width = EPD_DISPLAY_WIDTH
        self.height = EPD_DISPLAY_HEIGHT
        
        self.foreground_color = EPD_COLOR_BLACK
        self.background_color = EPD_COLOR_WHITE
        
        #response = self._uart.read()
        #print("Init response: {}".format(response))

    def _send(self, frame, data = None):
        self._uart.write(frame)

    def _command(self, command, parameters = None):
        frame_header = [0xA5]
        frame_length = [0x00, 0x00] # placeholder
        command_type = [command]
        command_parameter = list(parameters) if parameters else []
        frame_end = [0xCC, 0x33, 0xC3, 0x3C]
        parity = [0x00] # placeholder
        frame = bytearray(
            frame_header + 
            frame_length +
            command_type +
            command_parameter +
            frame_end +
            parity)
        # calculate frame length
        frame[1:3] = len(frame).to_bytes(2, 'big')
        # calculate parity
        for b in frame[:-1]:
            frame[-1] ^= b 
        # printhex(frame) # debug
        self._send(
            frame = frame,
            data = command_parameter)

    def reset(self):
        self._reset.value(EPD_PIN_LOW)
        sleep_ms(500)
        self._reset.value(EPD_PIN_HIGH)
        sleep_ms(500)
        self._reset.value(EPD_PIN_LOW)
        sleep_ms(3000)

    def wakeup(self):
        self._wakeup.value(EPD_PIN_LOW)
        sleep_ms(500)
        self._wakeup.value(EPD_PIN_HIGH)
        sleep_ms(500)
        self._wakeup.value(EPD_PIN_LOW)
        sleep_ms(100)
        response = self._uart.read()
        #print("Wake up response: {}".format(response))

    def sleep(self):
        self._command(command = EPD_CMD_SLEEP)

    def handshake(self):
        self._command(command = EPD_CMD_HANDSHAKE)
        sleep_ms(500)
        response = self._uart.read()
        if response != b'OK':
            #raise ePaperException('Handshake with ePaper display failed.')
            print("Unexpected response: {}".format(response))

    def set_baudrate(self, baudrate):
        self._command(
            command = EPD_CMD_SET_BAUD_RATE,
            parameters = baudrate.to_bytes(4, 'big'))
        sleep_ms(100)

    def get_baudrate(self):
        self._command(command = EPD_CMD_GET_BAUD_RATE)
        sleep_ms(100)
        response = self._uart.read()
        baudrate = int(response.decode("ASCII"))
        return baudrate

    def get_storage_area(self):
        self._command(command = EPD_CMD_GET_STORAGE_AREA)
        sleep_ms(100)
        response = self._uart.read()
        baudrate = int(response.decode("ASCII"))
        return baudrate

    #def set_storage_area(self):
    #    pass

    def refresh(self):
        self._command(command = EPD_CMD_REFRESH)
        #response = self._uart.read()
        #print("Refresh response: {}".format(response))

    def clear(self):
        self._command(command = EPD_CMD_CLEAR)

    def display_text(self, text, x, y):
        self._command(
            command = EPD_CMD_DISPLAY_TEXT,
            parameters = pack('!hh', x, y) + text.encode('hex'))
            
    def set_chinese_font(self, font_size = EPD_FONT_SIZE_32):
        self._command(
            command = EPD_CMD_SET_CHINESE_FONT_SIZE,
            parameters = pack('!B', font_size))
            
    def set_english_font(self, font_size = EPD_FONT_SIZE_32):
        self._command(
            command = EPD_CMD_SET_ENGLISH_FONT_SIZE,
            parameters = pack('!B', font_size))

    def set_color(self,
        foreground_color = EPD_COLOR_BLACK,
        background_color = EPD_COLOR_WHITE):
        
        if self.foreground_color != foreground_color or self.background_color != background_color:
            self._command(
                command = EPD_CMD_SET_COLOR,
                parameters = pack('!BB', foreground_color, background_color))
        
        self.foreground_color = foreground_color
        self.background_color = background_color

    def set_display_rotation(self,
        display_rotation = EPD_DISPLAY_ROTATION_NORMAL):
        self._command(
            command = EPD_CMD_SET_DISPLAY_ROTATION,
            parameters = pack('!B', display_rotation))
        
        if display_rotation in set([
            EPD_DISPLAY_ROTATION_NORMAL,
            EPD_DISPLAY_ROTATION_180]):
            self.width = EPD_DISPLAY_WIDTH
            self.height = EPD_DISPLAY_HEIGHT
        else:
            self.width = EPD_DISPLAY_HEIGHT
            self.height = EPD_DISPLAY_WIDTH

    def set_storage_area(self,
        storage = EPD_STORAGE_NAND_FLASH):
        self._command(
            command = EPD_CMD_SET_STORAGE_AREA,
            parameters = pack('!B', storage))

    def draw_line(self, x_start, y_start, x_end, y_end):
        self._command(
            command = EPD_CMD_DRAW_LINE,
            parameters = pack('!hhhh', x_start, y_start, x_end, y_end))

    def draw_pixel(self, x, y):
        self._command(
            command = EPD_CMD_DRAW_PIXEL,
            parameters = pack('!hh', x, y))

    def draw_png(self, x, y, image, skip_color = None):
    
        img = png.Reader(file = image)
        width, height, pixels, metadata = img.read()
        
        if not metadata['greyscale']:
            raise ePaperException('Only greyscale PNG images are supported!')
        
        if metadata['alpha']:
            raise ePaperException('PNG images with alpha channel are not supported!')
        
        if metadata['bitdepth'] > 2:
            raise ePaperException('PNG images with bitdepth higher than 2 are not supported!')
        
        _y = 0
        for pixrow in pixels:
            _x = 0
            if _y < self.height:
                for pixel in pixrow:
                    if _x < self.width:
                        if pixel != skip_color:
                            self.set_color(
                                foreground_color = pixel,
                                background_color = EPD_COLOR_WHITE)
                            self.draw_pixel(_x + x, _y + y)
                    _x += 1
            _y += 1
            
