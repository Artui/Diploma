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
        address = "http://" + str(ngrok_data) + ".ngrok.io/"
        res = rq.post(url=address, files={"file": open("opencv.png", "rb").read()})
        print(res.text)
        result = json.loads(res.text)
        result.sort(key=operator.itemgetter('confidence'))
        if len(result) == 0:
            print("No objects found")
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
        if self.goal_coordinates.get('x') < photo_width:
            if (self.goal_coordinates.get('x') + 50) < photo_width / 2:
                turn_koef = (photo_width - self.goal_coordinates.get('x')) / 15
                self.movement.turn_left(0.1 * turn_koef)
                return
        if self.goal_coordinates.get('x') > photo_width:
            if (self.goal_coordinates.get('x') - 50) > photo_width / 2:
                turn_koef = (photo_width - self.goal_coordinates.get('x')) / 15
                self.movement.turn_left(0.1 * turn_koef)
                return
        print("No need to turn")

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

    def distance_not_changed(self, distance):
        return (len(self.distance_history) > 3
                and (self.distance_history[-1] - distance < 3)
                and (self.distance_history[-2] - distance < 3))
