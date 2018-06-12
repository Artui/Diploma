import camera
import requests as rq
import distance, movement
import json
import operator


class CarController:
    goal = ""
    goal_coordinates = {}

    def __init__(self, args):
        image = camera.get_image()
        ngrok_data = args[1] if len(args) > 1 else ""
        address = "http://" + str(ngrok_data) + ".ngrok.io/"
        res = rq.post(url=address, files={"file": open("opencv.png", "rb").read()})
        print(res.text)
        result = json.loads(res.text)
        result.sort(key=operator.itemgetter('confidence'))
        result = result[0]
        self.goal = result.get("name")
        self.goal_coordinates = {"x": (result.get("start_x") + result.get('end_x'))/2,
                                 "y": (result.get("start_y") + result.get('end_y'))/2}
        distance.get_connection()
        distances = distance.get_distance_lists()
        print(distances)

    def calculate_turn(self):
        pass

    def run(self):
        pass
