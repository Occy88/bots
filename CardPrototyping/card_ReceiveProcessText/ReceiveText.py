#  imports change_text from ChangeText
from CardPrototyping.GenericCard import GenericCardTemplate


class ReceiveText(GenericCardTemplate()):
    """
    Print C
    """

    def on_msg(self, text):
        """
        receives text,
        :param text:
        :return:
        """
        text = "on_msg_modified " + text
        print("MSG Received, (modified a bit) : ", text)
        pass


