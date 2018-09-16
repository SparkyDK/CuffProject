import time
import wiringpi2 as wp

def debug_print(string):
    if True:
        print("DEBUG: " + string)


class ADS1256:

    from app.System.A_to_D.ADC_CONSTANTS import DRDY_PIN, RESET_PIN,PDWN_PIN, CS_PIN,\
        SPI_CHANNEL, SPI_FREQUENCY, DRDY_TIMEOUT, SCLK_FREQUENCY, DATA_TIMEOUT, CMD_RREG,\
        CMD_WREG, CMD_RDATA, REG_STATUS

    # The RPI GPIO to use for chip select and ready polling
    def __init__(self):
        # Set up the wiringpi object to use physical pin numbers
        wp.wiringPiSetupPhys()

        # Initialize the DRDY pin
        wp.pinMode(self.DRDY_PIN, wp.INPUT)

        # Initialize the reset pin
        wp.pinMode(self.RESET_PIN, wp.OUTPUT)
        wp.digitalWrite(self.RESET_PIN, wp.HIGH)

        # Initialize PDWN pin
        wp.pinMode(self.PDWN_PIN, wp.OUTPUT)
        wp.digitalWrite(self.PDWN_PIN, wp.HIGH)

        # Initialize CS pin
        wp.pinMode(self.CS_PIN, wp.OUTPUT)
        wp.digitalWrite(self.CS_PIN, wp.HIGH)

        # Initialize the wiringpi SPI setup
        spi_success = wp.wiringPiSPISetup(self.SPI_CHANNEL, self.SPI_FREQUENCY)
        debug_print("SPI success " + str(spi_success))

    def chip_select(self):
        wp.digitalWrite(self.CS_PIN, wp.LOW)

    def chip_release(self):
        wp.digitalWrite(self.CS_PIN, wp.HIGH)

    def WaitDRDY(self):
        """
        Delays until DRDY line goes low, allowing for automatic calibration
        """
        start = time.time()
        elapsed = time.time() - start

        # Waits for DRDY to go to zero or TIMEOUT seconds to pass
        drdy_level = wp.digitalRead(self.DRDY_PIN)
        while (drdy_level == wp.HIGH) and (elapsed < self.DRDY_TIMEOUT):
            elapsed = time.time() - start
            drdy_level = wp.digitalRead(self.DRDY_PIN)

        if elapsed >= self.DRDY_TIMEOUT:
            print("WaitDRDY() Timeout\r\n")

    def SendByte(self, byte):
        """
        Sends a byte to the SPI bus
        """
        debug_print("Entered SendByte")
        debug_print("Sending: " + str(byte))
        data = chr(byte)
        result = wp.wiringPiSPIDataRW(self.SPI_CHANNEL, data)
        debug_print("Read " + str(data))

    def ReadByte(self):
        """
        Reads a byte from the SPI bus
        :returns: byte read from the bus
        """
        byte = wp.wiringPiSPIDataRW(self.SPI_CHANNEL, chr(0x00))
        return byte

    def DataDelay(self):
        """
        Delay from last SCLK edge to first SCLK rising edge

        Master clock rate is typically 7.68MHz, this is adjustable through the
        SCLK_FREQUENCY variable

        Datasheet states that the delay between requesting data and reading the
        bus must be minimum 50x SCLK period, this function reads data after
        60 x SCLK period.
        """
        timeout = (60 / self.SCLK_FREQUENCY)

        start = time.time()
        elapsed = time.time() - start

        # Wait for TIMEOUT to elapse
        while elapsed < self.DATA_TIMEOUT:
            elapsed = time.time() - start

    def ReadReg(self, start_reg, num_to_read):
        """
        Read the provided register, implements:

        RREG: Read from Registers

        Description: Output the data from up to 11 registers starting with the
        register address specified as part of the command. The number of
        registers read will be one plus the second byte of the command. If the
        count exceeds the remaining registers, the addresses will wrap back to
        the beginning.

        1st Command Byte: 0001 rrrr where rrrr is the address of the first
        register to read.

        2nd Command Byte: 0000 nnnn where nnnn is the number of bytes to read
        1. See the Timing Characteristics for the required delay between the
        end of the RREG command and the beginning of shifting data on DOUT: t6.
        """

        result = []

        # Pull the SPI bus low
        self.chip_select()

        # Send the byte command
        self.SendByte(self.CMD_RREG | start_reg)
        self.SendByte(0x00)

        # Wait for appropriate data delay
        self.DataDelay()

        # Read the register contents
        read = self.ReadByte()

        # Release the SPI bus
        self.chip_release()

        return read

    def WriteReg(self, start_register, data):
        self.register = start_register
        """
        Writes data to the register, implements:

        WREG: Write to Register

        Description: Write to the registers starting with the register
        specified as part of the command. The number of registers that
        will be written is one plus the value of the second byte in the
        command.

        1st Command Byte: 0101 rrrr where rrrr is the address to the first
        register to be written.

        2nd Command Byte: 0000 nnnn where nnnn is the number of bytes-1 to be
        written

        TODO: Implement multiple register write
        """

        # Select the ADS chip
        self.chip_select()

        # Tell the ADS chip which register to start writing at
        self.SendByte(self.CMD_WREG | self.register)

        # Tell the ADS chip how many additional registers to write
        self.SendByte(0x00)

        # Send the data
        self.SendByte(data)

        # Release the ADS chip
        self.chip_release()

    def ReadADC(self):
        """
        Reads ADC data, implements:

        RDATA: Read Data

        Description: Issue this command after DRDY goes low to read a single
        conversion result. After all 24 bits have been shifted out on DOUT,
        DRDY goes high. It is not necessary to read back all 24 bits, but DRDY
        will then not return high until new data is being updated. See the
        Timing Characteristics for the required delay between the end of the
        RDATA command and the beginning of shifting data on DOUT: t6
        """

        # Pull the SPI bus low
        self.chip_select()

        # Wait for data to be ready
        self.WaitDRDY()

        # Send the read command
        self.SendByte(self.CMD_RDATA)

        # Wait through the data pause
        self.DataDelay()

        # The result is 24 bits
        self.result = []
        self.result.append(self.ReadByte())
        self.result.append(self.ReadByte())
        self.result.append(self.ReadByte())

        # Release the SPI bus
        self.chip_release()

        # Concatenate the bytes
        total = (self.result[0] << 16)
        total |= (self.result[1] << 8)
        total |= self.result[2]

        return total

    def ReadID(self):
        """
        Read the ID from the ADS chip
        :returns: numeric identifier of the ADS chip
        """
        self.WaitDRDY()
        myid = self.ReadReg(self.REG_STATUS, 1)
        return (myid >> 4)
