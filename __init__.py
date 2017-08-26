import ugfx
import badge
#import esp
import wifi
import time
import usocket as socket
import appglue

HOST = 'bananapi'
PORT = 6600
#PASSWORD = 'password'

def show (str1="",str2="",str3="",str4="",str5=""):
  ugfx.clear(ugfx.BLACK)
  ugfx.string(15, 5, str1, "Roboto_Regular12", ugfx.WHITE)
  ugfx.string(15, 20, str2, "Roboto_Regular12", ugfx.WHITE)
  ugfx.string(15, 35, str3, "Roboto_Regular12", ugfx.WHITE)
  ugfx.string(15, 50, str4, "Roboto_Regular12", ugfx.WHITE)
  ugfx.string(15, 65, str5, "Roboto_Regular12", ugfx.WHITE)
  ugfx.flush()

def connect():
  try:
    show("Connecting to socket","on",HOST)
    s = socket.socket()
    s.connect(socket.getaddrinfo(HOST, PORT)[0][-1])
    try:
      reply = s.recv(4096).decode('utf-8')
      show("MPD version",reply.replace("OK ",""),"")
      return s
    except:
      return None
  except:
    return None

def mpdCommand ( command ):
  s.send(command + " \n")
  reply = s.recv(4096).decode('utf-8')
  return reply

def showMain ():
  #currentsong part
  reply = mpdCommand("currentsong")
  replylines = reply.split('\n')[:-2]
  mySongDict = dict( (line.split(": ", 1)) for line in replylines)
  if not 'Artist' in mySongDict:
    myArtist = ""
  else:
    myArtist = mySongDict['Artist']
  if not 'Title' in mySongDict:
    myTitle = ""
  else:
    myTitle = mySongDict['Title']
  if not 'file' in mySongDict:
    myFile = ""
  else:
    myFile = mySongDict['file']
  #status part
  global myRandom
  global myRepeat
  reply = mpdCommand("status")
  replylines = reply.split('\n')[:-2]
  myStatusDict = dict( (line.split(": ", 1)) for line in replylines)
  if not 'volume' in myStatusDict:
    myVolume = ""
  else: myVolume = myStatusDict['volume']
  if not 'random' in myStatusDict:
    myRandom = "unknown"
  else:
    if myStatusDict['random'] == '1':
      myRandom = "On"
    else:
      myRandom = "Off"
  if not 'repeat' in myStatusDict:
    myRepeat = "unknown"
  else:
    if myStatusDict['repeat'] == '1':
      myRepeat = "On"
    else:
      myRepeat = "Off"
  #draw result
  show( "Vol: " + myVolume + " Repeat: " + myRepeat + " Random: " + myRandom,
 myArtist , myTitle , myFile )

def vol_up (pushed):
  if pushed:
    mpdCommand("volume 5")
    showMain()
    print("vol_up")
def vol_down(pushed):
  if pushed:
    mpdCommand("volume -5")
    showMain()
    print("vol_down")
def prev(pushed):
  if pushed:
    mpdCommand("previous")
    showMain()
    print("previous song")
def nxt(pushed):
  if pushed:
    mpdCommand("next")
    showMain()
    print("next song")
#def select(pushed):
#Start button
def return_home(pushed):
  if pushed:
    print("returning home")
    appglue.home()
#A button
def toggle_random(pushed):
  if pushed:
    if myRandom == "Off":
      mpdCommand("random 1")
      showMain()
      print("turned random on")
    else:
      mpdCommand("random 0")
      showMain()
      print("turned random off")
#B button
def toggle_repeat(pushed):
  if pushed:
    if myRepeat == "Off":
      mpdCommand("repeat 1")
      showMain()
      print("turned repeat on")
    else:
      mpdCommand("repeat 0")
      showMain()
      print("turned repeat off")

badge.init()
ugfx.init()
ugfx.input_init()
wifi.init()

ugfx.input_attach(ugfx.JOY_UP, vol_up)
ugfx.input_attach(ugfx.JOY_DOWN, vol_down)
ugfx.input_attach(ugfx.JOY_LEFT, prev)
ugfx.input_attach(ugfx.JOY_RIGHT, nxt)
#ugfx.input_attach(ugfx.BTN_SELECT, select)
ugfx.input_attach(ugfx.BTN_START, return_home)
ugfx.input_attach(ugfx.BTN_A, toggle_random)
ugfx.input_attach(ugfx.BTN_B, toggle_repeat)

show("Connecting","teh","wifis")
while not wifi.sta_if.isconnected():
  time.sleep(0.1)
s = connect()
reply = mpdCommand("currentsong")
if "permission" in reply:
  try:
    if PASSWORD and len(PASSWORD) > 0:
      reply = mpdCommand("password " + PASSWORD )
      if reply.strip() == "OK":
        show("Password accepted")
      else:
        show("Password not accepted","","Exiting...")
        time.sleep(3)
        appglue.home()
  except:
    pass

while 1:
  showMain()
  time.sleep(10)

s.close()

