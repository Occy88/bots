adb shell dumpsys window windows| sed -n '/Window .*StatusBar.*:/,/Window .*:/p'| grep 'Requested' |grep h
