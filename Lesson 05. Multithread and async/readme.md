# Домашнее задание
## Задание 1

В небольшом селе живут 30 людей. Каждый день разгневанные боги насылают одно из 4 проклятий (Боль, Жажду, Бессоницу и Дедлайн) на 10 людей. Род проклятия и персона случайны. Если проклятие не снять в течение дня - человек умирает.

К счастью для людей, рядом с селом есть группа индусов - которое знаю как превратить баг в фичу, чтобы спасти человека от неминуемой смерти. Команда индусов состоит из 5 людей: 1 - тимбилд. 4 - знахаря. Каждый знахарь ответственен за свой род проклятия.

Люди не знают какой род проклятия на них наложили. Поэтому они идут к индусу тимбилду - который определит его род и отправляет к соответствующему знахарю.

В среднем знахарь проводит обряд в течение 2 часов.

Условия:

- Чтобы попасть к знахарю, человек должен пройти через тимбилда.
- Тимбилд может работать только с одним человеком. Среднее время определения рода проклятия - занимает 1 минуту.
- Тимбилд знает, какие знахари сейчас доступны, а какие уже заняты обрядом.

Задача: Организовать правильную работу индусов и спасти деревню.

##  Задание 2

Дано приложение, которое совершает обход сайтов по списку. Задача - реализовать это же приложение, но с использованием библиотеки asyncio.

Сравните производительность обоих решений и ответьте на вопросы:

- Есть ли разница во времени выполнения и как она объясняется?
- Можно ли такой подход применить для обхода нескольких тысяч сайтов? Какие в этом случае возникают ограничения?

```
import requests
from time import time

SITES = ['www.google.com', 'www.yandex.ru', 'www.lenta.ru', 'www.rbc.ru', 'rg.ru']

def get_sync():
    t0 = time()
    for site in SITES:
        r = requests.get("https://" + site)
        r.status_code
    t1 = time()
    print("Sync poll took %s seconds" % (t1-t0))

get_sync()
```
