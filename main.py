import os
import json
import random
import string
import time

# 创建必要的文件和文件夹
if not os.path.exists("dict.book"):
    with open("dict.book", "w",encoding='utf-8') as file:
        file.write("{}")
if not os.path.exists("./dailys"):
    os.mkdir("./dailys")
if not os.path.exists("./origin"):
    os.mkdir("./origin")
if not os.path.exists("./encoded"):
    os.mkdir("./encoded")

def createRandomString(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    result = ''.join(random.choice(characters) for _ in range(length))
    return result


def decodeByBook(txt: str, book: dict, codeLength: int = 10) -> str:
    res: str = ""
    temp_txt: str = ""
    book = {value: key for key, value in book.items()}
    for char in txt:
        temp_txt += char
        if len(temp_txt) == codeLength:
            res += book[temp_txt]
            temp_txt = ""

    return res

# 解密
def decodeDaily(dailyPath: str, bookPath: str = "dict.book") -> str:
    book: dict = readBook(bookPath)
    origin_txt: str = ""
    with open(dailyPath, "r", encoding='utf-8') as file:
        origin_txt = file.read()
    
    fileName = "./encoded/" + \
        time.strftime("%Y-%m-%d_%H_%M", time.localtime()) + ".txt"
    
    with open(fileName, "w", encoding='utf-8') as file:
        file.write(decodeByBook(origin_txt,book))
    
def encodeByBook(txt: str, book: dict) -> str:
    res = ""
    for char in txt:
        res += book[char]
    return res

# 加密
def encodeDaily(originPath: str, bookPath: str = "dict.book") -> str:
    book: dict = readBook(bookPath)
    daily_txt: str = ""
    with open(originPath, "r", encoding='utf-8') as file:
        daily_txt = file.read()

    for char in daily_txt:
        keys = book.keys()

        # 没有找到对应的值
        if char not in keys:
            new_value: str = createRandomString(10)

            while new_value in book.values():
                new_value = createRandomString(10)

            book[char] = new_value

    for key in book.keys():
        print(f"{key} => {book[key]}")

    # 保存daily
    fileName = "./dailys/" + \
        time.strftime("%Y-%m-%d_%H_%M", time.localtime()) + ".daily"
    with open(fileName, "w",encoding='utf-8') as daily_file:
        daily_file.write(encodeByBook(daily_txt, book))

    # 保存book
    with open(bookPath, "w",encoding='utf-8') as file:
        file.write(json.dumps(book))


def readBook(bookPath: str = "dict.book") -> dict:
    dic: dict = {}

    with open(bookPath, "r",encoding='utf-8') as file:
        dic = json.loads(file.read())
        print()

    return dic


def getOriginDailyList() -> dict:
    origin: list = os.listdir("./origin")
    origin_dic: dict = {}

    for i in range(1, len(origin)+1):
        origin_dic[i] = {
            "filePath": "./origin/"+origin[i-1],
            "fileName": origin[i-1],
            "Index": i
        }

    return origin_dic


def getDailyList() -> dict:
    origin: list = os.listdir("./dailys")
    origin_dic: dict = {}

    for i in range(1, len(origin)+1):
        origin_dic[i] = {
            "filePath": "./dailys/"+origin[i-1],
            "fileName": origin[i-1],
            "Index": i
        }

    return origin_dic


def func_2() -> None:
    org_dic: dict = getOriginDailyList()
    for key in org_dic.keys():
        print(f"{key} : {org_dic[key]}")

    dailyIndex: int = int(input("输入要打开的文件代码："))

    encodeDaily(org_dic[dailyIndex]['filePath'])


def func_3() -> None:
    daily_dic: dict = getDailyList()
    for key in daily_dic.keys():
        print(f"{key} : {daily_dic[key]}")

    dailyIndex: int = int(input("输入要打开的文件代码："))

    decodeDaily(daily_dic[dailyIndex]['filePath'])

while True:
    
    print("""
          [1]
          """)
    
    code: int = int(input("Code:"))

    func_dict = {
        1: False,
        2: func_2,
        3: func_3,
    }

    func_dict[code]()
