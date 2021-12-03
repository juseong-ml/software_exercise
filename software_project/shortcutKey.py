from pynput.keyboard import Key, Listener, KeyCode
import win32api
# from gui import front
import DnDDemo3 as dd
import sys

from TkinterDnD2 import *



#단축키 정하기

store = set()

HOT_KEYS = {
    'print_hello': set([Key.alt_l, KeyCode(char='1')]),
    'open_notepad': set([Key.alt_l, KeyCode(char='2')]),
    # 'open_gui' : set([Key.alt_l, KeyCode(char='s')])
    'makeTag' : set([Key.alt_l, KeyCode(char='t')])
}


def print_hello():
    print('hello, World!!!')

#
def makeTag():
    try:
        dd.main()
    except Exception as err:
        print(err)

def open_notepad():
    print('open_notepad')
    try:
        win32api.WinExec('notepad.exe')
    except Exception as err:
        print(err)
#
# def open_gui():
#     try:
#         front()
#     except Exception as err:
#         print(err)

def handleKeyPress(key, **kwargs):
    store.add(key)


def handleKeyRelease(key):
    for action, trigger in HOT_KEYS.items():
        CHECK = all([True if triggerKey in store else False for triggerKey in trigger])

        if CHECK:
            try:
                action = eval(action)
                if callable(action):
                    action()
            except NameError as err:
                print(err)

    # 종료
    if key == Key.esc:
        return False
    elif key in store:
        store.remove(key)


with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
    listener.join()
