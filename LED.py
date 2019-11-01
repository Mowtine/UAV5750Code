import RPi.GPIO as GPIO    # Import Raspberry Pi GPIO library
from time import sleep     # Import the sleep function from the time module
import threading

class LED:

    def __init__(self):

        self.mode = 0
        self.LEDon = True
        self.GPIOport = 8
        GPIO.setwarnings(False)    # Ignore warning for now
        GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
        GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off). Change pin # if necessary

    def ChangeMode(self, mode):
        self.mode = mode

    def stop(self):
        self.LEDon = False

    def Lights(self, name):
        while self.LEDon:
            if self.mode == 1: # Run forever | CHANGE TO 'WHILE IN SEMI-MANUAL MODE' (-_-_-_-_)
                GPIO.output(8, GPIO.HIGH) # Turn on
                sleep(1)                  # Sleep for 1 second
                GPIO.output(8, GPIO.LOW)  # Turn off
                sleep(1)                  # Sleep for 1 second

            elif self.mode == 2: # Run forever | CHANGE TO 'WHILE IN WAYPOINT MODE' (--__--__--__)
                GPIO.output(8, GPIO.HIGH) # Turn on
                sleep(0.25)                  # Sleep for 0.25 seconds
                GPIO.output(8, GPIO.LOW)  # Turn off
                sleep(0.25)                  # Sleep for 0.25 seconds
                GPIO.output(8, GPIO.HIGH) # Turn on
                sleep(0.25)                  # Sleep for 0.25 seconds
                GPIO.output(8, GPIO.LOW)  # Turn off
                sleep(2.25)                  # Sleep for 2.25 seconds

            elif self.mode == 0: # Run forever | CHANGE TO 'WHILE IN MANUAL MODE' (------)
            	GPIO.output(8, GPIO.HIGH) # Turn on

    def run(self):
        dataThread = threading.Thread( target = self.Lights, args = ("LED Thread", ))
        dataThread.start()

        return dataThread

def main():
    LEDclas = LED()
    LEDclas.run()

if __name__ == "__main__":
    main()
