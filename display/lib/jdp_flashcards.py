import ujson

from jdp_epaper import ePaper
from jdp_epaper import EPD_STORAGE_NAND_FLASH
from jdp_epaper import EPD_FONT_SIZE_32,EPD_FONT_SIZE_48, EPD_FONT_SIZE_64
from jdp_epaper import EPD_COLOR_BLACK, EPD_COLOR_WHITE, EPD_COLOR_DARK_GRAY
from jdp_epaper import EPD_DISPLAY_ROTATION_NORMAL, EPD_DISPLAY_ROTATION_90

def get_configuration(filename):
    configuration = None
    with open(filename, 'r') as cfg:
        configuration = ujson.loads(cfg.read())
    return configuration
    
def init_display(display):
    #display.reset()
    display.wakeup()
    display.handshake()

    display.set_storage_area(EPD_STORAGE_NAND_FLASH)
    display.set_display_rotation(EPD_DISPLAY_ROTATION_90)

    display.set_color(EPD_COLOR_BLACK, EPD_COLOR_WHITE)
    display.clear()
    
def show_lang_vocab_ind(data, display):

    x = 10
    y = 10
    
    tabsize = 30
    
    for card in data:
        display.set_english_font(font_size = EPD_FONT_SIZE_48)
        display.display_text(card['phrase'], x, y)
        y += 50
        display.set_english_font(font_size = EPD_FONT_SIZE_32)
        display.display_text(card['translation'], x + tabsize, y)
        y += 40
        print(card)

def show_footer(text, display):
    x = 10
    y = 764
    display.draw_line(10, 760 , 590, 760)
    display.set_english_font(font_size = EPD_FONT_SIZE_32)
    display.display_text(text, x, y)

def show_flashcards(cards, config):

    render = {
        'lang-vocab-ind': show_lang_vocab_ind
    }

    format = cards['meta']['format']
    
    epd = ePaper(
        uartnr = config['uartnr'],
        baudrate = config['baudrate'],
        tx = config['tx'],
        rx = config['rx'],
        wakeup = config['wakeup'],
        reset = config['reset'])
        
    try:
        init_display(epd)
        
        if format in render:
            render[format](data = cards['data'], display = epd)
        else:
            pass
        #epd.set_chinese_font(font_size = EPD_FONT_SIZE_64)
        #epd.display_text("Ð»Ð»", 50, 50)
        #epd.display_text("Äã»áËµÓ¢ÓïÂð£¿", 50, 146)

        #epd.set_english_font(font_size = EPD_FONT_SIZE_48)
        #epd.set_color(EPD_COLOR_DARK_GRAY, EPD_COLOR_WHITE)
        #epd.display_text("Hello, World!", 50, 240)

        #epd.display_text(cards['meta']['format'], 10, 340)

        show_footer(
            text = "{}    {}".format(cards['meta']['created'], format),
            display = epd)
        epd.refresh()
    finally:
        epd.sleep()