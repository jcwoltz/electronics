"""
CC BY 3.0  J.C. Woltz
http://creativecommons.org/licenses/by/3.0/

import as module. just quick common functions between scrtips.  primarily different example alarm settings
v201207141403 - old file, new modularization.
Clock sleep times are not built to sleep for more than 59 minutes. This can be extended if you need to.

"""

    
def zCalcWakeTime10():
    """Set the RTC INT to triger at the next 10 minute interval"""
    # This is an abbreviated part of displayClockTime retrieving
    # only the current seconds and minutes.
    buff = readPCF2129(0x03,7)
    
    Seconds = bcdToDec(ord(buff[0]) & 0x7F)
    Minutes = bcdToDec(ord(buff[1]) & 0x7F)
    Hours = bcdToDec(ord(buff[2]) & 0x3F)
    Days = bcdToDec(ord(buff[3]) & 0x3F)
    DOW = bcdToDec(ord(buff[4]) & 0x07)
    Months = bcdToDec(ord(buff[5]) & 0x1F)
    Years = bcdToDec(ord(buff[6]))
    
    Minutes += 10
    Minutes = Minutes / 10
    Minutes = Minutes * 10
    if (Minutes > 50):
        Minutes = 0
    Seconds = 0
    writeClockAlarm(Minutes, 0)
    reportWakeTime(Years,Months,Days,DOW,Hours,Minutes,Seconds)
    writeClockAlarm(Minutes, 0)
    
    return str(Minutes)

def zCalcWakeTime1():
    """Set the RTC INT to triger in one minute, then goto sleep"""
    # This is an abbreviated part of displayClockTime retrieving
    # only the current seconds and minutes.
    buff = readPCF2129(0x03,7)
    
    Seconds = bcdToDec(ord(buff[0]) & 0x7F)
    Minutes = bcdToDec(ord(buff[1]) & 0x7F)
    Hours = bcdToDec(ord(buff[2]) & 0x3F)
    Days = bcdToDec(ord(buff[3]) & 0x3F)
    DOW = bcdToDec(ord(buff[4]) & 0x07)
    Months = bcdToDec(ord(buff[5]) & 0x1F)
    Years = bcdToDec(ord(buff[6]))
    
    Minutes += 1
    #Minutes = Minutes / 10
    #Minutes = Minutes * 10
    if (Minutes > 59):
        Minutes = 0
    writeClockAlarm(Minutes, Seconds)
    reportWakeTime(Years,Months,Days,DOW,Hours,Minutes,Seconds)
    writeClockAlarm(Minutes, Seconds)
    
    return str(Minutes)

def zCalcWakeTime5():
    """Set the RTC INT to triger in five minute, then goto sleep"""
    # This is an abbreviated part of displayClockTime retrieving
    # only the current seconds and minutes.
    buff = readPCF2129(0x03,7)
    
    Seconds = bcdToDec(ord(buff[0]) & 0x7F)
    Minutes = bcdToDec(ord(buff[1]) & 0x7F)
    Hours = bcdToDec(ord(buff[2]) & 0x3F)
    Days = bcdToDec(ord(buff[3]) & 0x3F)
    DOW = bcdToDec(ord(buff[4]) & 0x07)
    Months = bcdToDec(ord(buff[5]) & 0x1F)
    Years = bcdToDec(ord(buff[6]))
    
    Minutes += 5
    #Minutes = Minutes / 10
    #Minutes = Minutes * 10
    if (Minutes > 59):
        #Minutes = 0
        Minutes = Minutes - 60
    writeClockAlarm(Minutes, Seconds)
    reportWakeTime(Years,Months,Days,DOW,Hours,Minutes,Seconds)
    writeClockAlarm(Minutes, Seconds)
    return Minutes

