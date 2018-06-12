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
            distance.get_connection()
            distances = distance.get_distance_lists()
            self.initial_distance = distances[4]
            self.calculate_initial_turn(result.get("image_width"))

    def calculate_initial_turn(self, photo_width):
        if self.goal_coordinates.get('x') < photo_width:
            if (self.goal_coordinates.get('x') + 50) < photo_width / 2:
                turn_koef = (photo_width - self.goal_coordinates.get('x')) / 10
                self.movement.turn_right(0.1 * turn_koef)
                return
        if self.goal_coordinates.get('x') > photo_width:
            if (self.goal_coordinates.get('x') - 50) > photo_width / 2:
                turn_koef = (photo_width - self.goal_coordinates.get('x')) / 10
                self.movement.turn_right(0.1 * turn_koef)
                return
        print("No need to turn")

    def run(self):
        self.movement.get_connection()
        self.movement.start_all_wheels("050")
        while self.goal:
            distances = distance.get_distance_lists()
            print(distances)
            if distances[4] <= 5:
                self.movement.stop_all_wheels()
            time.sleep(0.3)
