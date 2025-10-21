'''         初始    稳定拉高    按下抖动    稳定下拉(tail执行2次)   松开抖动    稳定拉高(此刻tail=1)    再执行一次tail=0正好isPressed=0    
val         1       1           return      0                0    return       1                    1
isPressed   0       0           return    0=val*last_isDown  0    return     1=val*last_isDown      0
isDown      0       0           return    1(update_isDown)   1    return       0                    0
'''
import time
time.sleep(0.1) # Wait for USB to become ready
print("Hello, Pi Pico!")
from machine import Pin
class Button:
    def __init__(self,pin,debounce=20):
        self.pin = Pin(pin,Pin.IN,Pin.PULL_UP)
        self.db   = debounce
        self.last = 1
        self.tick = 0
        self.isDown = 0
        self.isPressed = 0
        self.tail = 0
    def update(self): 
        val = self.pin.value()
        if val^self.last:
            self.last = val
            self.tick = time.ticks_ms()
            self.tail = 2
            return
        if self.tail and time.ticks_diff(time.ticks_ms(),self.tick) > self.db:
            self.isPressed = self.last * self.isDown
            self.isDown = not self.last
            self.tail -= 1
class Switch(Button):
    def __init__(self,pin,debounce = 20,long_ms = 800,double_ms = 300):
        super().__init__(pin,debounce)
        self.isLongPressed = 0
        self.isDoubleClick = 0
        self.clickTick = 0
        self.clickCount = 0
        self.long_ms   = long_ms
        self.double_ms = double_ms
        self.trig = 1
    def update(self):
        val = self.pin.value()
        self.isPressed = 0
        self.isDoubleClick = 0
        self.isLongPressed = 0
        self.isDown = not self.last
        if val^self.last:
            self.last = val
            self.tick = time.ticks_ms()
            self.tail = 1^val
            self.trig = 1^val
            return
        if self.tail and time.ticks_diff(time.ticks_ms(),self.tick) > self.db:
            if time.ticks_diff(time.ticks_ms(),self.tick) > 800:
                self.isLongPressed = 1
                self.clickCount = 0
                self.tail = 0
                return
            if self.trig:
                self.trig = 0
                self.clickCount += 1
                self.clickTick = self.tick
            if self.clickCount==2:
                self.isDoubleClick = 1
                self.clickCount = 0
                return
        if self.clickCount and self.last and time.ticks_diff(time.ticks_ms(),self.clickTick) > 300:
            self.isPressed = 1
            self.clickCount = 0
# if __name__ == "__main__":
#     key = Switch(22)
#     num = 0
#     while 1:
#         key.update()
#         if key.isPressed:print("is pressed")
#         if key.isLongPressed:print("long presses")
#         if key.isDoubleClick:print("double click")
#         time.sleep_ms(1)
