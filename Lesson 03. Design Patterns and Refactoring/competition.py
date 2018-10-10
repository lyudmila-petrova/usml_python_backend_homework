from random import randint


class Car:
    CAR_SPECS = {
        'ferrary': {"max_speed": 340, "drag_coef": 0.324, "time_to_max": 26},
        'bugatti': {"max_speed": 407, "drag_coef": 0.39, "time_to_max": 32},
        'toyota': {"max_speed": 180, "drag_coef": 0.25, "time_to_max": 40},
        'lada': {"max_speed": 180, "drag_coef": 0.32, "time_to_max": 56},
        'sx4': {"max_speed": 180, "drag_coef": 0.33, "time_to_max": 44},
    }


class Weather:
    def __init__(self, max_wind_speed=20):
        self._max_wind_speed = max_wind_speed

    @property
    def wind_speed(self):
        return randint(0, self._max_wind_speed)


class Competition(object):
    __instance = None

    def __new__(cls, val):
        if Competition.__instance is None:
            Competition.__instance = object.__new__(cls)
            Competition.__instance.val = val
        return Competition.__instance

    def __init__(self, distance, weather=None):
        self.distance = distance
        self.weather = weather or Weather()

    def start(self, car_specs):
        for name, car in car_specs.items():
            time = 0

            for distance in range(self.distance):
                wind_speed = self.weather.wind_speed

                if time == 0:
                    speed = 1
                else:
                    speed = (time / car["time_to_max"]) * car['max_speed']
                    if speed > wind_speed:
                        speed -= (car["drag_coef"] * wind_speed)

                time += float(1) / speed

            print("Car <%s> result: %f" % (name, time))


if __name__ == "__main__":
    competition = Competition(10000)
    competition.start(Car.CAR_SPECS)
