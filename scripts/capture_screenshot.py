from playwright.sync_api import sync_playwright
import os

def capture(url, output_path, viewport_width=1920, viewport_height=1080):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': viewport_width, 'height': viewport_height})
        page.goto(url, wait_until='networkidle')
        page.screenshot(path=output_path, full_page=False)
        browser.close()

if __name__ == '__main__':
    os.makedirs('screenshots', exist_ok=True)
    shots = [
        ('https://fixmytyrenow.com',                  'screenshots/home_desktop_1920.png',  1920, 1080),
        ('https://fixmytyrenow.com',                  'screenshots/home_laptop_1366.png',   1366,  768),
        ('https://fixmytyrenow.com',                  'screenshots/home_tablet_768.png',     768, 1024),
        ('https://fixmytyrenow.com',                  'screenshots/home_mobile_375.png',     375,  812),
        ('https://fixmytyrenow.com/areas/barnet/',    'screenshots/barnet_desktop_1920.png', 1920, 1080),
        ('https://fixmytyrenow.com/areas/barnet/',    'screenshots/barnet_mobile_375.png',   375,  812),
    ]
    for url, path, w, h in shots:
        print(f'Capturing {url} at {w}x{h} -> {path}')
        capture(url, path, w, h)
    print('Done.')
