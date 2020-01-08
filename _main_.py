#Daily Sitecheck Web Scrapper V. 4.0.0
import sys
import asyncio
from pyppeteer import launch
sys.path.append('/env/')
from env import sites,text













# async def main():
    
    # browser = await launch(headless=False)
    # page = await browser.newPage()
#     await page.goto('http://example.com')
#     await page.screenshot({'path': 'example.png'})

#     dimensions = await page.evaluate('''() => {
#         return {
#             width: document.documentElement.clientWidth,
#             height: document.documentElement.clientHeight,
#             deviceScaleFactor: window.devicePixelRatio,
#         }
#     }''')

#     print(dimensions)
#     # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
#     await browser.close()

# asyncio.get_event_loop().run_until_complete(main())