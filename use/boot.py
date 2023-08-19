from esp8266_i2c_lcd import I2cLcd
from servo import Servos
from machine import Pin, I2C
import time
import network

serial = ''
pos_para = 0
pos_men = 0
pos_etc = 0

para_box_code = ['736532', '739664', '731618', '731362', '732476', '736289', '733498', '733941', '732624', '736562', '736995', '731945', '732533', '736876', '735195', '736564', '737915', '739584', '736112', '732558', '739517', '737949', '738948', '738619', '732148', '731315', '731535', '736562', '737968', '735533', '732872', '737489', '738139', '736745', '732555', '734383', '735943', '735324', '738813', '733387', '731441', '738227', '734254', '735273', '731718', '734831', '734934', '733983', '735814', '737179', '735413', '731523', '731272', '735494', '738829', '733145', '732965', '737248', '731913', '733515', '733358', '739795', '737166', '733973', '737881', '737474', '736955', '734267', '732714', '737629', '737897', '737139', '734814', '736818', '739244', '734117', '734432', '732557', '738539', '733818', '732462', '732777', '739654', '733524', '733349', '739225', '736819', '733398', '732316', '736958', '732579', '738336', '738435', '736191', '733739', '732744', '736227', '731315', '735689', '734727']
post_box_code = ['767465', '767179', '767328', '767269', '767197', '767128', '767155', '767979', '767338', '767249', '767298', '767547', '767859', '767837', '767316', '767611', '767851', '767422', '767469', '767453', '767481', '767435', '767889', '767967', '767449', '767161', '767922', '767893', '767583', '767663', '767996', '767283', '767799', '767398', '767229', '767265', '767677', '767455', '767262', '767294', '767559', '767334', '767343', '767771', '767411', '767738', '767961', '767338', '767797', '767796', '767197', '767554', '767543', '767873', '767989', '767313', '767439', '767262', '767836', '767955', '767158', '767166', '767283', '767789', '767862', '767793', '767892', '767144', '767162', '767465', '767977', '767599', '767184', '767248', '767439', '767541', '767161', '767114', '767377', '767565', '767786', '767677', '767286', '767151', '767736', '767814', '767267', '767388', '767351', '767742', '767283', '767347', '767481', '767635', '767781', '767681', '767556', '767989', '767673', '767617']

KEYS = [
    ['D', 'C', 'B', 'A'],
    ['#', '9', '6', '3'],
    ['0', '8', '5', '2'],
    ['*', '7', '4', '1']]

COLUMN_BITS = [0b01111111,0b10111111,0b11011111,0b11101111]

def scan_keypad(i2c, addr):
    buf = bytearray(1)
    keys = []
    for row in range(4):
        buf[0] = COLUMN_BITS[ row ]
        i2c.writeto(addr, buf)
        x = i2c.readfrom(addr,1)[0] & 0xf
        if (~x & 0xf) not in [1,2,4,8]:
            continue
        col = -1
        for i in range(4): 
            if (x>>i) & 1 == 0:
                col = (3-i)
                break
        if col >= 0:
            key = KEYS[row][col]
            # print("R{}='{:>04s}'".format(row+1,bin(x)[2:]))
            keys.append(key)
    return keys

def servo_para(pos_para):
    if pos_para == 0:
        return 1
    elif pos_para == 1:
        return 0

def servo_men(pos_men):
    if pos_men == 0:
        return 1
    elif pos_men == 1:
        return 0
    
def servo_etc(pos_etc):
    if pos_etc == 0:
        return 1
    elif pos_etc == 1:
        return 0

i2c = I2C(scl=Pin(5),sda=Pin(4),freq=100000) # i2c for lcd and kaeypad

i2cfs = I2C(scl=Pin(5), sda=Pin(4)) # i2c for servo
servos = Servos(i2cfs) # assign class

lcd = I2cLcd(i2c, 0x27, 2, 16)
lcd.clear()
lcd.putstr(f'Input Serial\n{serial}')
addr = 0x20 #Keypad
try:
    while True:
        keys = scan_keypad(i2c,addr)
        if len(keys) >= 1:
            print(pos_para)
            if keys[0] == 'A':
                lcd.clear()
                lcd.putstr(f'Check data')
                print(serial)
                time.sleep(2)
                if serial in para_box_code:
                    print('im in')
                    pos_para = servo_para(pos_para)
                    print(pos_para)
                    servos.position(0, degrees=pos_para*180)
                elif serial in post_box_code:
                    pos_men = servo_men(pos_men)
                    servos.position(1, degrees=pos_men*180)
                lcd.clear()
                serial = ''
                lcd.putstr(f'Input Serial\n{serial}')
                continue
            print(f"this is a key : {keys[0]}")
            serial += keys[0]
            lcd.clear()
            lcd.putstr(f'Input Serial\n{serial}')
        time.sleep(.5)       
except KeyboardInterrupt:
    pass
finally:
    print('Done')
    lcd.clear()
    print(serial)

