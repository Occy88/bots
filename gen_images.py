from ImageProcessing.MLPictureGen import MLPictureGen
# from ImageProcessing.ImgTools import img_col_similarity, crop_img
# from CardPrototyping.card_ADB.instances_ADB import android_phone

import time


# from CardPrototyping.card_ADB.instances_ADB import  android_phone
def main():
    # print("+++++++++++++SENT SIGNAL TO PROCESS TEXT+++++++++++")
    # android_phone.do_frame_update_complete(find_locations, 20)
    # android_phone.do_frame_update_complete(find_locations,-1)
    # android_phone.do_frame_update_complete(find_locations,10)
    #
    #
    # input("enter to stop")
    from ImageProcessing.ImgTools import load_img, show_img, resize_img, resize_bigger_to_smaller_img, img_col_similarity
    # show_img(orig)
    #
    # res = resize_img(orig, 0.7, percent=True)
    # show_img(res)
    # orig, res = resize_bigger_to_smaller_img(orig, res)
    # show_img(orig)
    # show_img(res)
    # print(img_col_similarity(orig,res))

    m = MLPictureGen()
    m.capture_on_two_click('open_gift_page', './PokemonGo/images/FriendGifting/')
    m.capture_on_two_click('gift_received_profile', './PokemonGo/images/FriendGifting/')
    m.capture_on_two_click('can_send_gift_profile', './PokemonGo/images/FriendGifting/')
    time.sleep(100)




    # while True:
    #     m.test_image('./PokemonGo/images/FriendGifting/', 'can_send_gift_profile')
    # time.sleep(100)


if __name__ == '__main__':
    main()
# {'on_msg': {'args': ('hello world',), 'kwargs': {}, -1: [], 10: [<bound method GenericCardTemplate.<locals>.GenericCard.__generic_callback_template.<locals>.__generic_callback of <CardPrototyping.card_Human.Human.Human object at 0x7fb7320687b8>>], 5: [<bound method GenericCardTemplate.<locals>.GenericCard.__generic_callback_template.<locals>.__generic_callback of <CardPrototyping.card_Human.Human.Human object at 0x7fb7320686a0>>], 'returned_args': [None]}}
