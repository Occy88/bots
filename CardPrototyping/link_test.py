from ApplicationManagers.ADBManager import adb_manager_card
from CardPrototyping.CardTest import card_test_card


def example(run_time):
    adb_manager_card.bind_on_frame_update(card_test_card.my_fun_bot, 20)
    card_test_card.bind_on_swipe(adb_manager_card.swipe)

    # some random sleep to decide how long you want the above to run for :D
    import time
    time.sleep(run_time)
