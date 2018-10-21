import wiringpi as wiringpi

def set_relay(s1, s2, s3):
     setup = wiringpi.wiringPiSetupGpio()
     if (setup == -1):
         print("setup failed... for wiringpi")
         exit(-1)
     wiringpi.pinMode(2, 1) # sets GPIO 1 ...urrr... 18 ... to output
     wiringpi.pinMode(3, 1) # sets GPIO 2 to output
     wiringpi.pinMode(4, 1) # sets GPIO 3 to output
     # Solenoid connecting to the air tank
     if (s1 == "open" or s1 == "OPEN"):
         # Assume normally closed relay
         wiringpi.digitalWrite(2, 1) # sets port 18 to 1 (3V3, on)
     elif(s1 == "closed" or s1 == "CLOSED"):
         wiringpi.digitalWrite(2, 0) # sets port 18 to 0 (0V, off)
     else:
         print("s1 can be either 'open' or 'closed', but it has been set to:", s1)
         exit(0)

     # Solenoid that vents the "reservoir" section of tubing in the box
     if (s2 == "open" or s2 == "OPEN"):
         # Assume normally open relay
         wiringpi.digitalWrite(3, 0) # sets port 2 to 0 (0V, off)
     elif(s2 == "closed" or s2 == "CLOSED"):
         wiringpi.digitalWrite(3, 1) # sets port 2 to 1 (3V3, on)
     else:
         print("s2 can be either 'open' or 'closed', but it has been set to:", s2)
         exit(0)

     # Solenoid that connects the reservoir/box to the patient's thigh cuff
     if (s3 == "open" or s3 == "OPEN"):
         # Assume normally open relay
         wiringpi.digitalWrite(4, 0) # sets port 3 to 0 (0V, off)
     elif(s3 == "closed" or s3 == "CLOSED"):
         wiringpi.digitalWrite(4, 1) # sets port 3 to 1 (3V3, on)
     else:
         print("s3 can be either 'open' or 'closed', but it has been set to:", s3)
         exit(0)

#     wiringpi.pinMode(18, 0) # sets GPIO 18 to input as a protective measure
#wiringpi.pullUpDnControl(1, 1) # pull down the new GPIO18 input with a weak internal pull-down; 2 to pull up)
#     wiringpi.pinMode(2, 0) # sets GPIO 2 to input as a protective measure
#wiringpi.pullUpDnControl(2, 1) # pull down the new GPIO2 input with a weak internal pull-down; 2 to pull up)
#     wiringpi.pinMode(3, 0) # sets GPIO 3 to input as a protective measure
#wiringpi.pullUpDnControl(3, 1) # pull down the new GPIO3 input with a weak internal pull-down; 2 to pull up)

#     relay1 = wiringpi.digitalRead(18) # read port 18 
#     relay2 = wiringpi.digitalRead(2) # read port 2
#     relay3 = wiringpi.digitalRead(3) # read port 3
#     print ("set_relay: relays now set as s1=", relay1, "s2=", relay2, "s3=", relay3)

#def set_relay(s1, s2, s3):
#    if (s1 == "open" or s1 == "OPEN"):
#        # Assume normally open relay
#        # sets port 18 to 0 (0V, off)
#        print ("Relay S1 now open")
#    elif(s1 == "closed" or s1 == "CLOSED"):
#        # sets port 18 to 1 (3V3, on)
#        print ("Relay S1 now closed")
#    else:
#        print("s1 can be either 'open' or 'closed', but it has been set to:", s1)
#        exit(0)
#
#    if (s2 == "open" or s2 == "OPEN"):
#        # Assume normally open relay
#        # sets port 2 to 0 (0V, off)
#        print ("Relay S2 now open")
#    elif(s2 == "closed" or s2 == "CLOSED"):
#        # sets port 2 to 1 (3V3, on)
#        print ("Relay S2 now closed")
#    else:
#        print("s2 can be either 'open' or 'closed', but it has been set to:", s2)
#        exit(0)
#
#    if (s3 == "open" or s3 == "OPEN"):
#        # Assume normally open relay
#        # sets port 3 to 0 (0V, off)
#        print ("Relay S3 now open")
#    elif(s3 == "closed" or s3 == "CLOSED"):
#        # sets port 3 to 1 (3V3, on)
#        print ("Relay S3 now closed")
#    else:
#        print("s3 can be either 'open' or 'closed', but it has been set to:", s3)
#        exit(0)

