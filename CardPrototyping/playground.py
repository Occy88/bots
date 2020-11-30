import time

from CardPrototyping.Functions import modify_text
from CardPrototyping.card_ReceiveProcessText.instances_ReceiveText import tell_humans


def main(text):
    print("+++++++++++++SENT SIGNAL TO PROCESS TEXT+++++++++++")
    text = modify_text(text)
    tell_humans.on_msg(text)
    time.sleep(1)


if __name__ == '__main__':
    main("hello world")
# {'on_msg': {'args': ('hello world',), 'kwargs': {}, -1: [], 10: [<bound method GenericCardTemplate.<locals>.GenericCard.__generic_callback_template.<locals>.__generic_callback of <CardPrototyping.card_Human.Human.Human object at 0x7fb7320687b8>>], 5: [<bound method GenericCardTemplate.<locals>.GenericCard.__generic_callback_template.<locals>.__generic_callback of <CardPrototyping.card_Human.Human.Human object at 0x7fb7320686a0>>], 'returned_args': [None]}}
