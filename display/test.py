from jdp_dashboard import *

def render_header(text,display):
    pass

def render_image(x, y, url, display):
    response = urequests.get(url, stream = True)
    if (response.status_code == 200):
        display.draw_png(x, y, image = response.raw)

mapping['render_header'] = (render_header, {'display':None})
mapping['render_image'] = (render_image, {'display':None})
    
print('Starting...')
sleep_time = show_dashboard('/config.json')
print("TODO: sleep {} minutes".format(sleep_time))
print("Done!")