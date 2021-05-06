# This functionality of getch() is needed in the input.py file because, taking
# input character by character let us examine what command the user is trying
# to enter. Once we predicted that we come up with suggestions on the terminal,
# basically I want to implement a command completion tool for linkedin-bot.
#
# This implementation of getch() function became more easy with the help of the
# user Phylliida who has posted a solution on stackoverflow,
# see https://stackoverflow.com/a/31749681/13910122

import threading


class _Getch:
    """Gets a single character from standard input. Does not echo to the screen. 
    From http://code.activestate.com/recipes/134892/
    """

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            try:
                self.impl = _GetchMacCarbon()
            except(AttributeError, ImportError):
                self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty
        import sys
        import termios

    def __call__(self):
        import sys
        import tty
        import termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt

        return msvcrt.getch()


class _GetchMacCarbon:
    """A function which returns the current ASCII key that is down; if no ASCII 
    key is down, the null string is returned. 

    The page http://www.mactech.com/macintosh-c/chap02-1.html was very helpful in 
    figuring out how to do this.
    """

    def __init__(self):
        import Carbon

        Carbon.Evt

    def __call__(self):
        import Carbon

        if Carbon.Evt.EventAvail(0x0008)[0] == 0:  # 0x0008 is the keyDownMask
            return ''

        # The event contains the following info:
        # (what, msg, when, where, mod) = Carbon.Evt.GetNextEvent(0x0008)[1]
        #
        # The message (msg) contains the ASCII char which is extracted with the
        # 0x000000FF charCodeMask; this number is converted to an ASCII character
        # with chr() and returned.
        (what, msg, when, where, mod) = Carbon.Evt.GetNextEvent(0x0008)[1]

        return chr(msg & 0x000000FF)


class Event(list):
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)


def getch():
    _getch = _Getch()

    import sys

    for i in range(sys.maxsize):
        ch = _getch()
        if k != '':
            break

    return ch


class KeyCallbackFunction():
    callbackParam = None
    actualFunction = None

    def __init__(self, actualFunction, callbackParam):
        self.actualFunction = actualFunction
        self.callbackParam = callbackParam

    def doCallback(self, inputKey):
        if self.actualFunction is None:
            return

        if self.callbackParam is None:
            callbackFunctionThread = threading.Thread(
                target=self.actualFunction, args=(inputKey,))
        else:
            callbackFunctionThread = threading.Thread(
                target=self.actualFunction, args=(inputKey, self.callbackParam))

        callbackFunctionThread.daemon = True
        callbackFunctionThread.start()


