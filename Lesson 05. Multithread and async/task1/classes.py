import threading
from queue import Queue
from time import time, sleep

from numpy.random.mtrand import RandomState


class Manager:
    def __init__(self, healers):
        self.__healers = dict(map(lambda h: (h.speciality, h), healers))

    def manage(self, persons):
        for p in persons:
            sleep(0.25)
            print(p, 'is queued')
            self.__healers[p.damn].add_patient(p)


class Healer(threading.Thread):
    def __init__(self, speciality, day_start=time()):
        super().__init__()
        self.__speciality = speciality
        self.__queue = Queue()
        self.__day_start = day_start

    @property
    def speciality(self):
        return self.__speciality

    def run(self):
        while not self.__queue.empty():
            patient = self.__queue.get()
            damn = patient.damn
            result = patient.cure(self)
            if result:
                print(patient, 'is successfully recovered from', damn, 'at', time() - self.__day_start)
            else:
                print('My drugs are useless for person', patient)

    def set_day_start(self, ts):
        self.__day_start = ts

    def add_patient(self, patient):
        self.__queue.put(patient)


class Person:
    def __init__(self, person_id):
        self.__id = person_id
        self.__damn = None
        self.__damn_timestamp = None

    @property
    def damn(self):
        return self.__damn

    @damn.setter
    def damn(self, name):
        self.__damn = name
        self.__damn_timestamp = time()

    def cure(self, healer: Healer):
        if healer.speciality == self.__damn:
            rs = RandomState()
            sleep(rs.uniform(1.5, 2.5))
            self.__damn = None
            self.__damn_timestamp = None
            return True
        return False

    def is_health(self):
        return self.__damn is None

    def __str__(self):
        return "Person#%d(%s)" % (self.__id, self.__damn)

    def __repr__(self):
        return "Person#%d(%s)" % (self.__id, self.__damn)

    def __del__(self):
        if self.__damn:
            print('Game over for person #%d. COD is "<%s>"' % (self.__id, self.__damn))
