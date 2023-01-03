# PID for turning

ad = 0 # angle diff
past_ad = 0

# turning speed = 1-5
def adv_turn(speed):
    if speed == 1:
        arr = ['z', 120, 120]
        pause_time = 0.3

    elif speed == 2:
        arr = ['z', 180, 180]
        pause_time = 0.3

    elif speed == 3:
        arr = ['z', 200, 200]
        pause_time = 0.2

    elif speed == 4:
        arr = ['z', 220, 220]
        pause_time = 0.1

    elif speed == 5:
        arr = ['z', 250, 250]
        pause_time = 0.1




