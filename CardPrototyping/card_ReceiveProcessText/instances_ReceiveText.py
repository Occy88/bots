from CardPrototyping.card_Human.instances_Human import octavio, joe
from CardPrototyping.card_ReceiveProcessText.ReceiveText import ReceiveText

tell_humans = ReceiveText()
tell_humans.on_msg_complete(octavio.on_say)
tell_humans.on_msg_complete(joe.on_say)
