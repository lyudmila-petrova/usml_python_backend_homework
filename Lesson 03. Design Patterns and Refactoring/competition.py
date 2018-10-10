from random import randint
from abc import ABC, abstractmethod


class AbstractCar(ABC):
    @abstractmethod
    def race(self, distance, weather):
        pass

    @property
    @abstractmethod
    def name(self):
        return None

    @property
    @abstractmethod
    def max_speed(self):
        return None

    @property
    @abstractmethod
    def drag_coef(self):
        return None

    @property
    @abstractmethod
    def time_to_max(self):
        return None


class Car(AbstractCar):
    CAR_SPECS = {
        'ferrary': {"max_speed": 340, "drag_coef": 0.324, "time_to_max": 26},
        'bugatti': {"max_speed": 407, "drag_coef": 0.39, "time_to_max": 32},
        'toyota': {"max_speed": 180, "drag_coef": 0.25, "time_to_max": 40},
        'lada': {"max_speed": 180, "drag_coef": 0.32, "time_to_max": 56},
        'sx4': {"max_speed": 180, "drag_coef": 0.33, "time_to_max": 44},
    }

    def __init__(self, name, max_speed=None, drag_coef=None, time_to_max=None):
        self.__name = name

        if None in [max_speed, drag_coef, time_to_max]:
            if name not in Car.CAR_SPECS:
                raise KeyError(f"Не удалось найти существующую спецификацию для {name}. Задайте спецификацию вручную")

            self.__max_speed = Car.CAR_SPECS[name]['max_speed']
            self.__drag_coef = Car.CAR_SPECS[name]['drag_coef']
            self.__time_to_max = Car.CAR_SPECS[name]['time_to_max']
        else:
            self.__max_speed = max_speed
            self.__drag_coef = drag_coef
            self.__time_to_max = time_to_max

    @property
    def name(self):
        return self.__name

    @property
    def max_speed(self):
        return self.__max_speed

    @property
    def drag_coef(self):
        return self.__drag_coef

    @property
    def time_to_max(self):
        return self.__time_to_max

    def race(self, distance, weather):
        car = self
        time = 0

        for distance in range(distance):
            wind_speed = weather.wind_speed

            if time == 0:
                speed = 1
            else:
                speed = car.max_speed if time > car.time_to_max else (time / car.time_to_max) * car.max_speed
                if speed > wind_speed:
                    speed -= (car.drag_coef * wind_speed)

            time += float(1) / speed

        return time


class NullCarDecorator(AbstractCar):
    def __init__(self, obj):
        self.obj = obj

    def race(self, distance, weather):
        return self.obj.race(distance, weather)

    @property
    def name(self):
        return self.obj.name

    @property
    def max_speed(self):
        return self.obj.max_speed

    @property
    def drag_coef(self):
        return self.obj.drag_coef

    @property
    def time_to_max(self):
        return self.obj.time_to_max


class VerboseCar(NullCarDecorator):
    def __init__(self, obj):
        super().__init__(obj)

    def race(self, distance, weather):
        print("Car <%s> on start" % self.obj.name)
        time = self.obj.race(distance, weather)
        print("Car <%s> result: %f" % (self.obj.name, time))
        return time


class Weather:
    def __init__(self, max_wind_speed=20):
        self._max_wind_speed = max_wind_speed

    @property
    def wind_speed(self):
        return randint(0, self._max_wind_speed)


class NotificationManager:
    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, subscriber):
        if subscriber not in self.__subscribers:
            self.__subscribers.add(subscriber)

    def unsubcribe(self, subscriber):
        if subscriber in self.__subscribers:
            self.__subscribers.remove(subscriber)

    def notify_subscribers(self, message):
        for subscriber in self.__subscribers:
            subscriber.update(message)


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, message):
        pass


class SmsSubscriber(AbstractObserver):
    def __init__(self, phone):
        self.__phone = phone

    def update(self, message):
        print('%s recieved message!' % self.__phone)


class EmailSubscriber(AbstractObserver):
    def __init__(self, email):
        self.__email = email

    def update(self, message):
        print("%s recieved message: %s" % (self.__email, message))


class Competition(NotificationManager):
    __instance = None

    def __new__(cls, *args):
        if Competition.__instance is None:
            Competition.__instance = object.__new__(cls)
        return Competition.__instance

    def __init__(self, distance, weather=None):
        super().__init__()
        self.distance = distance
        self.weather = weather or Weather()

    def start(self, cars):
        results = []
        for car in cars:
            time = car.race(self.distance, self.weather)
            results.append((car.name, time))

        print("---")
        results_sorted = sorted(results, key=lambda x: x[1])
        winner_name = results_sorted[0][0]
        winner_time = results_sorted[0][1]
        print("Winner is", results_sorted[0][0])

        self.notify_subscribers(f"{winner_name} came first with {winner_time}")


if __name__ == "__main__":
    weather = Weather(35)
    competition = Competition(10000, weather)

    competition.subscribe(EmailSubscriber("test@example.com"))
    competition.subscribe(SmsSubscriber("+79990000000"))

    cars = [
        Car('ferrary'),
        Car('bugatti'),
        Car('toyota'),
        Car('lada'),
        Car('sx4'),
        Car('drandulet', max_speed=120, drag_coef=0.42, time_to_max=63)
    ]

    cars = map(lambda x: VerboseCar(x), cars)

    competition.start(cars)