def zCalcWakeTime10info():
    """Set the RTC INT to triger at the next 10 minute interval"""
    # This is an abbreviated part of displayClockTime retrieving
    # only the current seconds and minutes.
    buff = readPCF2129(0x03,7)
    
    Seconds = bcdToDec(ord(buff[0]) & 0x7F)
    Minutes = bcdToDec(ord(buff[1]) & 0x7F)
    Hours = bcdToDec(ord(buff[2]) & 0x3F)
    Days = bcdToDec(ord(buff[3]) & 0x3F)
    DOW = bcdToDec(ord(buff[4]) & 0x07)
    Months = bcdToDec(ord(buff[5]) & 0x1F)
    Years = bcdToDec(ord(buff[6]))
    
    Minutes += 10
    Minutes = Minutes / 10
    Minutes = Minutes * 10
    if (Minutes > 59):
        Minutes = 0
        Hours += 1
    if (Hours > 23):
        Hours = 0
        Days += 1
        DOW += 1
    Seconds = 0
    writeClockAlarm(Minutes, Seconds)
    reportWakeTime(Years,Months,Days,DOW,Hours,Minutes,Seconds)
    writeClockAlarm(Minutes, Seconds)
    return str(Minutes)

def zCalcWakeTime2info():
    """Set the RTC INT to triger at the next 2 minute interval"""
    # This is an abbreviated part of displayClockTime retrieving
    # only the current seconds and minutes.
    buff = readPCF2129(0x03,7)
    
    if (getI2cResult() == 1):
        Seconds = bcdToDec(ord(buff[0]) & 0x7F)
        Minutes = bcdToDec(ord(buff[1]) & 0x7F)
        Hours = bcdToDec(ord(buff[2]) & 0x3F)
        Days = bcdToDec(ord(buff[3]) & 0x3F)
        DOW = bcdToDec(ord(buff[4]) & 0x07)
        Months = bcdToDec(ord(buff[5]) & 0x1F)
        Years = bcdToDec(ord(buff[6]))
    
        Minutes += 2
        if (Minutes > 59):
            Minutes = Minutes - 60
            Hours += 1
        if (Hours > 23):
            Hours = 0
            Days += 1
            DOW += 1
        Seconds = 0
    
        if (writeClockAlarm(Minutes, Seconds) == 1):
            reportWakeTime(Years,Months,Days,DOW,Hours,Minutes,Seconds)
        else:
            writeClockAlarm(Minutes, Seconds)
    
        return str(Minutes)
    else:
        eventString = "Failed: " + str(getI2cResult())
        return eventString

def zCalcWakeTimeinfo(pMinutes):
    """Set the RTC INT to triger at the next pMinutes interval"""
    buff = readPCF2129(0x03,7)
    
    if (getI2cResult() == 1):
        Seconds = bcdToDec(ord(buff[0]) & 0x7F)
        Minutes = bcdToDec(ord(buff[1]) & 0x7F)
        Hours = bcdToDec(ord(buff[2]) & 0x3F)
        Days = bcdToDec(ord(buff[3]) & 0x3F)
        DOW = bcdToDec(ord(buff[4]) & 0x07)
        Months = bcdToDec(ord(buff[5]) & 0x1F)
        Years = bcdToDec(ord(buff[6]))
    
        Minutes += pMinutes
        if (Minutes > 59 and Minutes < 120):
            Minutes = Minutes - 60
            Hours += 1
        if (Hours > 23):
            Hours = 0
            Days += 1
            DOW += 1
        Seconds = 0
    
        if (writeClockAlarm(Minutes, Seconds) == 1):
            reportWakeTime(Years,Months,Days,DOW,Hours,Minutes,Seconds)
        else:
            writeClockAlarm(Minutes, Seconds)
        return str(Minutes)
    else:
        eventString = "Failed: " + str(getI2cResult())
        return eventString

def reportWakeTime(Years,Months,Days,DOW,Hours,Minutes,Seconds):
    """Internal Function used to report to portal when RTC Alarm will trigger wakeup"""
    #eventString = str(loadNvParam(8)) + ": wake at: " + str(Hours) + ":" + str(Minutes) + ":" + str(Seconds)
    #rpc(portalAddr, "logEvent", eventString)
    rpc(portalAddr, "GClockDisplay", "WakeAt",Years,Months,Days,DOW,Hours,Minutes,Seconds)
    
def gotoSleep(Seconds):
    """Verify all conditions are met before sleeping, input is seconds incase RTC fails"""
    if (allowSleep):
        if (jcdebug):
            print secondCounter
        if (timeSynced):
            if (readPin(RTC_INT)):
                sleep(1,Seconds)
            else:
                rpc(portalAddr, "logEvent", "Cannot Sleep Interrupt pin already low")
        else:
            rpc(portalAddr,"logEvent","Cannot sleep time not synchronized")
    else:
        return 0
