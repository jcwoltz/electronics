"""
SNARF-BASE-testing.py   - Main script to test built in devices on board and
                        - pinwake by rtc on RF100/200

CC BY 3.0  J.C. Woltz
http://creativecommons.org/licenses/by/3.0/

v201103062335 - Too many mods to log
v201103171943 - Set initial Portal Address to none. Add set_portal_addr() function
                Add the zCalcWakeTime1() function. 
v201103191511 - Would not compile without a portalAddr. So set portal as 1 and left
                Function to change portal addr.
v201103272322 - testing plotlq rpc call, modfied arguments
v201104021650 - Branch SNARF-BASE-testing, modify for LOCATION at ESCO With ATMEGA
v201104041240 - Added devname everywhere. modified jc_m and portal to diplay more info about when it will wakeup

"""

from synapse.platforms import *
from synapse.switchboard import *
from synapse.pinWakeup import *
from pcf2129a_m import *
from lm75a_m import *
from m24lc256_m import *
from jc_m import *

portalAddr = '\x00\x00\x01' # hard-coded address for Portal <------------<<<<<<<<
e10Addr = '\x4c\x70\xbd'
#portal_addr = None
secondCounter = 0 
minuteCounter = 0
datablock = 1
taddress = 8000
jcdebug = True

#These are the GPIO pins used on the SNARF-BASE v3.h
VAUX = GPIO_5
RTC_INT = GPIO_10
LED1 = GPIO_0

@setHook(HOOK_STARTUP)
def start():    
    global devName, devType
    global taddress
    #global Dname, Dtype
    devType = str(loadNvParam(10))
    devName = str(loadNvParam(8))
    setPinDir(LED1, True)
    # Setup the Auxilary Regulator for sensors:
    setPinDir(VAUX, True)       #output
    writePin(VAUX, True)        #Turn on aux power
    # Setup the RTC Interrupt pin
    setPinDir(RTC_INT, False)   #Input
    setPinPullup(RTC_INT, True) #Turn on pullup
    monitorPin(RTC_INT, True)   #monitor changes to this pin. Will go low on int
    wakeupOn(RTC_INT, True, False)  #Wake from sleep when pin goes low
    
    # I2C GPIO_17/18 rf100. rf200 needs external pullups.
    i2cInit(True)
    # On startup try to get the portal address. 
    #if portalAddr is None:
    #    mcastRpc(1, 5, "get_portal_logger")
    #else:
    #    getPortalTime()
    # Go ahead and redirect STDOUT to Portal now
    ucastSerial(portalAddr) # put your correct Portal address here!
    # send errors to portal
    uniConnect(DS_PACKET_SERIAL, DS_ERROR)
    
    getPortalTime()
    
    initUart(1,38400)
    flowControl(1,False)
    stdinMode(0, False)      # Line Mode, Echo Off
    crossConnect(DS_UART1,DS_STDIO)
    #taddress = int(readEEPROM(59,5))
    #sleep(1,3)
    #Check if rtc has invalid year, if so, automatically update rtc from portal
    #This is not a very robust check, but work for testing.
    checkClockYear()
    
    #print "Startup Done!"
    
@setHook(HOOK_100MS)
def timer100msEvent(msTick):
    """Hooked into the HOOK_100MS event"""
    global secondCounter, minuteCounter
    pulsePin(LED1, 50, True)
    secondCounter += 1
    #pulsePin(LED1, 50, True)
    if secondCounter >= 100:
        doEverySecond()
        secondCounter = 0
        minuteCounter += 1
        #zCalcWakeTime1()
    if minuteCounter >= 60:
        doEveryMinute()
        minuteCounter = 0
    #if secondCounter == 70:
    #    zCalcWakeTime10info()
    #    savelastwritelocation()
    #if secondCounter == 100:
    #    tt = str(readEEPROM(59,5))
    #    rpc(portalAddr, "dispayLastWriteAddress", tt)
    #if secondCounter >= 300:
    #    secondCounter = 0
    #     writePin(LED1, False)
    #     sleep(0,0)
    
    
def doEverySecond():
    #Since the uart is crossconnected, this goes out over the uart
    global taddress
    dts = str(displayClockDT())
    eventString = devName + "," + dts + "," + str(taddress)  #+ str(displayLMTempF()) #+ chr(0x03) + dts #"," + str(displayLMTemp()) + "," + str(taddress)
    #eventString = dts + "," + str(displayLMTempF())
    print eventString
    taddress += 1
    #rpc(portalAddr, "plotlqwx", Dname, getLq(), displayClockDT())
    #rpc(portalAddr, "infoDT", displayClockDT())
    #print displayClockDT()
    #sleep(0,1)
    
    
def doEveryMinute():
    dts = str(displayClockDT())
    eventString = devName + ":" + dts + "," + str(displayLMTempF()) + "," + str(displayLMTemp())
    rpc(e10Addr, "reportJC", devName, devType, eventString)
    

def logLocal():
    global datablock
    #address = datablock * 64
    global taddress
    
    #For testing, we log clockdate and time, temp C, temp F to half a page of eeprom
    eventString = str(displayClockDT()) + "," + str(displayLMTemp()) + "," + str(displayLMTempF()) + ",EOB"
    t = len(eventString)
    if (t < 32):
        index = t
        while (index < 32):
            eventString = eventString + "0"
            index += 1
    tt = len(eventString)
    writeEEblock(taddress, eventString)

    eventString = devName + ": " + eventString + " " + str(t) + " " + str(taddress) + " " + str(tt)
    rpc(portalAddr, "logEvent", eventString)
    #if (t < 32):
    #    t = 32
    taddress += tt
    datablock += 1
    
    return getI2cResult()
    
@setHook(HOOK_GPIN)
def buttonEvent(pinNum, isSet):
    """Hooked into the HOOK_GPIN event"""
    #mostly debug and pointless irw
    if (jcdebug):
        print str(pinNum),
        print str(isSet)
        eventString = devName + ": HOOK_GPIN: " + str(pinNum) + " " + str(isSet)
        rpc(portalAddr, "logEvent", eventString)
    
def testLogE():
    eventString = devName + " Start: " + str(displayClockDT()) + ",EOB"
    t = len(eventString)
    #writeEEblock(taddress, eventString)
    writeEEblock(0, eventString)
    String2 = str(getI2cResult()) + " " + str(t)
    return String2


def turnONVAUX():
    writePin(VAUX, True)       #Turn on aux power 

def turnOFFVAUX():
    writePin(VAUX, False)      #Turn off aux power

def set_portal_addr():
    """Set the portal SNAP address to the caller of this function"""
    global portalAddr
    portalAddr = rpcSourceAddr()
    getPortalTime()

def savelastwritelocation():
    global taddress
    if (taddress < 100):
        tt = "000" + str(taddress)
    elif (taddress < 1000):
        tt = "00" + str(taddress)
    elif (taddress < 10000):
        tt = "0" + str(taddress)
    else:
        tt = str(taddress)
    writeEEblock(59, tt)
    return tt

def echo(text):
    print str(text)
    
@setHook(HOOK_STDIN)
def getInput(data):
    ''' Process command line input '''
    c = data[0]
    if c == 'r':
        print "rrrr"
    rpc(portalAddr, "logEvent", data)