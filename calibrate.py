from CardPrototyping.card_SendGifts.SendGifts import SendGifts
import time

def main():

    t = SendGifts("some name")

    t.calibrate()
    time.sleep(100)
if __name__ == '__main__':
    main()
# {'on_msg': {'args': ('hello world',), 'kwargs': {}, -1: [], 10: [<bound method GenericCardTemplate.<locals>.GenericCard.__generic_callback_template.<locals>.__generic_callback of <CardPrototyping.card_Human.Human.Human object at 0x7fb7320687b8>>], 5: [<bound method GenericCardTemplate.<locals>.GenericCard.__generic_callback_template.<locals>.__generic_callback of <CardPrototyping.card_Human.Human.Human object at 0x7fb7320686a0>>], 'returned_args': [None]}}
