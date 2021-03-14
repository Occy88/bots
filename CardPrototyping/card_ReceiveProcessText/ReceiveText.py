#  imports change_text from ChangeText
from CardPrototyping.GenericCard import GenericCardTemplate


class ReceiveText(GenericCardTemplate()):
    """
    Print C
    """

    def do_send_msg(self, text):
        """
        receives text,
        :param text:
        :return:
        """
        text = "do_msg_modified " + text
        print("MSG Received, (modified a bit) : ", text)
        pass