class KeyCapture():
    """Class KeyCapture"""
    gotKeyLock = threading.Lock()
    gotKeys = []
    gotKeyEvent = threading.Event()

    keyBlockingSetKeyLock = threading.Lock()

    addingEventsLock = threading.Lock()
    keyReceiveEvents = Event()

    keysGotLock = threading.Lock()
    keysGot = []

    keyBlockingKeyLockLossy = threading.Lock()
    keyBlockingKeyLossy = None
    keyBlockingEventLossy = threading.Event()

    keysBlockingGotLock = threading.Lock()
    keysBlockingGot = []
    keyBlockingGotEvent = threading.Event()

    wantToStopLock = threading.Lock()
    wantToStop = False

    stoppedLock = threading.Lock()
    stopped = True

    isRunningEvent = False

    getKeyThread = None

    keyFunction = None
    keyArgs = None

    def startCapture(self, keyFunction=None, args=None):
        """Begin capturing keys. A seperate thread is launched that captures 
        key presses, and then these can be received via get, getAsync, and 
        adding an event via addEvent. Note that this will prevent the system 
        to accept keys as normal (say, if you are in  a python shell) because 
        it overrides that key capturing behavior.

        If you start capture when it's already been started, a 
        InterruptedError("Keys are still being captured") will be thrown.

        Note that get(), getAsync() and events are independent, so if a key 
        is pressed:

        1: Any calls to get() that are waiting, with lossy on, will return that 
            key.
        2: It will be stored in the queue of get keys, so that get() with lossy 
            off will return the oldest key pressed not returned by get() yet.
        3: All events will be fired with that key as their input.
        4: It will be stored in the list of getAsync() keys, where that list 
            will be returned and set to empty list on the next call to getAsync().

        get() call with it, aand add it to the getAsync() list.
        """

        """Make sure we aren't already capturing keys."""
        self.stoppedLock.acquire()

        if not self.stopped:
            self.stoppedLock.release()
            raise InterruptedError("Keys are still being captured")

        self.stopped = False
        self.stoppedLock.release()

        # If we have captured before, we need to allow the get() calls to actually
        # wait for key presses now by clearing the event.
        if self.keyBlockingEventLossy.is_set():
            self.keyBlockingEventLossy.clear()

        # Have one function that we call every time a key is captured, intended
        # for stopping capture as desired.
        self.keyFunction = keyFunction
        self.keyArgs = args

        # Begin capturing keys (in a seperate thread).
        self.getKeyThread = threading.Thread(
            target=self._threadProcessKeyPresses)
        self.getKeyThread.daemon = True
        self.getKeyThread.start()

        # Process key captures (in a seperate thread).
        self.getKeyThread = threading.Thread(
            target=self._threadStoreKeyPresses)
        self.getKeyThread.daemon = True
        self.getKeyThread.start()

    def capturing(self):
        self.stoppedLock.acquire()
        isCapturing = not self.stopped
        self.stoppedLock.release()

        return isCapturing

    def stopCapture(self):
        """Stops the thread that is capturing keys on the first opporunity 
        has to do so. It usually can't stop immediately because getting a key 
        is a blocking process, so this will probably stop capturing after the 
        next key is pressed.

        However, Sometimes if you call stopCapture it will stop before 
        starting capturing the next key, due to multithreading race conditions. 
        So if you want to stop capturing reliably, call stopCapture in a function 
        added via addEvent. Then you are guaranteed that capturing will stop 
        immediately after the rest of the callback functions are called (before 
        starting to capture the next key).
        """
        self.wantToStopLock.acquire()
        self.wantToStop = True
        self.wantToStopLock.release()

    def addEvent(self, keyPressEventFunction, args=None):
        """Takes in a function that will be called every time a key is pressed 
        (with that key passed in as the first paramater in that function).
        """
        self.addingEventsLock.acquire()
        callbackHolder = KeyCallbackFunction(keyPressEventFunction, args)
        self.keyReceiveEvents.append(callbackHolder.doCallback)
        self.addingEventsLock.release()

    def clearEvents(self):
        self.addingEventsLock.acquire()
        self.keyReceiveEvents = Event()
        self.addingEventsLock.release()

    def get(self, lossy=False):
        """Gets a key captured by this KeyCapture, blocking until a key is pressed.

        There is an optional lossy paramater:
        If True all keys before this call are ignored, and the next pressed key will 
            be returned.
        If False this will return the oldest key captured that hasn't been returned 
            by get yet. 

        False is the default.
        """
        if lossy:
            self.keyBlockingEventLossy.wait()
            self.keyBlockingKeyLockLossy.acquire()
            keyReceived = self.keyBlockingKeyLossy
            self.keyBlockingKeyLockLossy.release()

            return keyReceived

        while True:
            self.keyBlockingGotEvent.wait()
            readKey = None
            self.keysBlockingGotLock.acquire()

            if len(self.keysBlockingGot) != 0:
                readKey = self.keysBlockingGot.pop(0)

            if len(self.keysBlockingGot) == 0:
                self.keyBlockingGotEvent.clear()

            self.keysBlockingGotLock.release()

            if not readKey is None:
                return readKey

            self.wantToStopLock.acquire()

            if self.wantToStop:
                self.wantToStopLock.release()
                return None

            self.wantToStopLock.release()

    def clearGetList(self):
        self.keysBlockingGotLock.acquire()
        self.keysBlockingGot = []
        self.keysBlockingGotLock.release()

    def getAsync(self):
        """Gets a list of all keys pressed since the last call to getAsync, in order
        from first pressed, second pressed, .., most recent pressed.
        """
        self.keysGotLock.acquire()

        keysPressedList = list(self.keysGot)
        self.keysGot = []
        self.keysGotLock.release()

        return keysPressedList

    def clearAsyncList(self):
        self.keysGotLock.acquire()
        self.keysGot = []
        self.keysGotLock.release()

    def _processKey(self, readKey):
        self.keysGotLock.acquire()
        self.keysGot.append(readKey)
        self.keysGotLock.release()

        self.keyBlockingKeyLockLossy.acquire()
        self.keyBlockingKeyLossy = readKey
        self.keyBlockingEventLossy.set()
        self.keyBlockingEventLossy.clear()
        self.keyBlockingKeyLockLossy.release()

        self.keysBlockingGotLock.acquire()
        self.keysBlockingGot.append(readKey)

        if len(self.keysBlockingGot) == 1:
            self.keyBlockingGotEvent.set()

        self.keysBlockingGotLock.release()

        self.addingEventsLock.acquire()
        self.keyReceiveEvents(readKey)
        self.addingEventsLock.release()

    def _threadProcessKeyPresses(self):
        while True:
            self.gotKeyEvent.wait()
            readKey = None
            self.gotKeyLock.acquire()

            if len(self.gotKeys) != 0:
                readKey = self.gotKeys.pop(0)

            if len(self.gotKeys) == 0:
                self.gotKeyEvent.clear()

            self.gotKeyLock.release()

            if not readKey is None:
                self._processKey(readKey)

            self.wantToStopLock.acquire()

            if self.wantToStop:
                self.wantToStopLock.release()
                break

            self.wantToStopLock.release()

    def _threadStoreKeyPresses(self):
        while True:
            readKey = getch()

            if not self.keyFunction is None:
                self.keyFunction(readKey, self.keyArgs)

            self.gotKeyLock.acquire()
            self.gotKeys.append(readKey)

            if len(self.gotKeys) == 1:
                self.gotKeyEvent.set()

            self.gotKeyLock.release()

            self.wantToStopLock.acquire()

            if self.wantToStop:
                self.wantToStopLock.release()
                self.gotKeyEvent.set()
                break

            self.wantToStopLock.release()

        # If we have reached here we stopped capturing.
        #
        # All we need to do to clean up is ensure that all the calls to .get()
        # now return None. To ensure no calls are stuck never returning, we will
        # leave the event set so any tasks waiting for it immediately exit. This
        # will be unset upon starting key capturing again.
        self.stoppedLock.acquire()

        # We also need to set this to True so we can start up capturing again.
        self.stopped = True
        self.stopped = True

        self.keyBlockingKeyLockLossy.acquire()
        self.keyBlockingKeyLossy = None
        self.keyBlockingEventLossy.set()
        self.keyBlockingKeyLockLossy.release()

        self.keysBlockingGotLock.acquire()
        self.keyBlockingGotEvent.set()
        self.keysBlockingGotLock.release()

        self.stoppedLock.release()
