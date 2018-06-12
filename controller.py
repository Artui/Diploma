from .camera import get_image
import requests as rq
import distance, movement


class CarController:
    goal = None

    def __init__(self):
        image = get_image()

    def calculate_turn(self):
        pass

    def run(self):
        pass