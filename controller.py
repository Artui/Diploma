import json
import operator
import sys
import time

import requests as rq

import camera
import distance
import movement


class CarController:
    goal = ""
    goal_coordinates = {}
    initial_distance = 0
    movement = movement.Movement()
    distance = distance.Distance()
    distance_history = []

    def __init__(self, args):
        image = camera.get_image()
        ngrok_data = args[1] if len(args) > 1 else ""
        self.address = "http://" + str(ngrok_data) + ".ngrok.io/"
        result = self.get_photo_data()
        if not result:
            sys.exit(0)
        else:
            result = result[0]
            self.goal = result.get("name")
            self.goal_coordinates = {"x": (result.get("start_x") + result.get('end_x')) / 2,
                                     "y": (result.get("start_y") + result.get('end_y')) / 2}
            self.distance.get_connection()
            distances = self.distance.get_distance_list()
            self.initial_distance = distances[4]
            self.calculate_initial_turn(result.get("image_width"))

    def calculate_initial_turn(self, photo_width):
        if self.goal_coordinates.get('x') < photo_width / 2:
            if (self.goal_coordinates.get('x') + 50) < photo_width / 2:
                turn_koef = (photo_width - self.goal_coordinates.get('x')) / 15
                self.movement.turn_left(0.1 * turn_koef)
                return
        if self.goal_coordinates.get('x') > photo_width / 2:
            if (self.goal_coordinates.get('x') - 50) > photo_width / 2:
                turn_koef = (self.goal_coordinates.get('x') - photo_width) / 15
                self.movement.turn_left(0.1 * turn_koef)
                return
        print("No need to turn")

    def turn_to_avoid(self, coords_data, photo_width):
        if coords_data.get('x') < photo_width / 2:
            if coords_data.get('x') + 50 > photo_width / 2:
                turn_koef = (photo_width - coords_data.get('x')) / 15
                self.movement.turn_left(0.1 * turn_koef / 2)
                self.movement.start_all_wheels("070")
                time.sleep(1)
                self.movement.stop_all_wheels()
                self.movement.turn_right(0.1 * turn_koef / 2)
                self.movement.start_all_wheels("070")
                time.sleep(1)
                self.movement.stop_all_wheels()
                self.movement.turn_left(0.1 * turn_koef)
                return

        if coords_data.get('x') > photo_width / 2:
            if coords_data.get('x') - 50 < photo_width / 2:
                turn_koef = (coords_data.get('x') - photo_width) / 15
                self.movement.turn_right(0.1 * turn_koef / 2)
                self.movement.start_all_wheels("070")
                time.sleep(1)
                self.movement.stop_all_wheels()
                self.movement.turn_left(0.1 * turn_koef / 2)
                self.movement.start_all_wheels("070")
                time.sleep(1)
                self.movement.stop_all_wheels()
                self.movement.turn_right(0.1 * turn_koef)
                return

        print("No need to turn")

    def get_photo_data(self):
        image = camera.get_image()
        res = rq.post(url=self.address, files={"file": open("opencv.png", "rb").read()})
        print(res.text)
        result = json.loads(res.text)
        result.sort(key=operator.itemgetter('confidence'))
        if len(result) == 0:
            print("No objects found")
            return None
        return result[0]

    def run(self):
        self.movement.get_connection()
        self.movement.start_all_wheels("070")
        while self.goal:
            distances = self.distance.get_distance_list()
            print(distances)
            if (distances[4] <= 5 and distances[3] < 200) or self.distance_not_changed(distances[4]):
                self.goal = None
            self.distance_history.append(distances[4])
            time.sleep(0.3)
            new_photo = self.get_photo_data()
            if new_photo:
                if new_photo.get('name') != self.goal:
                    avoid_coords = {"x": (new_photo.get("start_x") + new_photo.get('end_x')) / 2,
                                    "y": (new_photo.get("start_y") + new_photo.get('end_y')) / 2}
                    self.turn_to_avoid(avoid_coords, new_photo.get("image_width"))

    def distance_not_changed(self, distance):
        return (len(self.distance_history) > 3
                and (self.distance_history[-1] - distance < 3)
                and (self.distance_history[-2] - distance < 3))
