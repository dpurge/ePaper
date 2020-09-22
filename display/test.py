from jdp_flashcards import get_configuration, init_display, show_footer
from jdp_epaper import ePaper, EPD_DISPLAY_WIDTH, EPD_DISPLAY_HEIGHT, EPD_DISPLAY_ROTATION_90, EPD_COLOR_BLACK, EPD_COLOR_WHITE

import font_pol_64

######
class Writer():

    text_row = 0        # attributes common to all Writer instances
    text_col = 0
    row_clip = False    # Clip or scroll when screen full
    col_clip = False    # Clip or new line when row is full

    @classmethod
    def set_textpos(cls, row, col):
        cls.text_row = row
        cls.text_col = col
        
    def __init__(self, display, font):
        self.display = display
        self.font = font
        if not font.hmap():
            raise ValueError('Font must be horizontally mapped.')
        # rotated screen
        self.screenwidth = 600
        self.screenheight = 800

    def _newline(self):
        height = self.font.height()
        Writer.text_row += height
        Writer.text_col = 0
        #margin = self.screenheight - (Writer.text_row + height)
        #if margin < 0:
        #    if not Writer.row_clip:
        #        #self.device.scroll(0, margin)
        #        Writer.text_row += margin
                
    def _printchar(self, char):
    
        if char == '\n':
            self._newline()
            return
        
        glyph, char_height, char_width = self.font.get_ch(char)
        
        #if Writer.text_row + char_height > self.screenheight:
        #    if Writer.row_clip:
        #        return
        #    else:
        #        self._newline()
            
        #if Writer.text_col + char_width > self.screenwidth:
        #    if Writer.col_clip:
        #        return
        #    else:
        #        self._newline()
                
        # TODO
        #self.display.display_text(char, Writer.text_row, Writer.text_col)
        
        div, mod = divmod(char_width, 8)
        rowbytes = div + 1 if mod else div
        
        drow = Writer.text_row
        for pixrow in range(char_height):
            for pixcol in range(char_width):
                dcol = Writer.text_col + pixcol
                gbyte, gbit = divmod(pixcol, 8)
                if gbit == 0:
                    data = glyph[pixrow * rowbytes + gbyte]
                if data & (1 << (7 - gbit)):
                    self.display.draw_pixel(dcol, drow)
            drow += 1
            if drow >= self.screenheight or drow < 0:
                break
        
        Writer.text_col += char_width

    def printstring(self, string):
        for char in string:
            self._printchar(char)
######


print('Starting...')
    
cfg = get_configuration('/config.json')

if cfg:
    
    epd = ePaper(
        uartnr = cfg['display']['uartnr'],
        baudrate = cfg['display']['baudrate'],
        tx = cfg['display']['tx'],
        rx = cfg['display']['rx'],
        wakeup = cfg['display']['wakeup'],
        reset = cfg['display']['reset'])
        
    try:
        init_display(epd)
        
        for x in range(600):
            epd.draw_pixel(x, 200)
        
        wri = Writer(epd, font_pol_64)
        Writer.set_textpos(10, 10)
        wri.printstring('Łódź.\n')
        wri.printstring('Źdźbło.\n')
        wri.printstring('Siała-baba-mak.\n')

        show_footer(
            text = "{}    {}".format('2018-11-21', 'Test'),
            display = epd)
        epd.refresh()
    finally:
        epd.sleep()
    
print("Done!")