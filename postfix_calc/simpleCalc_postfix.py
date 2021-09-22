import sys

from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
# from postfix import *

form_class=loadUiType("SimpleCalc.ui")[0]

class CalcClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        nums = [self.b0, self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8, self.b9]
        for number in nums:
            number.clicked.connect(self.Nums)
        self.bDel.clicked.connect(self.bDelClick)
        self.bClear.clicked.connect(self.bClearClick)
        self.bRun.clicked.connect(self.bRunClick)
        self.bPlus.clicked.connect(self.bPlusClick)
        self.bMinus.clicked.connect(self.bMinusClick)
        self.bMult.clicked.connect(self.bMultClick)
        self.bDivide.clicked.connect(self.bDevideClick)
        self.bDot.clicked.connect(self.bDotClick)
        self.bleft.clicked.connect(self.bleftClick)
        self.bright.clicked.connect(self.brightClick)
        self.bSpace.clicked.connect(self.bSpaceClick)
        self.bRun.clicked.connect(self.bRunClick)
        self.bCaution.clicked.connect(self.bCautionClick)


    def Nums(self):
        global num
        sender = self.sender()
        newNum = int(sender.text())
        setNum = str(newNum)
        if self.result.text() == "0":
            self.result.setText(setNum)
        else:
            self.result.setText(self.result.text()+setNum)

    def bDotClick(self):
        self.result.setText(self.result.text()+".")
    def bPlusClick(self):
        self.result.setText(self.result.text()+"+")
    def bMinusClick(self):
        self.result.setText(self.result.text()+"-")
    def bDevideClick(self):
        self.result.setText(self.result.text()+"/")
    def bMultClick(self):
        self.result.setText(self.result.text()+"*")
    def bleftClick(self):
        self.result.setText(self.result.text()+"(")
    def brightClick(self):
        self.result.setText(self.result.text()+")")
    def bSpaceClick(self):
        self.result.setText(self.result.text()+" ")

    def bCautionClick(self):
        QMessageBox.information(self, "How to Use", "1. 모든 숫자와 연산자(+,-,*,/,(,)) 사이에는 띄어쓰기를 해야합니다. "
                                                    "ex : 12 + 5"
                                                    " 2.처음에 괄호를 사용하고 싶으면 0을 지우고 사용해야 합니다. ")

    def bDelClick(self):
        n=len(self.result.text())
        self.result.setText(self.result.text()[0:n-1])

    def bClearClick(self):
        self.result.setText("0")

    def bRunClick(self):
        in_num = self.result.text().split()
        operator = ["+", "-", "*", "/", "(", ")"]
        postfix = []
        stack = []

        def operator_num(n):  # 기호에 따른 우선 순위 파악을 위한 함수
            if n == "+" or n == "-":
                return 1
            elif n == "(":
                return 3
            elif n == ")":
                return 4
            else:
                return 2

        def add(num1, num2):
            return num1 + num2

        def minus(num1, num2):
            return num2 - num1

        def multi(num1, num2):
            return num1 * num2

        def divide(num1, num2):
            return num2 / num1

        def post_fix(*args):  # 중위식을 넣어서 후위식으로 변경한다.

            for arg in args:

                if arg not in operator:  # 리스트한 식에서 숫자와 기호를 분류하고 숫자는 정수로 변환한다.

                    arg = int(arg)
                    postfix.append(arg)  # 후위식을 나타내기 위한 리스트에 저장한다.

                else:  # 여기서 부터는 기호들만 상대한다.
                    if len(stack) == 0:  # 기호들을 후위식으로 나타내기 위한 stack리스트에 아무것도 없을시 저장한다.
                        stack.append(arg)

                    else:
                        operator_value = operator_num(arg)  # 새로 들어오는 기호와 스택에 있는 기호 비교위한 함수를 사용
                        stack_value = operator_num(stack[-1])  # 스택의 값을 비교위해 변환한다.

                        if operator_value > stack_value:  # 들어오는 기호의 우선순위가 스택에 있는 기호보다 높을 경우
                            if operator_value == 4:
                                while True:
                                    postfix.append(stack.pop())
                                    if stack[-1] == "(":
                                        stack.pop()
                                        break

                            else:
                                stack.append(arg)  # 스택에 그대로 저장한다.


                        elif operator_value < stack_value:  # 들어오는 기호의 우선순위가 스택의 기호보다 낮을 경우
                            if stack[-1] == '(':
                                stack.append(arg)
                            else:
                                while len(stack) > 0:  # 스택의 값을 전부 꺼내기 위함이다.
                                    if stack[-1] == 3:
                                        break
                                    postfix.append(stack.pop())  # 스택의 값들을 후위식에 스택식으로 쌓는다.
                                stack.append(arg)  # 스택에는 우선 순위 낮은 값이 들어간다.


                        elif operator_value == stack_value:  # 들어오는 기호와 스택 기호의 우선 순위가 같을 경우
                            if stack_value == 3:
                                stack.append(arg)
                            else:
                                postfix.append((stack.pop()))  # 스택을 제거하고 후위식에 넣는다.
                                stack.append(arg)

            while len(stack) > 0:  # 남은 스택을 전부 끄집어 낸다
                postfix.append(stack.pop())

            return postfix

        def calculator_function(*args):  # 계산하는 함수

            while len(postfix) > 1:  # 후위식이 결과 하나만 나올때까지만 반복한다.

                for operate in args:

                    if operate in operator:  # 연산 기호 여부 확인한다.
                        arg_index = postfix.index(operate)  # 후위식에서 연산기호의 위치를 특정한다.
                        # print("후위식: ", end='') #줄바꿈 캔슬
                        # print(postfix)
                        # 연산기호기준 앞의 두 숫자를 계산한다.

                        if operate == "+":
                            postfix.pop(arg_index)  # 후위식에서 기호를 제거한다.
                            result = add(postfix.pop(arg_index - 1), postfix.pop(arg_index - 2))
                            # 기호 앞의 두 숫자들을 제거함과 동시에 두 숫자를 계산한다.
                            # 단 pop는 제거 하는 기능이므로 1,2 순서가 되어야 한다.
                            postfix.insert(arg_index - 2, result)  # 결과가 나온 숫자를 후위식에 옳은 위치에 삽입

                        elif operate == "-":
                            postfix.pop(arg_index)
                            result = minus(postfix.pop(arg_index - 1), postfix.pop(arg_index - 2))
                            postfix.insert(arg_index - 2, result)

                        elif operate == "*":
                            postfix.pop(arg_index)
                            result = multi(postfix.pop(arg_index - 1), postfix.pop(arg_index - 2))
                            postfix.insert(arg_index - 2, result)

                        elif operate == "/":
                            postfix.pop(arg_index)
                            result = divide(postfix.pop(arg_index - 1), postfix.pop(arg_index - 2))
                            postfix.insert(arg_index - 2, result)

                    else:
                        continue

            return postfix.pop()

        (post_fix(*in_num))
        self.result.setText(str(calculator_function(*postfix)))

app=QApplication(sys.argv)
myWindow=CalcClass(None)
myWindow.show()
app.exec_()
