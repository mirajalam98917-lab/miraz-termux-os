#!/usr/bin/env python3

import os
import sys
import json
import time
import math
import random
import shutil
import hashlib
import socket
import platform
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime, date

# ============================================================
#                    M I R A Z   O S
#                       v5.0
#                 4D STYLE TOOLBOX
# ============================================================

BASE = os.path.expanduser("~/miraz-termux-os")
DATA = os.path.join(BASE, "data")
os.makedirs(DATA, exist_ok=True)

EXPENSES = os.path.join(DATA, "expenses.json")
TODOS = os.path.join(DATA, "todos.json")
NOTES = os.path.join(DATA, "notes.txt")
REMINDERS = os.path.join(DATA, "reminders.json")
CLIPBOARD = os.path.join(DATA, "clipboard.txt")
PLANNER = os.path.join(DATA, "planner.json")
BUDGET = os.path.join(DATA, "budget.json")

# ---------------- COLORS ----------------

R = "\033[0m"
B = "\033[1m"
DIM = "\033[2m"

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"

# ============================================================
#                         HELPERS
# ============================================================

def clear():
    os.system("clear")


def pause():
    input(f"\n{DIM}ENTER dabao...{R}")


def load(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return default


def save(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(RED + f"Save error: {e}" + R)


def now():
    return datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")


def beep():
    print("\a", end="")


def line():
    print(CYAN + "═" * 62 + R)


def header(text):
    print()
    line()
    print(CYAN + B + text.center(62) + R)
    line()


# ============================================================
#                    3D / 4D MIRAZ LOGO
# ============================================================

def logo():

    art = [
        "███╗   ███╗██╗██████╗  █████╗ ███████╗",
        "████╗ ████║██║██╔══██╗██╔══██╗╚══███╔╝",
        "██╔████╔██║██║██████╔╝███████║  ███╔╝ ",
        "██║╚██╔╝██║██║██╔══██╗██╔══██║ ███╔╝  ",
        "██║ ╚═╝ ██║██║██║  ██║██║  ██║███████╗",
        "╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝"
    ]

    print(CYAN + B)

    for i, x in enumerate(art):
        print(" " * 3 + x)
        if i == 1:
            print(DIM + " " * 5 + "░▒▓█ SHADOW LAYER █▓▒░" + R)

    print()
    print(MAGENTA + B + "              M I R A Z   O S" + R)
    print(YELLOW + "              4D DAILY TOOLBOX" + R)
    print()


def screen(title):
    clear()
    logo()
    header(title)


# ============================================================
#                     STARTUP ANIMATION
# ============================================================

def startup():

    clear()

    print(CYAN + B)

    print("""
███╗   ███╗██╗██████╗  █████╗ ███████╗
████╗ ████║██║██╔══██╗██╔══██╗╚══███╔╝
██╔████╔██║██║██████╔╝███████║  ███╔╝
██║╚██╔╝██║██║██╔══██╗██╔══██║ ███╔╝
██║ ╚═╝ ██║██║██║  ██║██║  ██║███████╗
╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
""")

    print(MAGENTA + "              4D DAILY TOOLBOX" + R)
    print()

    for i in range(31):
        bar = "█" * i + "░" * (30-i)
        print(
            "\r" + CYAN +
            f" BOOTING [ {bar} ] {i*100//30}%"
            + R,
            end="",
            flush=True
        )
        time.sleep(0.025)

    print()
    print(GREEN + "✓ MIRAZ CORE ONLINE" + R)
    print(GREEN + "✓ LOCAL DATA READY" + R)
    print(GREEN + "✓ 49 TOOL MODULES READY" + R)

    time.sleep(.6)


# ============================================================
#                    1. EXPENSE TRACKER
# ============================================================

def expense_tracker():

    while True:
        screen("💰 EXPENSE TRACKER")

        print("""
1. Add Expense
2. View Expenses
3. Delete Expense
4. Total Spending
0. Back
""")

        c = input("MIRAZ > ")

        data = load(EXPENSES, [])

        if c == "1":

            name = input("Expense name: ")

            try:
                amount = float(input("Amount ₹: "))
            except:
                print(RED + "Invalid amount." + R)
                pause()
                continue

            category = input("Category: ") or "Other"

            data.append({
                "name": name,
                "amount": amount,
                "category": category,
                "date": now()
            })

            save(EXPENSES, data)
            print(GREEN + "✓ Saved" + R)
            pause()

        elif c == "2":

            if not data:
                print(YELLOW + "No expenses." + R)

            for i, x in enumerate(data, 1):
                print(
                    f"{i}. {x['name']} | ₹{x['amount']:.2f} | "
                    f"{x['category']} | {x['date']}"
                )

            pause()

        elif c == "3":

            for i, x in enumerate(data, 1):
                print(f"{i}. {x['name']} ₹{x['amount']}")

            try:
                n = int(input("Delete: "))
                data.pop(n-1)
                save(EXPENSES, data)
                print(GREEN + "✓ Deleted" + R)
            except:
                print(RED + "Invalid." + R)

            pause()

        elif c == "4":

            total = sum(float(x["amount"]) for x in data)

            print(
                GREEN +
                f"\nTotal Spending: ₹{total:.2f}"
                + R
            )

            pause()

        elif c == "0":
            return


# ============================================================
#                 2. MONTHLY EXPENSE SUMMARY
# ============================================================

def monthly_summary():

    screen("📊 MONTHLY EXPENSE SUMMARY")

    data = load(EXPENSES, [])
    month = datetime.now().strftime("%Y-%m")

    current = [
        x for x in data
        if x.get("date", "").startswith(
            datetime.now().strftime("%d-%m-%Y")[:0]
        )
    ]

    total = 0
    categories = {}

    for x in data:

        try:
            d = datetime.strptime(
                x["date"],
                "%d-%m-%Y %I:%M:%S %p"
            )

            if d.strftime("%Y-%m") == month:

                amount = float(x["amount"])
                total += amount

                cat = x["category"]
                categories[cat] = categories.get(cat, 0) + amount

        except:
            pass

    print(f"\nThis month: {datetime.now().strftime('%B %Y')}")
    print(GREEN + f"Total: ₹{total:.2f}" + R)

    if categories:
        print("\nCategories:")

        for k, v in categories.items():
            print(f"  {k:<15} ₹{v:.2f}")

    pause()


# ============================================================
#                    3. BUDGET CALCULATOR
# ============================================================

def budget_calculator():

    screen("💵 BUDGET CALCULATOR")

    try:
        income = float(input("Monthly income ₹: "))
        expenses = float(input("Monthly expenses ₹: "))

        remaining = income - expenses
        saving = (remaining / income) * 100 if income else 0

        print(f"\nIncome    : ₹{income:.2f}")
        print(f"Expenses  : ₹{expenses:.2f}")
        print(
            GREEN +
            f"Remaining : ₹{remaining:.2f}"
            + R
        )
        print(f"Savings % : {saving:.2f}%")

    except:
        print(RED + "Invalid input." + R)

    pause()


# ============================================================
#                     CALCULATOR CENTER
# ============================================================

def calculators():

    while True:

        screen("🧮 CALCULATOR CENTER")

        print("""
1. Normal Calculator
2. Percentage
3. Discount
4. Profit / Loss
5. EMI
6. Simple Interest
7. Compound Interest
8. Average
9. Ratio
10. Unit Converter
0. Back
""")

        c = input("MIRAZ > ")

        try:

            if c == "1":

                exp = input("Example: 25*4+10 = ")

                allowed = "0123456789+-*/().% "

                if not all(ch in allowed for ch in exp):
                    raise ValueError

                result = eval(
                    exp,
                    {"__builtins__": {}},
                    {}
                )

                print(GREEN + f"Result = {result}" + R)
                pause()

            elif c == "2":

                a = float(input("Value: "))
                b = float(input("Percent: "))

                print(
                    GREEN +
                    f"Result = {a*b/100:.2f}"
                    + R
                )

                pause()

            elif c == "3":

                price = float(input("Price: "))
                d = float(input("Discount %: "))

                save_amt = price*d/100
                final = price-save_amt

                print(f"Discount: ₹{save_amt:.2f}")
                print(GREEN + f"Final: ₹{final:.2f}" + R)

                pause()

            elif c == "4":

                cp = float(input("Cost price: "))
                sp = float(input("Selling price: "))

                if sp > cp:
                    print(
                        GREEN +
                        f"Profit = ₹{sp-cp:.2f}"
                        + R
                    )
                elif cp > sp:
                    print(
                        RED +
                        f"Loss = ₹{cp-sp:.2f}"
                        + R
                    )
                else:
                    print("No profit / loss.")

                pause()

            elif c == "5":

                p = float(input("Loan amount: "))
                annual = float(input("Annual interest %: "))
                years = float(input("Years: "))

                r = annual / 12 / 100
                n = years * 12

                if r == 0:
                    emi = p/n
                else:
                    emi = p*r*(1+r)**n/((1+r)**n-1)

                print(
                    GREEN +
                    f"Monthly EMI = ₹{emi:.2f}"
                    + R
                )

                pause()

            elif c == "6":

                p = float(input("Principal: "))
                r = float(input("Rate %: "))
                t = float(input("Years: "))

                si = p*r*t/100

                print(
                    GREEN +
                    f"Interest = ₹{si:.2f}"
                    + R
                )

                pause()

            elif c == "7":

                p = float(input("Principal: "))
                r = float(input("Rate %: "))
                t = float(input("Years: "))

                amount = p*(1+r/100)**t

                print(f"Amount: ₹{amount:.2f}")
                print(
                    GREEN +
                    f"Interest: ₹{amount-p:.2f}"
                    + R
                )

                pause()

            elif c == "8":

                nums = [
                    float(x)
                    for x in input(
                        "Numbers separated by space: "
                    ).split()
                ]

                print(
                    GREEN +
                    f"Average = {sum(nums)/len(nums):.2f}"
                    + R
                )

                pause()

            elif c == "9":

                a = float(input("First number: "))
                b = float(input("Second number: "))

                g = math.gcd(int(a), int(b))

                print(
                    GREEN +
                    f"Ratio = {int(a)//g}:{int(b)//g}"
                    + R
                )

                pause()

            elif c == "10":
                unit_converter()

            elif c == "0":
                return

        except Exception:
            print(RED + "Invalid input." + R)
            pause()


# ============================================================
#                    UNIT CONVERTER
# ============================================================

def unit_converter():

    screen("📏 UNIT CONVERTER")

    print("""
1. Kilometers → Miles
2. Miles → Kilometers
3. Kilograms → Pounds
4. Pounds → Kilograms
5. Celsius → Fahrenheit
6. Fahrenheit → Celsius
7. Meters → Feet
8. Feet → Meters
""")

    c = input("Select: ")

    try:

        x = float(input("Value: "))

        if c == "1":
            result = x * 0.621371
        elif c == "2":
            result = x / 0.621371
        elif c == "3":
            result = x * 2.20462
        elif c == "4":
            result = x / 2.20462
        elif c == "5":
            result = x*9/5+32
        elif c == "6":
            result = (x-32)*5/9
        elif c == "7":
            result = x*3.28084
        elif c == "8":
            result = x/3.28084
        else:
            return

        print(GREEN + f"\nResult: {result:.4f}" + R)

    except:
        print(RED + "Invalid." + R)

    pause()


# ============================================================
#                      STUDY TOOLS
# ============================================================

def study_timer():

    screen("📚 STUDY TIMER")

    try:
        minutes = int(input("Minutes: "))

        if minutes <= 0:
            raise ValueError

        seconds = minutes*60

        while seconds:

            m = seconds//60
            s = seconds%60

            print(
                f"\r⏱️  {m:02d}:{s:02d}",
                end="",
                flush=True
            )

            time.sleep(1)
            seconds -= 1

        beep()

        print(
            "\n" +
            GREEN +
            "🎉 Study session complete!"
            + R
        )

    except:
        print(RED + "Invalid." + R)

    pause()


def stopwatch():

    screen("⏱️ STOPWATCH")

    input("ENTER = Start")
    start = time.time()

    input("ENTER = Stop")

    elapsed = time.time()-start

    print(
        GREEN +
        f"\nTime: {elapsed:.2f} seconds"
        + R
    )

    pause()


def marks():

    screen("📊 MARKS & PERCENTAGE")

    try:

        subjects = int(input("Number of subjects: "))
        total = 0
        obtained = 0

        for i in range(subjects):

            x = float(input(f"Subject {i+1} marks: "))
            obtained += x

        maximum = subjects*100
        percentage = obtained/maximum*100

        print(f"\nObtained: {obtained}/{maximum}")
        print(
            GREEN +
            f"Percentage: {percentage:.2f}%"
            + R
        )

    except:
        print(RED + "Invalid." + R)

    pause()


def exam_countdown():

    screen("🎯 EXAM COUNTDOWN")

    try:

        text = input(
            "Exam date YYYY-MM-DD: "
        )

        target = datetime.strptime(
            text,
            "%Y-%m-%d"
        ).date()

        today = date.today()
        days = (target-today).days

        if days > 0:
            print(
                GREEN +
                f"\n🔥 {days} days remaining!"
                + R
            )
        elif days == 0:
            print(YELLOW + "\nExam is TODAY!" + R)
        else:
            print("Exam date has passed.")

    except:
        print(RED + "Invalid date." + R)

    pause()


def study_notes():

    screen("📝 STUDY NOTES")

    subject = input("Subject: ")
    text = input("Note: ")

    path = os.path.join(
        DATA,
        "study_notes.txt"
    )

    with open(path, "a", encoding="utf-8") as f:
        f.write(
            f"\n[{now()}] {subject}\n{text}\n"
        )

    print(GREEN + "✓ Study note saved." + R)

    pause()


def study_checklist():

    screen("✅ STUDY CHECKLIST")

    items = load(
        os.path.join(DATA, "study_checklist.json"),
        []
    )

    print("""
1. Add topic
2. Show topics
3. Mark completed
0. Back
""")

    c = input("Select: ")

    if c == "1":

        x = input("Topic: ")

        items.append({
            "topic": x,
            "done": False
        })

        save(
            os.path.join(DATA, "study_checklist.json"),
            items
        )

    elif c == "2":

        for i, x in enumerate(items, 1):

            status = "✓" if x["done"] else "○"

            print(
                f"{i}. {status} {x['topic']}"
            )

        pause()

    elif c == "3":

        for i, x in enumerate(items, 1):
            print(f"{i}. {x['topic']}")

        try:
            n = int(input("Complete: "))
            items[n-1]["done"] = True

            save(
                os.path.join(DATA, "study_checklist.json"),
                items
            )

        except:
            pass


def daily_planner():

    screen("📅 DAILY STUDY PLANNER")

    data = load(PLANNER, {})

    today = date.today().isoformat()

    print("Today's plan:\n")

    for i in range(1, 6):

        task = input(
            f"{i}. Subject / Task: "
        )

        if task:
            data.setdefault(today, []).append(task)

    save(PLANNER, data)

    print(GREEN + "\n✓ Plan saved." + R)
    pause()


# ============================================================
#                     PRODUCTIVITY
# ============================================================

def notes_manager():

    while True:

        screen("📝 NOTES MANAGER")

        print("""
1. Add Note
2. Read Notes
3. Clear Notes
0. Back
""")

        c = input("Select: ")

        if c == "1":

            text = input("Note: ")

            with open(NOTES, "a", encoding="utf-8") as f:
                f.write(
                    f"[{now()}]\n{text}\n\n"
                )

            print(GREEN + "✓ Saved." + R)
            pause()

        elif c == "2":

            if os.path.exists(NOTES):

                with open(
                    NOTES,
                    encoding="utf-8"
                ) as f:
                    print(f.read())

            else:
                print("No notes.")

            pause()

        elif c == "3":

            if input("Type YES to clear: ") == "YES":

                open(
                    NOTES,
                    "w",
                    encoding="utf-8"
                ).close()

                print(GREEN + "✓ Cleared." + R)

            pause()

        elif c == "0":
            return


def todo_manager():

    while True:

        screen("✅ TO-DO MANAGER")

        tasks = load(TODOS, [])

        print("""
1. Add
2. Show
3. Complete
4. Delete
0. Back
""")

        c = input("Select: ")

        if c == "1":

            text = input("Task: ")

            tasks.append({
                "task": text,
                "done": False
            })

            save(TODOS, tasks)

        elif c == "2":

            for i, x in enumerate(tasks, 1):

                status = "✓" if x["done"] else "○"

                print(
                    f"{i}. {status} {x['task']}"
                )

            pause()

        elif c == "3":

            try:
                n = int(input("Task number: "))
                tasks[n-1]["done"] = True
                save(TODOS, tasks)
            except:
                pass

        elif c == "4":

            try:
                n = int(input("Delete number: "))
                tasks.pop(n-1)
                save(TODOS, tasks)
            except:
                pass

        elif c == "0":
            return


def reminder_list():

    screen("🔔 REMINDER LIST")

    data = load(REMINDERS, [])

    print("""
1. Add Reminder
2. View Reminders
0. Back
""")

    c = input("Select: ")

    if c == "1":

        text = input("Reminder: ")

        data.append({
            "text": text,
            "created": now()
        })

        save(REMINDERS, data)

        print(GREEN + "✓ Reminder saved." + R)

    elif c == "2":

        for i, x in enumerate(data, 1):
            print(
                f"{i}. {x['text']} "
                f"({x['created']})"
            )

        pause()


def clipboard_saver():

    screen("📋 TEXT CLIPBOARD")

    print("""
1. Save text
2. Read saved text
3. Clear
""")

    c = input("Select: ")

    if c == "1":

        text = input("Text: ")

        with open(
            CLIPBOARD,
            "a",
            encoding="utf-8"
        ) as f:
            f.write(
                f"[{now()}]\n{text}\n\n"
            )

        print(GREEN + "✓ Saved." + R)

    elif c == "2":

        if os.path.exists(CLIPBOARD):

            with open(
                CLIPBOARD,
                encoding="utf-8"
            ) as f:
                print(f.read())

        pause()

    elif c == "3":

        open(
            CLIPBOARD,
            "w",
            encoding="utf-8"
        ).close()

        print(GREEN + "✓ Cleared." + R)
        pause()


def counter():

    screen("🔢 COUNTER")

    count = 0

    print(
        "\nENTER = +1 | d = -1 | r = reset | q = quit"
    )

    while True:

        print(
            f"\rCOUNT: {count} ",
            end="",
            flush=True
        )

        key = input("\n> ").lower()

        if key == "":
            count += 1
        elif key == "d":
            count -= 1
        elif key == "r":
            count = 0
        elif key == "q":
            break


def date_time():

    screen("📅 DATE / TIME")

    print(
        f"""
Date : {datetime.now().strftime('%d %B %Y')}
Day  : {datetime.now().strftime('%A')}
Time : {datetime.now().strftime('%I:%M:%S %p')}
"""
    )

    pause()


# ============================================================
#                       PHONE / SYSTEM
# ============================================================

def system_info():

    screen("⚙️ SYSTEM INFORMATION")

    total, used, free = shutil.disk_usage("/")

    print(
        f"""
OS           : {platform.system()}
Release      : {platform.release()}
Machine      : {platform.machine()}
Architecture : {platform.architecture()[0]}
Python       : {platform.python_version()}

Storage Total: {total/(1024**3):.2f} GB
Storage Used : {used/(1024**3):.2f} GB
Storage Free : {free/(1024**3):.2f} GB

Time         : {now()}
"""
    )

    pause()


def battery_info():

    screen("🔋 BATTERY INFO")

    try:

        p = subprocess.run(
            ["termux-battery-status"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if p.returncode == 0:

            data = json.loads(p.stdout)

            for k, v in data.items():
                print(f"{k:<15}: {v}")

        else:
            print(
                YELLOW +
                "Termux:API available nahi hai."
                + R
            )

    except:

        print(
            YELLOW +
            "Battery API unavailable."
            + R
        )

    pause()


def storage_info():

    screen("💾 STORAGE INFO")

    total, used, free = shutil.disk_usage("/")

    print(
        f"""
Total : {total/(1024**3):.2f} GB
Used  : {used/(1024**3):.2f} GB
Free  : {free/(1024**3):.2f} GB
"""
    )

    pause()


def ram_info():

    screen("🧠 RAM INFO")

    try:

        with open("/proc/meminfo") as f:
            data = f.read()

        values = {}

        for line_ in data.splitlines():

            parts = line_.split()

            if len(parts) >= 2:
                values[parts[0].rstrip(":")] = int(parts[1])

        total = values.get("MemTotal", 0)
        free = values.get("MemAvailable", 0)

        print(
            f"""
RAM Total     : {total/1024:.0f} MB
RAM Available : {free/1024:.0f} MB
RAM Used      : {(total-free)/1024:.0f} MB
"""
        )

    except:
        print("RAM information unavailable.")

    pause()


def android_info():

    screen("📱 ANDROID DEVICE INFO")

    commands = [
        ["getprop", "ro.product.manufacturer"],
        ["getprop", "ro.product.model"],
        ["getprop", "ro.build.version.release"],
        ["getprop", "ro.build.version.sdk"]
    ]

    names = [
        "Manufacturer",
        "Model",
        "Android",
        "SDK"
    ]

    for name, cmd in zip(names, commands):

        try:

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            print(
                f"{name:<15}: "
                f"{result.stdout.strip()}"
            )

        except:
            pass

    pause()


def package_viewer():

    screen("📦 TERMUX PACKAGE VIEWER")

    try:

        result = subprocess.run(
            ["pkg", "list-installed"],
            capture_output=True,
            text=True
        )

        print(result.stdout)

    except:
        print(
            "pkg command unavailable."
        )

    pause()


# ============================================================
#                        FILE TOOLS
# ============================================================

def file_explorer():

    while True:

        screen("📁 FILE EXPLORER")

        path = input(
            "Folder path [ENTER = current]: "
        ).strip()

        if not path:
            path = "."

        if not os.path.isdir(path):
            print(RED + "Folder not found." + R)
            pause()
            continue

        for x in os.listdir(path):

            full = os.path.join(path, x)

            if os.path.isdir(full):
                print(BLUE + "📁 " + x + R)
            else:
                print("📄 " + x)

        pause()

        return


def file_search():

    screen("🔎 FILE SEARCH")

    name = input("Filename contains: ")

    print()

    found = False

    for root, dirs, files in os.walk("."):

        for f in files:

            if name.lower() in f.lower():

                print(
                    os.path.join(root, f)
                )

                found = True

    if not found:
        print(YELLOW + "Nothing found." + R)

    pause()


def file_size():

    screen("📏 FILE SIZE")

    path = input("File path: ")

    if os.path.isfile(path):

        size = os.path.getsize(path)

        print(
            GREEN +
            f"\nBytes : {size}"
            + R
        )

        print(
            f"KB    : {size/1024:.2f}"
        )

        print(
            f"MB    : {size/(1024**2):.2f}"
        )

    else:
        print(RED + "File not found." + R)

    pause()


def text_viewer():

    screen("📄 TEXT FILE VIEWER")

    path = input("Text file: ")

    if not os.path.isfile(path):
        print(RED + "Not found." + R)
        pause()
        return

    try:

        with open(
            path,
            encoding="utf-8",
            errors="replace"
        ) as f:
            print("\n" + f.read())

    except Exception as e:
        print(RED + str(e) + R)

    pause()


def folder_size():

    screen("🗂️ FOLDER SIZE")

    path = input(
        "Folder [ENTER=current]: "
    ).strip() or "."

    total = 0

    for root, dirs, files in os.walk(path):

        for f in files:

            try:
                total += os.path.getsize(
                    os.path.join(root, f)
                )
            except:
                pass

    print(
        GREEN +
        f"\nFolder size: {total/(1024**2):.2f} MB"
        + R
    )

    pause()


def copy_move():

    screen("📋 COPY / MOVE")

    print("""
1. Copy
2. Move
""")

    c = input("Select: ")

    source = input("Source: ")
    destination = input("Destination: ")

    try:

        if c == "1":

            if os.path.isdir(source):
                shutil.copytree(
                    source,
                    destination,
                    dirs_exist_ok=True
                )
            else:
                shutil.copy2(
                    source,
                    destination
                )

            print(GREEN + "✓ Copied." + R)

        elif c == "2":

            shutil.move(
                source,
                destination
            )

            print(GREEN + "✓ Moved." + R)

    except Exception as e:

        print(
            RED +
            f"Error: {e}"
            + R
        )

    pause()


def temp_cleaner():

    screen("🧹 MIRAZ DATA CLEANER")

    print(
        "Ye tool sirf MIRAZ OS ke temporary/cache files ko dekhega."
    )

    cache = os.path.join(
        DATA,
        "cache"
    )

    if not os.path.exists(cache):
        print("\nNo temporary files.")
        pause()
        return

    if input(
        "\nType CLEAN to continue: "
    ) != "CLEAN":
        return

    shutil.rmtree(cache)
    os.makedirs(cache)

    print(GREEN + "✓ MIRAZ temporary data cleaned." + R)

    pause()


# ============================================================
#                       SECURITY TOOLS
# ============================================================

def password_generator():

    import secrets
    import string

    screen("🔐 PASSWORD GENERATOR")

    try:
        length = int(input("Length 4-128: "))

        if not 4 <= length <= 128:
            raise ValueError

    except:
        print(RED + "Invalid length." + R)
        pause()
        return

    chars = (
        string.ascii_letters +
        string.digits +
        "!@#$%^&*_-+="
    )

    password = "".join(
        secrets.choice(chars)
        for _ in range(length)
    )

    print(
        "\n" +
        GREEN +
        password +
        R
    )

    pause()


def pin_generator():

    import secrets

    screen("🔢 RANDOM PIN GENERATOR")

    try:
        length = int(
            input("PIN length 4-12: ")
        )

        if not 4 <= length <= 12:
            raise ValueError

    except:
        print(RED + "Invalid." + R)
        pause()
        return

    pin = "".join(
        str(secrets.randbelow(10))
        for _ in range(length)
    )

    print(
        "\nPIN: " +
        GREEN +
        pin +
        R
    )

    pause()


def sha_text():

    screen("🔒 SHA-256 TEXT HASH")

    text = input("Text: ")

    result = hashlib.sha256(
        text.encode()
    ).hexdigest()

    print(
        "\n" +
        CYAN +
        result +
        R
    )

    pause()


def file_checksum():

    screen("🔒 FILE CHECKSUM")

    path = input("File: ")

    if not os.path.isfile(path):
        print(RED + "File not found." + R)
        pause()
        return

    sha = hashlib.sha256()

    try:

        with open(path, "rb") as f:

            while True:

                chunk = f.read(1024*1024)

                if not chunk:
                    break

                sha.update(chunk)

        print(
            "\nSHA-256:\n" +
            CYAN +
            sha.hexdigest() +
            R
        )

    except Exception as e:
        print(RED + str(e) + R)

    pause()


def password_strength():

    screen("🔍 PASSWORD STRENGTH")

    password = input(
        "Password to test: "
    )

    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(not c.isalnum() for c in password):
        score += 1

    levels = [
        "Very Weak",
        "Weak",
        "Fair",
        "Good",
        "Strong",
        "Very Strong",
        "Excellent"
    ]

    print(
        "\nStrength: " +
        GREEN +
        levels[min(score, 6)] +
        R
    )

    pause()


# ============================================================
#                         CODING TOOLS
# ============================================================

def coding_tools():

    while True:

        screen("💻 CODING CENTER")

        print("""
1. Python Version
2. Python Calculator
3. Random Number
4. Text Case Converter
5. Character Counter
6. JSON Formatter / Validator
0. Back
""")

        c = input("Select: ")

        if c == "1":

            print(
                f"\nPython: {platform.python_version()}"
            )

            pause()

        elif c == "2":

            exp = input(
                "Expression: "
            )

            allowed = "0123456789+-*/().% "

            if all(x in allowed for x in exp):

                try:
                    print(
                        GREEN +
                        f"Result: {eval(exp, {'__builtins__': {}}, {})}"
                        + R
                    )
                except:
                    print(RED + "Invalid." + R)

            else:
                print(RED + "Unsafe expression." + R)

            pause()

        elif c == "3":

            try:

                a = int(input("Minimum: "))
                b = int(input("Maximum: "))

                print(
                    GREEN +
                    f"Random: {random.randint(a,b)}"
                    + R
                )

            except:
                print(RED + "Invalid." + R)

            pause()

        elif c == "4":

            text = input("Text: ")

            print(
                "\nUPPER : " + text.upper()
            )
            print(
                "lower : " + text.lower()
            )
            print(
                "Title : " + text.title()
            )

            pause()

        elif c == "5":

            text = input("Text: ")

            print(
                f"""
Characters : {len(text)}
Words      : {len(text.split())}
Letters    : {sum(c.isalpha() for c in text)}
Numbers    : {sum(c.isdigit() for c in text)}
"""
            )

            pause()

        elif c == "6":

            json_tool()

        elif c == "0":
            return


def json_tool():

    screen("🧹 JSON FORMATTER / VALIDATOR")

    text = input(
        "Paste JSON: "
    )

    try:

        obj = json.loads(text)

        print(
            GREEN +
            "\n✓ Valid JSON\n\n" +
            json.dumps(
                obj,
                indent=4,
                ensure_ascii=False
            )
            + R
        )

    except Exception as e:

        print(
            RED +
            f"\n✗ Invalid JSON\n{e}"
            + R
        )

    pause()


# ============================================================
#                       NETWORK TOOLS
# ============================================================

def network_tools():

    while True:

        screen("🌐 NETWORK CENTER")

        print("""
1. Internet Connectivity
2. Local IP
3. DNS Lookup
4. Network Interfaces
0. Back
""")

        c = input("Select: ")

        if c == "1":

            try:

                urllib.request.urlopen(
                    "https://example.com",
                    timeout=5
                )

                print(
                    GREEN +
                    "\n✓ Internet is reachable."
                    + R
                )

            except:
                print(
                    RED +
                    "\n✗ Internet unavailable."
                    + R
                )

            pause()

        elif c == "2":

            try:

                hostname = socket.gethostname()
                ip = socket.gethostbyname(hostname)

                print(
                    f"""
Hostname : {hostname}
Local IP : {ip}
"""
                )

            except Exception as e:
                print(RED + str(e) + R)

            pause()

        elif c == "3":

            host = input(
                "Domain you want to look up: "
            )

            try:

                result = socket.gethostbyname_ex(
                    host
                )

                print(
                    f"""
Name    : {result[0]}
Aliases : {result[1]}
IPs     : {result[2]}
"""
                )

            except Exception as e:
                print(
                    RED +
                    f"Lookup failed: {e}"
                    + R
                )

            pause()

        elif c == "4":

            try:

                result = subprocess.run(
                    ["ip", "addr"],
                    capture_output=True,
                    text=True
                )

                print(result.stdout)

            except:

                print(
                    "ip command unavailable."
                )

            pause()

        elif c == "0":
            return


# ============================================================
#                         QUICK MENU
# ============================================================

def quick_menu():

    while True:

        screen("⚡ QUICK ACCESS")

        print("""
1. 📅 Date / Time
2. 📊 Marks
3. 🔐 Password Generator
4. 🔢 PIN Generator
5. 🔒 SHA-256
6. 📏 Unit Converter
7. 📱 System Info
8. 💾 Storage
0. Back
""")

        c = input("Select: ")

        if c == "1":
            date_time()

        elif c == "2":
            marks()

        elif c == "3":
            password_generator()

        elif c == "4":
            pin_generator()

        elif c == "5":
            sha_text()

        elif c == "6":
            unit_converter()

        elif c == "7":
            system_info()

        elif c == "8":
            storage_info()

        elif c == "0":
            return


# ============================================================
#                     MONEY MENU
# ============================================================

def money_menu():

    while True:

        screen("💰 MONEY & CALCULATION")

        print("""
1. Expense Tracker
2. Monthly Expense Summary
3. Budget Calculator
4. Calculator Center
0. Back
""")

        c = input("Select: ")

        if c == "1":
            expense_tracker()

        elif c == "2":
            monthly_summary()

        elif c == "3":
            budget_calculator()

        elif c == "4":
            calculators()

        elif c == "0":
            return


# ============================================================
#                       STUDY MENU
# ============================================================

def study_menu():

    while True:

        screen("📚 STUDY CENTER")

        print("""
1. Study Timer
2. Stopwatch
3. Marks & Percentage
4. Exam Countdown
5. Study Notes
6. Study Checklist
7. Daily Study Planner
0. Back
""")

        c = input("Select: ")

        if c == "1":
            study_timer()

        elif c == "2":
            stopwatch()

        elif c == "3":
            marks()

        elif c == "4":
            exam_countdown()

        elif c == "5":
            study_notes()

        elif c == "6":
            study_checklist()

        elif c == "7":
            daily_planner()

        elif c == "0":
            return


# ============================================================
#                  PRODUCTIVITY MENU
# ============================================================

def productivity_menu():

    while True:

        screen("📝 PRODUCTIVITY")

        print("""
1. Notes Manager
2. To-Do Manager
3. Reminder List
4. Text Clipboard
5. Counter
6. Date / Time
0. Back
""")

        c = input("Select: ")

        if c == "1":
            notes_manager()

        elif c == "2":
            todo_manager()

        elif c == "3":
            reminder_list()

        elif c == "4":
            clipboard_saver()

        elif c == "5":
            counter()

        elif c == "6":
            date_time()

        elif c == "0":
            return


# ============================================================
#                    PHONE MENU
# ============================================================

def phone_menu():

    while True:

        screen("📱 PHONE / SYSTEM")

        print("""
1. Battery Info
2. Storage Info
3. RAM Info
4. CPU / System Info
5. Android Device Info
6. Termux Package Viewer
0. Back
""")

        c = input("Select: ")

        if c == "1":
            battery_info()

        elif c == "2":
            storage_info()

        elif c == "3":
            ram_info()

        elif c == "4":
            system_info()

        elif c == "5":
            android_info()

        elif c == "6":
            package_viewer()

        elif c == "0":
            return


# ============================================================
#                      FILE MENU
# ============================================================

def file_menu():

    while True:

        screen("📁 FILE TOOLS")

        print("""
1. File Explorer
2. File Search
3. File Size
4. Text File Viewer
5. Folder Size
6. Copy / Move
7. MIRAZ Temp Cleaner
0. Back
""")

        c = input("Select: ")

        if c == "1":
            file_explorer()

        elif c == "2":
            file_search()

        elif c == "3":
            file_size()

        elif c == "4":
            text_viewer()

        elif c == "5":
            folder_size()

        elif c == "6":
            copy_move()

        elif c == "7":
            temp_cleaner()

        elif c == "0":
            return


# ============================================================
#                    SECURITY MENU
# ============================================================

def security_menu():

    while True:

        screen("🔐 SECURITY TOOLS")

        print("""
1. Strong Password Generator
2. Random PIN Generator
3. SHA-256 Text Hash
4. File Checksum
5. Password Strength Meter
0. Back
""")

        c = input("Select: ")

        if c == "1":
            password_generator()

        elif c == "2":
            pin_generator()

        elif c == "3":
            sha_text()

        elif c == "4":
            file_checksum()

        elif c == "5":
            password_strength()

        elif c == "0":
            return


# ============================================================
#                         MAIN MENU
# ============================================================

def main():

    while True:

        clear()
        logo()

        print(
            CYAN +
            "╔════════════════════════════════════════════════════════════╗"
            + R
        )

        print(
            CYAN +
            "║" +
            R +
            "                 DAILY CONTROL CENTER                     " +
            CYAN +
            "║" +
            R
        )

        print(
            CYAN +
            "╠════════════════════════════════════════════════════════════╣"
            + R
        )

        print("║  01 💰 MONEY & CALCULATION                                ║")
        print("║  02 📚 STUDY CENTER                                       ║")
        print("║  03 📝 PRODUCTIVITY                                       ║")
        print("║  04 📱 PHONE / SYSTEM                                     ║")
        print("║  05 📁 FILE TOOLS                                         ║")
        print("║  06 🔐 SECURITY                                           ║")
        print("║  07 💻 CODING                                             ║")
        print("║  08 🌐 NETWORK                                            ║")
        print("║  09 ⚡ QUICK ACCESS                                        ║")

        print(
            CYAN +
            "╠════════════════════════════════════════════════════════════╣"
            + R
        )

        print("║  00 ❌ EXIT                                               ║")

        print(
            CYAN +
            "╚════════════════════════════════════════════════════════════╝"
            + R
        )

        print(
            DIM +
            f"\nMIRAZ SYSTEM TIME: {datetime.now().strftime('%I:%M:%S %p')}"
            + R
        )

        c = input(
            "\n" + MAGENTA + B + "MIRAZ OS > " + R
        ).strip()

        if c == "1":
            money_menu()

        elif c == "2":
            study_menu()

        elif c == "3":
            productivity_menu()

        elif c == "4":
            phone_menu()

        elif c == "5":
            file_menu()

        elif c == "6":
            security_menu()

        elif c == "7":
            coding_tools()

        elif c == "8":
            network_tools()

        elif c == "9":
            quick_menu()

        elif c == "0" or c == "00":

            clear()

            print(
                MAGENTA +
                B +
                "\n     M I R A Z   O S   O F F L I N E"
                + R
            )

            print(
                CYAN +
                "\n     Thanks for using MIRAZ OS 👋"
                + R
            )

            sys.exit(0)

        else:

            print(
                RED +
                "\nInvalid option!"
                + R
            )

            time.sleep(.7)


# ============================================================
#                          RUN
# ============================================================

if __name__ == "__main__":

    try:
        startup()
        main()

    except KeyboardInterrupt:

        clear()

        print(
            YELLOW +
            "\nMIRAZ OS stopped."
            + R
        )

    except Exception as e:

        print(
            RED +
            f"\nError: {e}"
            + R
        )
