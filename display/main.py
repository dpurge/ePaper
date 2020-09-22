from jdp_flashcards import get_configuration, show_flashcards
from jdp_network import get_json_from_url


print('Starting...')
    
cfg = get_configuration('/config.json')

if cfg:
    
    cards = get_json_from_url(
        url = cfg['flashcards']['url'],
        essid = cfg['wlan']['essid'],
        password = cfg['wlan']['password'],
        timeout = cfg['wlan']['timeout'])
        
    if cards:
        show_flashcards(
            cards = cards,
            config = cfg['display'])
    
    print("TODO: sleep {} minutes".format(cfg['flashcards']['sleep']))
    
print("Done!")

