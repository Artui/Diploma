import movement
import time

movement = movement.Movement()

movement.get_connection()
time.sleep(3)
movement.start_all_wheels("060")
time.sleep(1.5)
movement.stop_all_wheels()
movement.start_wheel(1, "120")
time.sleep(1)
movement.stop_all_wheels()
movement.start_all_wheels("060")
time.sleep(1.5)
movement.stop_all_wheels()