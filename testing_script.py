import movement
import time

movement.get_connection()
time.sleep(1)
movement.start_all_wheels("070")
time.sleep(1)
movement.stop_all_wheels()
