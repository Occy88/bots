# from PokemonGo.DetectPokestop import pokestop_detector
# from CardPrototyping.Functions import modify_text
# from CardPrototyping.card_ReceiveProcessText.instances_ReceiveText import tell_humans
from CardPrototyping.card_ADB.instances_ADB import android_phone
from PokemonGo.DetectPokestop import find_locations


# from CardPrototyping.card_ADB.instances_ADB import  android_phone
def main(text):
    print("+++++++++++++SENT SIGNAL TO PROCESS TEXT+++++++++++")
    android_phone.do_frame_update_complete(find_locations, 20)
    android_phone.do_frame_update_complete(find_locations,-1)
    android_phone.do_frame_update_complete(find_locations,10)


    input("enter to stop")


if __name__ == '__main__':
    main("hello world")
# {'on_msg': {'args': ('hello world',), 'kwargs': {}, -1: [], 10: [<bound method GenericCardTemplate.<locals>.GenericCard.__generic_callback_template.<locals>.__generic_callback of <CardPrototyping.card_Human.Human.Human object at 0x7fb7320687b8>>], 5: [<bound method GenericCardTemplate.<locals>.GenericCard.__generic_callback_template.<locals>.__generic_callback of <CardPrototyping.card_Human.Human.Human object at 0x7fb7320686a0>>], 'returned_args': [None]}}