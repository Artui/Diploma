import movement
import time

movement = movement.Movement()

movement.get_connection()
time.sleep(3)
movement.start_all_wheels("060")
time.sleep(2)
movement.stop_all_wheels()
time.sleep(3)
movement.start_all_wheels("060")
time.sleep(2)
movement.stop_all_wheels()