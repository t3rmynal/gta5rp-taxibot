import sys
import os
import time
import winsound
import threading
from PIL import ImageGrab
import pyautogui
from colorama import init, Fore, Style

init(autoreset=True)

pyautogui.FAILSAFE = False

# ---- настройки ----
TARGET_COLOR = (0x30, 0x43, 0x68)  # цвет
TOLERANCE    = 5                    
REGION       = (1120, 350, 1350, 900)  # область скрина
POLL_DELAY   = 0.001               

LOGO = r"""
  _   ____                                   _
 | | |___ \                                 | |
 | |_  __) |_ __ _ __ ___  _   _ _ __   __ _| |
 | __||__ <| '__| '_ ` _ \| | | | '_ \ / _` | |
 | |_ ___) | |  | | | | | | |_| | | | | (_| | |
  \__|____/|_|  |_| |_| |_|\__, |_| |_|\__,_|_|
                            __/ |
                           |___/
"""

BANNER = """\
  ╔══════════════════════════════╗
  ║      GTA5RP  -  TaxiBot      ║
  ║   by t3rmynal  |  python     ║
  ╚══════════════════════════════╝"""


def play_sound():
    # звук принятия вызова
    for freq, ms in [(880, 90), (1046, 90), (1318, 220)]:
        winsound.Beep(freq, ms)


def find_color():
    # скриншот
    img = ImageGrab.grab(bbox=REGION)
    px  = img.load()
    w, h = img.size
    tr, tg, tb = TARGET_COLOR
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y][:3]
            if abs(r - tr) < TOLERANCE and \
               abs(g - tg) < TOLERANCE and \
               abs(b - tb) < TOLERANCE:
                return REGION[0] + x, REGION[1] + y
    return None


def move_and_click(x, y):
    pyautogui.moveTo(x, y, duration=0.05)
    pyautogui.click()


def run_bot():
    print(Fore.YELLOW + "  >> запущен, жду вызов...")
    print(Fore.CYAN   + "  >> ctrl+c чтобы остановить\n")

    frames = ["|", "/", "-", "\\"]
    i = 0
    start = time.time()

    while True:
        result = find_color()
        if result:
            x, y = result
            move_and_click(x, y)
            threading.Thread(target=play_sound, daemon=True).start()
            elapsed = time.time() - start
            print(Fore.GREEN + f"\r  [+] вызов принят! позиция ({x}, {y})  время ожидания: {elapsed:.1f}с      ")
            return

        elapsed = time.time() - start
        print(Fore.WHITE + f"\r  {frames[i % 4]}  сканирую...  [{elapsed:.0f}с]", end="", flush=True)
        i += 1
        time.sleep(POLL_DELAY)


def print_header():
    os.system("cls")
    print(Fore.CYAN   + LOGO)
    print(Fore.YELLOW + BANNER + "\n")


def main():
    print_header()

    while True:
        print(Fore.WHITE  + "  [1]  запустить бота")
        print(Fore.WHITE  + "  [2]  выйти\n")
        print(Fore.CYAN   + "  >  ", end="")

        try:
            choice = input().strip()
        except (KeyboardInterrupt, EOFError):
            break

        if choice == "1":
            print()
            try:
                run_bot()
            except KeyboardInterrupt:
                print(Fore.RED + "\r  >> остановлен                              ")

            print(Fore.WHITE + "\n  enter чтобы вернуться в меню...")
            try:
                input()
            except (KeyboardInterrupt, EOFError):
                pass

            print_header()

        elif choice == "2":
            break

    print(Fore.RED + "\n  пока!\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
