from jdp_dashboard import *

#import font_pol_64
#from jdp_writer import JdpWriter

def render_header(text,display):
    display.set_english_font(font_size = EPD_FONT_SIZE_64)
    display.display_text(text = text, x = 10, y = 10)

def render_png_image(x, y, url, display):
    response = urequests.get(url, stream = True)
    if (response.status_code == 200):
        display.draw_png(x, y, image = response.raw)

def render_bmp_image(x, y, url, display):
    response = urequests.get(url, stream = True)
    if (response.status_code == 200):
        print(response.raw)

mapping['render_header'] = (render_header, {'display':None})
mapping['render_png_image'] = (render_png_image, {'display':None})
mapping['render_bmp_image'] = (render_bmp_image, {'display':None})
    
print('Starting...')
sleep_time = show_dashboard('/config.json')
print("TODO: sleep {} minutes".format(sleep_time))
print("Done!")