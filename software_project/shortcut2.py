from pynput.keyboard import Key, Listener, KeyCode
import win32api
##단축키를 정하자
MY_HOT_KEYS = [
    {"function1": {Key.alt_l, KeyCode(char="n") }}
    ##ctrl + alt + n
]

##기존의 키가 눌려져있었다는 사실을 알아야하기에
##집합으로 만들어야함 키를 누르고있으면 계속 pressed에 걸리기떄문에
##그래서 집합을 사용함
current_keys = set()

def function1():
    print("함수1 호출")
    win32api.WinExec("cacl.exe")

def key_pressed(key):
    print("pressd {}".format(key))
    for data in MY_HOT_KEYS:
        ##딕셔너리 형태로 오기때문에 리스트로 캐스팅
        FINCTION = list(data.keys())[0]
        KEYS = list(data.values())[0]

        if key in KEYS:
            current_keys.add(key)

            if all(k in current_keys for k in KEYS):  ##좀 더 고급스럽게 표현하자면

            # checker = True
            # for k in KEYS:
            #     ##3개가 다있는지 확인하는 것
            #     if k not in current_keys:
            #         ##단축키 동작하면 X
            #         checker=False
            #         break
            # if checker:
                function = eval(FUNCTION)
                function()


def key_released(key):
    print("Released {}".format(key))

    if key in current_keys:
        current_keys.clear()
        current_keys.remove(key)


    if key == Key.esc:
        return False

##Listener은 win32.py에 윈도우용 api 함수를 랩핑해놓은 것
with Listener(on_press=key_pressed, on_releasde=key_released) as listener:
    listener.join() ##쓰레드로 쓴다.