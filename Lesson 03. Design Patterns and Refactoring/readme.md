# Задание

_В качестве основы берем код урока 2, файл competition.py_

Изучить паттерны проектирования, применить к прошлому домашнему заданию минимум по одному паттерну из каждой категории (порождающие, структурные, поведенческие). Код должен соответствовать SOLID принципам. 

В readme файле укажите обоснование использования паттерна.

## Решение. Использованные паттерны

### Singleton (Порождающий)

Не позволяет создание более 1 экземпляра класса для соревнования (Competition).

Уже применен по итогам прошлого задания.

### Decorator (Структурный)
Добавлена болтливая обертка для класса Car.

### Observer (Поведенческий)
Добавлена возможность подписки на результаты соревнования.

Не все имеют возможность присутсвовать на заездах лично, но готовы получать оповещения по email и sms.
