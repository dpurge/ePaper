from jdp_flashcards import get_configuration, show_png
from jdp_network import get_raw_from_url


print('Starting...')
    
cfg = get_configuration('/config.json')

if cfg:
    
    img = get_raw_from_url(
        url = 'http://www.schaik.com/pngsuite/basn0g02.png', #cfg['flashcards']['url'],
        essid = cfg['wlan']['essid'],
        password = cfg['wlan']['password'],
        timeout = cfg['wlan']['timeout'])
        
    if img:
        show_png(
            image = img,
            config = cfg['display'])
    
    print("TODO: sleep {} minutes".format(cfg['flashcards']['sleep']))
    
print("Done!")

