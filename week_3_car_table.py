"""
Take csv-file with vehicles' parameters and make list of car-like objects
"""

import os
import csv


class CarBase:
    #   order of parameters in line of csv-file without error:
    #   car_type;brand;passenger_seats_count;photo_file_name;body_whl;carrying;extra
    #       [1,1,1,1,0,1,0]  Car
    #       [1,1,0,1,1,1,0]  Truck
    #       [1,1,0,1,0,1,1]  SpecMachine
    car_class = ["car", "truck", "spec_machine"]

    def __init__(self, car_type, brand, photo_file_name, carrying):
        self.car_type = car_type
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = carrying

    def __str__(self):
        return f"{self.car_type} \"{self.brand}\""

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def get_photo_file_ext(photo_file_name):
        return os.path.splitext(photo_file_name)

    @classmethod
    def parse_csv_string(cls, row):
        print(row)
        check = ""
        car = None
        if row:
            check = row[0].lower()
        if check in cls.car_class:
            car_type = check
            brand = row[1]
            photo = CarBase.get_photo_file_ext(row[3])
            if photo[0]:  # and photo[1]: if file extension must be
                photo_file_name = photo[0]
            else:
                return None
            try:
                if car_type == cls.car_class[0]:
                    passenger_seats_count = int(row[2])
                else:
                    passenger_seats_count = ''

                if car_type == cls.car_class[1]:
                    if row[4] == '' or row[4] == '0':
                        body_whl = [0, 0, 0]
                    else:
                        body_whl = list(map(lambda x: float(x), row[4].split('x')))
                else:
                    body_whl = ''
                carrying = float(row[5])

                if car_type == cls.car_class[2]:
                    extra = row[6]
                else:
                    extra = ''
            except (ValueError, IndexError):
                return None

            car = [car_type, brand, passenger_seats_count,
                   photo_file_name, body_whl, carrying, extra]
        return car


class Car(CarBase):
    def __init__(self, car_type, brand, passenger_seats_count, photo_file_name, carrying):
        self.passenger_seats_count = passenger_seats_count
        super(Car, self).__init__(car_type, brand, photo_file_name, carrying)


class Truck(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, body_whl):
        self.body_width = body_whl[0]
        self.body_height = body_whl[1]
        self.body_length = body_whl[2]
        super(Truck, self).__init__(car_type, brand, photo_file_name, carrying)

    def get_body_volume(self):
        body_volume = self.body_width * self.body_height * self.body_length
        return body_volume


class SpecMachine(CarBase):
    def __init__(self, car_type, brand, photo_file_name, carrying, extra):
        self.extra = extra
        super(SpecMachine, self).__init__(car_type, brand, photo_file_name, carrying)


def get_car_list(csv_filename):
    car_list = []
    lines_error = []
    with open(csv_filename, newline='', encoding='utf-8') as csv_f:
        carreader = csv.reader(csv_f, delimiter=';')
        next(carreader)
        i = 0
        # Each row read from the csv file is returned as a list of strings
        for row in carreader:
            i += 1
            car = CarBase.parse_csv_string(row)
            if car:
                if car[0] == CarBase.car_class[0]:
                    car = Car(car[0], car[1], car[2], car[3], car[5])
                elif car[0] == CarBase.car_class[1]:
                    car = Truck(car[0], car[1], car[3], car[5], car[4])
                elif car[0] == CarBase.car_class[2]:
                    car = SpecMachine(car[0], car[1], car[3], car[5], car[6])
                else:
                    continue
                car_list.append(car)
            else:
                lines_error.append(i)
    print("\nThese lines contain errors:", lines_error)
    return car_list


def main(csv_filename):
    car_list = get_car_list(csv_filename)
    print("These descriptions have gotten from csv-file:\n",car_list, "\n")
    print("Attribute of a Truck-class vehicle:\n",car_list[-3].__dict__, "\n")
    print("Truck-class vehicle volume:\n",car_list[1].get_body_volume())


if __name__ == "__main__":
    csv_filename = "coursera_week3_cars.csv"
    main(csv_filename)
