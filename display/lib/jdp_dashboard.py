import ujson
import urequests

from jdp_network import wlan_connect, wlan_disconnect

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

def render_footer(text, display, padding = 4, font_size = EPD_FONT_SIZE_32):
    
    if font_size == EPD_FONT_SIZE_64:
        text_heigt = 64
    elif font_size == EPD_FONT_SIZE_48:
        text_heigt = 48
    else:
        text_heigt = 32
    
    footer_y = display.height - padding - text_heigt
    separator_y = footer_y - padding
    
    display.set_color(
        foreground_color = EPD_COLOR_BLACK,
        background_color = EPD_COLOR_WHITE)
    
    display.draw_line(
        padding, separator_y ,
        display.width - padding, separator_y)
    
    display.set_english_font(font_size = font_size)
    display.display_text(text, padding, footer_y)

def render_tile(column, row, image, display,
    padding = 4, footer_height = 32 + 2 * 4):
    slot_width = (display.width - 3 * padding) // 2 # 294
    slot_height = (display.height - footer_height - 9 * padding) // 8 # 90
    
    display.draw_png(
        x = (slot_width + padding) * column + padding,
        y = (slot_height + padding) * row + padding,
        image = image,
        skip_color = display.background_color)

def show_dashboard(config, display_time=15):
    """
    Tiles are placed on a 2x8 grid.
    Display size = 600x800 pixels.
    Padding = 4 pixels.
    Horizontal sizes:
        1 slot  = 294 pixels
        2 slots = 592 pixels
        Footer  = 592 pixels
    Vertical sizes:
        1 slot  = 90 pixels
        2 slots = 184 pixels
        3 slots = 278 pixels
        4 slots = 372 pixels
        5 slots = 466 pixels
        6 slots = 560 pixels
        7 slots = 654 pixels
        8 slots = 752 pixels
        Footer  = 40 pixels
    Tile format:
        - tiles must be PNG images
        - tiles must be grayscale
        - only 4 colors allowed (black, dark gray, light gray, white)
        - alpha channel is not supported
        - bit depth must not be higher than 2
    """
    
    cfg = get_configuration(config)
    if cfg:
        display_time = cfg['dashboard']['sleep']
        
        epd = ePaper(
            uartnr = cfg['display']['uartnr'],
            baudrate = cfg['display']['baudrate'],
            tx = cfg['display']['tx'],
            rx = cfg['display']['rx'],
            wakeup = cfg['display']['wakeup'],
            reset = cfg['display']['reset'])
        
        dashboard = None
        
        try:
            if (wlan_connect(
                essid = cfg['wlan']['essid'],
                password = cfg['wlan']['password'],
                timeout = cfg['wlan']['timeout'])):
            
                response = urequests.get(cfg['dashboard']['url'])
                if (response.status_code == 200):
                    dashboard = response.json()
                    response.close()
                
                if dashboard and dashboard['meta']['format'] == 'tile-png':
                    init_display(display = epd)
                    
                    for tile in dashboard['data']:
                        print(tile['x'], tile['y'], tile['image'])
                        response = urequests.get(tile['image'], stream = True)
                        if (response.status_code == 200):
                            img = response.raw
                            render_tile(
                                row = tile['x'],
                                column = tile['y'],
                                image = img,
                                display = epd)
                            response.close()
                    
                    render_footer(
                        text = "{}    {}    {}".format(
                            dashboard['meta']['created'],
                            dashboard['meta']['user'],
                            dashboard['meta']['location']),
                        display = epd)
                    
                    epd.refresh()
        finally:
            wlan_disconnect(timeout = cfg['wlan']['timeout'])
            epd.sleep()
        
    return display_time