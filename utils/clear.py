import json  # подключили библиотеку для работы с json
from pprint import pprint  # подключили Pprint для красоты выдачи текста
import re
from pandas.io.json import json_normalize

keyUp = ["react", "reactjs", "native"]
keyDow = ["вакансия"]

def ClearStep1():
    with open('pars/1050008285/data.json', 'r', encoding='utf-8') as f:  # открыли файл с данными
        text = json.load(f)  # загнали все, что получилось в переменную
        i = 0
        i2 = 0
        i3 = 0
        data = []
        dubl = []
        for txt in text:  # создали цикл, который будет работать построчно
            i += 1
            isNew = False
            for k in keyUp:
                if k in txt["text"].lower() and "вакансия" not in txt["text"].lower():
                    if txt["text"] not in dubl:
                        i3 += 1
                        dubl.append(txt["text"])
                        isNew = True
                    if isNew:
                        i2 += 1
                        isNumber = False
                        isNumberOld = False
                        clean_lines = ""
                        for v in txt["text"]:
                            if ((v == " " and isNumber) or (v == "." and isNumber)):
                                isNumberOld = True
                                continue
                            if v.isdigit():
                                isNumber = True
                            else:
                                if isNumberOld:
                                    clean_lines += " "
                                    isNumberOld = False
                                isNumber = False
                            clean_lines += v
                        number = [int(s) for s in re.findall(r'\b\d+\b', clean_lines)]
                        # newNumber = []
                        # for n in number:
                        #     # if n < 50000:
                        #     isBaks = False
                        #     if n > 100 and n < 10000:
                        #         isBaks = True
                        #     if isBaks == False:
                        #         newNumber.append(n)
                        #     # if isBaks:isBaks
                        #     #     a = n * 70
                        #         newNumber.append(a)
                        # number = newNumber
                        number = sorted(number, reverse=True)
                        max = 0
                        if len(number) > 0:
                            max = number[0]
                        data.append({"id":txt["id"], "date":txt["date"], "url": txt["url"], "text":txt["text"], "number":number, "max":max})
                        break
        with open(f"clear.json", 'w') as f:
            json.dump(data, f, ensure_ascii=False)
        print(f"всего сообщений: {i}; найдено совпедений:{i2}; без дублей:{i3}")
            # print(txt["id"])  # и выводим на экран все, что в значении ключей name и salary
        # pprint(text)  # вывели результат на экран

def ClearStep2():
    with open('clear.json', 'r', encoding='utf-8') as f:  # открыли файл с данными
        text = json.load(f)  # загнали все, что получилось в переменную
        result = sorted(text, key=lambda x: x['max'])
        fin = ""
        for txt in result:

            fin += f"max:{txt['max']} \n"
            fin += f"number: {txt['number']} \n"
            fin += f"date: {txt['date']} \n"
            fin += f"url: {txt['url']} \n\n"
            words = txt["text"].split(" ")
            iA = 0
            line = ""
            for v in words:
                iA +=1
                if iA == 10:
                    iA = 0
                    line += "\n"
                line += v + " "

            fin += f"{line} \n"
            fin += f"\n\n"
        #     i += 1
        #     # print(txt["text"])
        #     if txt["text"] not in data:
        #         i2 += 1
        #         data.append(txt["text"])
        print(f"всего сообщений: {len(text)};")
        with open('finModel.txt', 'w') as f:
            f.write(fin)
ClearStep1()
ClearStep2()