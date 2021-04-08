from .ADB import ADBManager

android_phone = ADBManager()
android_phone.start_capture('android1')
