import movement
import time

movement = movement.Movement()

movement.get_connection()
time.sleep(3)
movement.start_all_wheels("055")
time.sleep(3)
movement.stop_all_wheels()
time.sleep(3)
movement.start_all_wheels("055")
time.sleep(3)
movement.stop_all_wheels()