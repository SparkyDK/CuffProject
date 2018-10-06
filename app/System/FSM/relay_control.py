import wiringpi as wiringpi
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(1, 1) # sets GPIO 1 to output
wiringpi.pinMode(2, 1) # sets GPIO 2 to output
wiringpi.pinMode(3, 1) # sets GPIO 3 to output

def set_relay(s1, s2, s3):
    if (s1 == "open" or s1 == "OPEN"):
        # Assume normally open relay
        wiringpi.digitalWrite(1, 0) # sets port 1 to 0 (0V, off)
    elif(s1 == "closed" or s1 == "CLOSED"):
        wiringpi.digitalWrite(1, 1) # sets port 1 to 1 (3V3, on)
    else:
        print("s1 can be either 'open' or 'closed', but it has been set to:", s1)
        exit(0)

    if (s2 == "open" or s2 == "OPEN"):
        # Assume normally open relay
        wiringpi.digitalWrite(2, 0) # sets port 2 to 0 (0V, off)
    elif(s2 == "closed" or s2 == "CLOSED"):
        wiringpi.digitalWrite(2, 1) # sets port 2 to 1 (3V3, on)
    else:
        print("s2 can be either 'open' or 'closed', but it has been set to:", s2)
        exit(0)

    if (s3 == "open" or s3 == "OPEN"):
        # Assume normally open relay
        wiringpi.digitalWrite(3, 0) # sets port 3 to 0 (0V, off)
    elif(s3 == "closed" or s3 == "CLOSED"):
        wiringpi.digitalWrite(3, 1) # sets port 3 to 1 (3V3, on)
    else:
        print("s3 can be either 'open' or 'closed', but it has been set to:", s3)
        exit(0)

#wiringpi.pinMode(1, 0) # sets GPIO 1 to input as a protective measure
#wiringpi.pullUpDnControl(1, 1) # pull down the new GPIO1 input with a weak internal pull-down; 2 to pull up)
#wiringpi.pinMode(2, 0) # sets GPIO 2 to input as a protective measure
#wiringpi.pullUpDnControl(2, 1) # pull down the new GPIO2 input with a weak internal pull-down; 2 to pull up)
#wiringpi.pinMode(3, 0) # sets GPIO 3 to input as a protective measure
#wiringpi.pullUpDnControl(3, 1) # pull down the new GPIO3 input with a weak internal pull-down; 2 to pull up)