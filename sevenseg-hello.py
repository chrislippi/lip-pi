# This script writes out 'hello aj' to delight the kiddies on Raspberry Pi with Radioshack 7 Segment Display

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

class NumberOutOfRange(Exception):
  """
  This exception is thrown for numbers that are outside the range of values that a
  7 segment display can display.
  """

  def __init__(self, number):
    self.number = number

  def __str__(self):
    return repr("The number %d is outside the range of your 7 segment display" % self.number)

  def __unicode__(self):
    return u"The number %d is outside the range of your 7 segment display" % self.number


class SevenSegmentDisplay():
  """
  This is a class that controls a seven segment display attached to a Raspberry Pi's GPIO headers.
  By default, it's assumed that the pins are wired up in the following way:
  - pin 11 controls segment a (the top one)
  - pin 12 controls segment b (the top right one)
  - pin 13->c, 15->d, 16->e, 18->f, 22->g.
  These outputs are assumed to be active high, i.e. the segment lights up when
  the pin is turned ON.
  """

  # the mapping of numbers to segments needed for displaying that number
  numbers = [
    "abcdef", #0
    "bc",     #1
    "baged",  #2
    "abgcd",  #3
    "bcgf",   #4
    "afgcd",  #5
    "afgcde", #6
    "abc",    #7
    "abcdefg",#8
    "abcdfg", #9
    ]

  letters = [
    "abcefg", #A
    "fedcg",  #b
    "afed",   #C
    "bcdeg",  #d
    "afged",  #E
    "afge",   #F
    "bcefg",  #H    
    "bcde",   #J
    "fed",    #L
    "abefg",  #P
    "bcdef",  #U
    ]

  hello_aj = [
    "bcefg",  #H    
    "",       #blank
    "afged",  #e
    "",       #blank
    "fed",    #L
    "",       #blank
    "fed",    #L
    "",       #blank
    "abcdef", #0
    "",       #blank	 
    "abcefg", #A
    "",       #blank
    "bcde",   #J
    ]

  current_state = None #.. which means off

  # setup
  def __init__(self,
                 segments = {'a': 18, 'b': 23, 'c': 25, 'd': 22, 'e': 27, 'f': 4, 'g': 17 }):
    """
    The "segments" argument contains the pin mapping - please check this every time you set up   
    the RPi for this project
    segments={'a':18', 'b': 23, (etc)}  # a, b etc are the segments, 18, 23 etc are the pin numbers
    """

    self.segments = segments
    for s in self.segments:
      GPIO.setup(self.segments[s], GPIO.OUT)
    self.off()

  def off(self):
    """ turns the 7 segment display off. """
    for s in self.segments:
      GPIO.output(self.segments[s], False)

    #update state
    self.current_state = None

  def set(self, number_to_display):
    """ show some number on the 7 segment display. """

    self.off()
    segments_to_turn_on = self.hello_aj[number_to_display]
    for s in segments_to_turn_on:
      GPIO.output(self.segments[s], True)

    #update state
    self.current_state = number_to_display

# Main loop
# Loop through and spell out the string defined in the SevenSegmentDisplay class
i=0
while i < 13:
    	s=SevenSegmentDisplay()
	s.set(1)
	for i in range(0, 14):
		print("Displaying string position %d" % i)
		s.set(i)
		time.sleep(.25)

GPIO.cleanup()	
   
