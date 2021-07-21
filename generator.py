from pickle import load, dump
from bs4 import BeautifulSoup
from random import choice
from urllib.request import urlopen
from datetime import date
from os import path


def create_data(pages):
    webpage = "https://www.parlamentnilisty.cz/arena/monitor?p="
    beginning = []
    ending = []
    following = dict()
    for i in range(1, pages + 1):
        current = urlopen(webpage + str(i))

        soup = BeautifulSoup(current.read(), "html.parser")

        x = soup.select("h2")
        for i in range(len(x)):
            if "href" in str(x[i]):
                continue
            title = str(x[i]).replace("<h2>", "")
            title = title.replace("</h2>", "")
            words = title.split()
            beginning.append(words[0])
            ending.append(words[-1])
            for j in range(len(words) - 1):
                if following.get(words[j]) is None:
                    following[words[j]] = []
                    following[words[j]].append(words[j + 1])
                else:
                    following[words[j]].append(words[j + 1])

    with open(str(date.today()) + ".txt", "wb") as f:
        dump((beginning, ending, following), f)


def create_headline(b, e , f):
    i = 0
    result = ""
    while True:
        if i == 0:
            last = choice(b)
            result += last + " "
        if last in e and i >= 10:
            break
        else:
            try:
                last = choice(f[last])
                result += last + " "
            except KeyError:
                last = choice(f[choice(list(f.keys()))])
                result += last + " "
        i += 1
    return result


if __name__ == "__main__":
    date_file = str(date.today()) + ".txt"
    if not path.exists(date_file):
        create_data(1000)
    with open(date_file, "rb") as f:
        data = load(f)
    beginning, ending, following = data
    print(create_headline(beginning, ending, following))