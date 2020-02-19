# -*- coding: utf-8 -*-

"""
This file is part of the **pyppeteer_sitecheck_scrapper**
project git@geodev.geo-instruments.com:DanEdens/pyppet_sitecheck_scrapper.git

:platform: Windows
:license:
:synopsis: Code to create a startup shell link

.. moduleauthor::  Dan Edens @DanEdens <Dan.Edens@geo-instruments.com>
"""

import os
import sys
from comtypes.GUID import GUID
import comtypes
import ctypes
from ctypes.wintypes import (
    LPWSTR,
    LPCWSTR,
    DWORD,
    INT,
    WORD,
    FILETIME,
    WCHAR,
    USHORT,
    BYTE,
    LPVOID,
    HWND,
    BOOL,
    LPCOLESTR,
    LPOLESTR
)


APP_NAME = 'SitecheckScanner'
PATH = os.path.join(
    os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup'),
    APP_NAME + ".lnk"
)


HRESULT = LPVOID
MAX_PATH = 255
POINTER = ctypes.POINTER
COMMETHOD = comtypes.COMMETHOD
CLSCTX_INPROC_SERVER = comtypes.CLSCTX_INPROC_SERVER


LIBID_ShellCoreObjects = GUID('{56f9f44f-f74c-4e38-99bc-9f3ebd3d696a}')
IID_IShellLinkW = GUID('{000214F9-0000-0000-C000-000000000046}')
CLSID_ShellLink = GUID('{00021401-0000-0000-C000-000000000046}')


class _SHITEMID(ctypes.Structure):
    _fields_ = [
        ('cb', USHORT),
        ('abID', BYTE * 1)
    ]


SHITEMID = _SHITEMID
LPSHITEMID = POINTER(SHITEMID)
SHITEMID = POINTER(LPSHITEMID)


class _ITEMIDLIST(ctypes.Structure):
    _fields_ = [
        ('mkid', SHITEMID)
    ]


ITEMIDLIST = _ITEMIDLIST
LPITEMIDLIST = POINTER(ITEMIDLIST)
PIDLIST_ABSOLUTE = LPITEMIDLIST
PCIDLIST_ABSOLUTE = POINTER(PIDLIST_ABSOLUTE)


class _WIN32_FIND_DATAW(ctypes.Structure):
    _fields_ = [
        ('dwFileAttributes', DWORD),
        ('ftCreationTime', FILETIME),
        ('ftLastAccessTime', FILETIME),
        ('ftLastWriteTime', FILETIME),
        ('nFileSizeHigh', DWORD),
        ('nFileSizeLow', DWORD),
        ('dwReserved0', DWORD),
        ('dwReserved1', DWORD),
        ('cFileName', WCHAR * MAX_PATH),
        ('cAlternateFileName', WCHAR * 14),
        ('dwFileType', DWORD),
        ('dwCreatorType', DWORD),
        ('wFinderFlags', WORD)
    ]


WIN32_FIND_DATAW = _WIN32_FIND_DATAW
PWIN32_FIND_DATAW = POINTER(_WIN32_FIND_DATAW)
LPWIN32_FIND_DATAW = POINTER(_WIN32_FIND_DATAW)


class IPersistFile(comtypes.IUnknown):
    _methods_ = [
        COMMETHOD(
            [],
            HRESULT,
            'IsDirty',
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Load',
            (['in'], LPCOLESTR, 'pszFileName'),
            (['in'], DWORD, 'dwMode'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Save',
            (['in'], LPCOLESTR, 'pszFileName'),
            (['in'], BOOL, 'fRemember'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SaveCompleted',
            (['in'], LPCOLESTR, 'pszFileName'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetCurFile',
            (['out'], POINTER(LPOLESTR), 'ppszFileName'),
        )

    ]


class IShellLinkW(comtypes.IUnknown):
    _case_insensitive_ = True
    _iid_ = IID_IShellLinkW
    _idlflags_ = []
    _methods_ = [
        COMMETHOD(
            [],
            HRESULT,
            'GetPath',
            (['out'], LPWSTR, 'pszFile'),
            (['in'], INT, 'cch'),
            (['in', 'out'], POINTER(WIN32_FIND_DATAW), 'pfd'),
            (['in'], DWORD, 'fFlags'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetIDList',
            (['out'], POINTER(PIDLIST_ABSOLUTE), 'ppidl'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetIDList',
            (['in'], POINTER(PCIDLIST_ABSOLUTE), 'pidl'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetDescription',
            (['out'], LPWSTR, 'pszName'),
            (['in'], INT, 'cch')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetDescription',
            (['in'], LPCWSTR, 'pszName'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetWorkingDirectory',
            (['out'], LPWSTR, 'pszDir'),
            (['in'], INT, 'cch')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetWorkingDirectory',
            (['in'], LPCWSTR, 'pszDir'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetArguments',
            (['out'], LPWSTR, 'pszArgs'),
            (['in'], INT, 'cch')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetArguments',
            (['in'], LPCWSTR, 'pszArgs'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetHotkey',
            (['out'], POINTER(WORD), 'pwHotkey')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetHotkey',
            (['in'], WORD, 'wHotkey')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetShowCmd',
            (['out'], POINTER(INT), 'piShowCmd')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetShowCmd',
            (['in'], INT, 'iShowCmd')
        ),
        COMMETHOD(
            [],
            HRESULT,
            'GetIconLocation',
            (['out'], LPWSTR, 'pszIconPath'),
            (['in'], INT, 'cch'),
            (['out'], POINTER(INT), 'piIcon'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetIconLocation',
            (['in'], LPCWSTR, 'pszIconPath'),
            (['in'], INT, 'iIcon'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetRelativePath',
            (['in'], LPCWSTR, 'pszPathRel'),
            (['in'], DWORD, 'dwReserved'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'Resolve',
            (['in'], HWND, 'hwnd'),
            (['in'], DWORD, 'fFlags'),
        ),
        COMMETHOD(
            [],
            HRESULT,
            'SetPath',
            (['in'], LPCWSTR, 'pszFile'),
        ),
    ]


class ShellCoreObjectsLib(object):
    name = 'ShellCoreObjectsLib'
    _reg_typelib_ = (LIBID_ShellCoreObjects, 1, 0)


class ShellLink(comtypes.CoClass):
    _reg_clsid_ = CLSID_ShellLink
    _idlflags_ = []
    _reg_typelib_ = (LIBID_ShellCoreObjects, 1, 0)
    _com_interfaces_ = [IShellLinkW]


IID_IPersistFile = GUID("{0000010B-0000-0000-C000-000000000046}")


def UpdateStartupShortcut(create):
    if os.path.exists(PATH):
        os.remove(PATH)

    if create:
        if not os.path.exists(os.path.split(PATH)[0]):
            os.makedirs(os.path.split(PATH)[0])

        comtypes.CoInitialize()
        shell_link = comtypes.CoCreateInstance(
            CLSID_ShellLink,
            ShellLink,
            CLSCTX_INPROC_SERVER
        )

        shell_link.SetPath(os.path.abspath(sys.executable))
        shell_link.SetDescription('')
        shell_link.SetArguments("-h -e OnInitAfterBoot")
        shell_link.SetWorkingDirectory(os.path.dirname(os.path.abspath(sys.executable)))
        shell_link.SetIconLocation('', 0)
        persist = shell_link.QueryInterface(IPersistFile, IID_IPersistFile)
        persist.Save(PATH, 1)
        comtypes.CoUninitialize()
