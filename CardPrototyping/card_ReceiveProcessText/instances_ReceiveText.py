from CardPrototyping.card_Human.instances_Human import octavio, joe
from CardPrototyping.card_ReceiveProcessText.ReceiveText import ReceiveText

tell_humans = ReceiveText()
tell_humans.do_send_msg_complete(octavio.do_say,10)
tell_humans.do_send_msg_complete(joe.do_say)
