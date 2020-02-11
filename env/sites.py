"""
    This file removes non-human readable code from __main__
    Provides a consolidated reference for debugging Webpage navigation

    Currently Supported Sites:
    Amp - <project.name>.geo-instruments.com/index.php
    Quickview - https://quickview.geo-instruments.com/login.php
    Truelook (currently unstable) - https://app.truelook.com/<project specific>
"""

from env import creds


class amp:
    """
        Text values for use in Amp-specific Events

        type: (str)
        username, password, label, logincss, pwcss,
        urlstring, loginbutton, planview,
        csspath, title, sensor

        *username and password are called from here before creds
        to maintain loop consistency with QV during login()
    """
    username = creds.ampuser
    password = creds.amppass
    label = ['3', '4']
    logincss = '#s_text_login_name'
    pwcss = '#s_password_login_password'
    urlstring = '.geo-instruments.com/index.php'
    loginbutton = 'body > div > form > input.button'
    planview = '?s_cat=project&i_project=17&i_planview='
    csspath = '> div:nth-child('
    title = ') > a:nth-child(1)'
    sensor = ') > a:nth-child(3)'


class qv:
    """
        Text values for use in QV-specific Events

        type: (str)
        username, password, logincss, pwcss, urlstring,
        loginbutton, projects, proj_pre, proj_post, views,
        thumb, scrollbar, scrollbar2, hoverbox
    """
    username = creds.qvuser
    password = creds.qvpass
    logincss = '#user'
    pwcss = '#pass'
    urlstring = 'https://quickview.geo-instruments.com/login.php'
    loginbutton = '#login > form > button'
    projects = '#menuProjects > a > i'
    proj_pre = 'div#projectList div:nth-child('
    proj_post = ') > div.panelRowTxt2'
    views = 'li#menuViews p'
    thumb = '#thumb'
    scrollbar = 'body > div.wrapper > div.sidePanel.ui-resizable > div.ui-resizable-handle.ui-resizable-e'
    scrollbar2 = 'body > div.wrapper > div.sidePanel.ui-resizable > img'
    hoverbox = "#hoverBox"


class truelook:
    """
        Text values for use in Truelook-specific Events

        type: (str)
        urlstring, planview,
        logincss, pwcss, loginbutton,
    """
    urlstring = '.geo-instruments.com/index.php'
    logincss = 'input#tl_login_username'
    pwcss = 'input#tl_login_password'
    loginbutton = 'keyboard.press(\'Enter\')'  # broken
    planview = 'img#tl_live_image'
