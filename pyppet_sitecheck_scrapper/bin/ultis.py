"""
    Geo-Instruments
    Daily Sitecheck Scanner
    Repository: https://geodev.geo-instruments.com/DanEdens/pyppet_sitecheck_scrapper

    Utilities Package for Scanner

"""


async def wait_type(page, selector, txt):
    """
    Wait for a selector to load than type supplied text.
    Returns page in case entering text changes the context.
    """
    await page.waitForSelector(selector)
    await page.type(selector, txt)
    return page


async def wait_click(page, selector):
    """
    Wait for a selector to load than clicks on it.
    Returns page in case this changes the context.
    """
    await page.waitForSelector(selector),
    await page.click(selector)
    return page


async def wait_hover(page, selector):
    """
    Wait for a selector to load than hover over it.
    Returns page in case this changes the context.
    """
    await page.waitForSelector(selector),
    await page.hover(selector)
    return page


def disable_timeout_pyppeteer():
    """
    Allows Browser to be left open indefinitely
    Keeps Session open longer than 20 seconds.
    """
    import pyppeteer.connection

    original_method = pyppeteer.connection.websockets.client.connect

    def new_method(*args, **kwargs):
        kwargs['ping_interval'] = None
        kwargs['ping_timeout'] = None
        return original_method(*args, **kwargs)

    pyppeteer.connection.websockets.client.connect = new_method


