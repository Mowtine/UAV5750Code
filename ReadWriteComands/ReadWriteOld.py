import threading
import time

try:
    import pigpio
except:
    print("Problem importing pigpio")


class Reader:

    def __init__(self, name, port, GPIO):

        self.pi = GPIO
        self.name = name
        self.port = port
        self.values = [5, 0, 3, 0]
        self.read = True
        self.stream = []
        try:
            if not self.pi.connected:
                print("GPIOs not connected")
        except Exception as e:
            print(e)
        self._lock = threading.Lock()

    def ReaderThread(self, name):
        print('I am reading now and saving values to Values')
        while self.read:
            ### TODO: this is where we will be repeating until we have enough
            ### bites to read a signal and decode it
            with self._lock:
                print("Reading in " + name)
                values = self.GetValues()
                print("Saving in " + name)
                self.SaveValues(values)
            time.sleep(1)

    def SaveValues(self, listToSave):
        self.values = listToSave

    def GetValues(self):
        ### TODO: this is where we need to read the controller values.
        return self.values

    def run(self):

        dataThread = threading.Thread( target = self.ReaderThread, args = ("Reader Thread", ))
        dataThread.start()

        return dataThread

    def Stop(self):
        self.read = False

class Writer:

    def __init__(self, name, port, GPIO):

        self.pi = GPIO
        self.name = name
        self.port = port
        self.values = [5, 0, 3, 0]
        self.write = True
        self.stream = []
        try:
            if not self.pi.connected:
                print("GPIOs not connected")
        except Exception as e:
            print(e)
        self._lock = threading.Lock()

    def WriterThread(self, name):
        print('I am writing now to pins')

        while self.write:

            with self._lock:
                ## TODO: change the pins to be the current output
                print("Writing in " + name)
                self.WriteValues(self.values)
            time.sleep(1)
        try:
            for i in range(len(values)):
                # By default PWM is from 0 - 255
                self.pi.set_PWM_dutycycle(self.port[i], 0)
        except Exception as e:
            print("Error writing to pin")
            print(e)

    def SaveValues(self, listToSave):
        self.values = listToSave

    def WriteValues(self, values):
        print("Writing: " + str(values))
        try:
            for i in range(len(values)):
                # By default PWM is from 0 - 255
                self.pi.set_PWM_dutycycle(self.port[i], int(values[i]*255))
        except Exception as e:
            print("Error writing to pin")
            print(e)

    def run(self):

        dataThread = threading.Thread( target = self.WriterThread, args = ("Writer Thread", ))
        dataThread.start()

        return dataThread

    def Stop(self):
        self.write = False

def main():
    reader = Reader("input",8000)

    readerThread = threading.Thread(target=reader.ReaderThread, args=("Thread1",))
    readerThread.start()
    time.sleep(2)
    print(reader.values)
    print("Ending main function and ending thread")
    reader.read = False



if __name__ == "__main__":
    main()
