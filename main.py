from tkinter import *
import random as r
import os

if os.getcwd() != os.path.dirname(os.path.realpath(__file__)):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

ticWin = Tk()
ticWin.title('TicTacToe')
ticWin.iconphoto(False, PhotoImage(file='./assets/TicTacToe/logo.png'))
buttons = {}
buttonOrder = [[], [], []]
players = ['X', 'O']
playerIm = {}
gameOver = False
for i in ['X', 'O', 'P']:
    playerIm[i] = PhotoImage(file=f'./assets/TicTacToe/{i}.png')


def gameEnd(p: str = 'P'):
    global gameOver
    gameOver = True
    for i in buttons:
        buttons[i].configure(state=DISABLED)
    winWin = Toplevel(ticWin)
    winWin.geometry('300x200')

    winnerL = Label(winWin, image=playerIm[p])
    resultl = Label(winWin, font=('Arial Bold', 10),
                    text=(('BOT' if p in 'O' else 'PLAYER') + ' WINS!' if p not in 'P' else "It's a DRAW!"))

    winnerL.pack()
    resultl.pack()
    if p not in 'P':
        print(p, 'WINS!')
    else:
        print('It is a DRAW!')


def checkRows(p: str) -> tuple[dict, list]:
    end = {}
    vals = []
    for row in range(len(buttonOrder)):
        end[tuple(buttonOrder[row])] = buttonOrder[row].count(p) == len(buttonOrder[row])
        vals.append((buttonOrder[row].count(p), [n for n in buttonOrder[row] if n not in players]))
    return end, vals


def checkColumns(p: str) -> tuple[dict, list]:
    end = {}
    vals = []
    for column in range(len(buttonOrder[0])):
        col = []
        for row in range(len(buttonOrder)):
            col.append(buttonOrder[row][column])
        end[tuple(col)] = col.count(p) == len(buttonOrder)
        vals.append((col.count(p), [n for n in col if n not in players]))
    return end, vals


def checkDiagonals(p: str) -> tuple[dict, list]:
    end = {}
    vals = []
    for l in [[(buttonOrder[i][i]) for i in range(3)], [(buttonOrder[len(buttonOrder) - 1 - i][i]) for i in range(3)]]:
        end[tuple(l)] = l.count(p) == len(buttonOrder)
        vals.append((l.count(p), [n for n in l if n not in players]))
    return end, vals


def check() -> bool:
    for p in players:
        for check in [checkRows(p), checkColumns(p), checkDiagonals(p)]:
            for ret in check[0].values():
                if ret:
                    gameEnd(p)
                    return (True)
    return (False)


def bot() -> bool:
    checks = lambda i, p: [c[i] for c in [checkRows(p), checkColumns(p), checkDiagonals(p)]]
    av = []
    for c in checks(1, players[0]):
        for check in c:
            if check[0] == 0 and len(check[1]) == 1:
                play(check[1][0], players[1])
                return (True)
            if check[0] == 2 and len(check[1]) > 0:
                av.append(check[1][0])

    if len(av) > 0:
        play(r.choice(av), players[1])
        return True

    for c in [checks(1, players[0]), checks(1, players[1])]:
        for check in c:
            if len(check[0]) >= 1: av.extend(check[1][1])
    bs = {}
    for n in av:
        if n not in bs.keys(): bs[n] = av.count(n)
    try:
        play(r.choice([k for k, v in bs.items() if v == max(bs.values())]), players[1])
    except IndexError:
        gameEnd()
    return (True)


def play(bnum: int, player: str) -> None:
    buttons[bnum].configure(state=DISABLED, image=playerIm[str(player).upper()])
    buttonOrder[(bnum - 1) // 3][bnum % 3 - 1] = str(player)

    if not (check() or gameOver) and player == players[0]:
        bot()


for i in range(9):
    buttons[i + 1] = Button(ticWin, width=120, height=120, borderwidth=5, image=playerIm['P'],
                            command=lambda i=i: play(i + 1, players[0]))
    buttons[i + 1].grid(row=i // 3, column=i % 3, columnspan=1)
    buttonOrder[i // 3].append(i + 1)

ticWin.mainloop()
