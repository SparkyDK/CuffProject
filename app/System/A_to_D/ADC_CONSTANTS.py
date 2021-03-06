# All of the TI1256-specific register values, etc.

# Assumed connectivity
""" Wiring Diagram
 +-----+-----+---------+------+---+---Pi 2---+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
 |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5V      |     |     |
 |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |
 |   4 |   7 | GPIO. 7 |   IN | 1 |  7 || 8  | 1 | ALT0 | TxD     | 15  | 14  |
 |     |     |      0v |      |   |  9 || 10 | 1 | ALT0 | RxD     | 16  | 15  |
 |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 1 | IN   | GPIO. 1 | 1   | 18  |
 |  27 |   2 | GPIO. 2 |   IN | 1 | 13 || 14 |   |      | 0v      |     |     |
 |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
 |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
 |  10 |  12 |    MOSI | ALT0 | 0 | 19 || 20 |   |      | 0v      |     |     |
 |   9 |  13 |    MISO | ALT0 | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
 |  11 |  14 |    SCLK | ALT0 | 0 | 23 || 24 | 1 | OUT  | CE0     | 10  | 8   |
 |     |     |      0v |      |   | 25 || 26 | 1 | OUT  | CE1     | 11  | 7   |
 |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
 |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |
 |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
 |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
 |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
 |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
 |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+---Pi 2---+---+------+---------+-----+-----+
"""

# These options can be adjusted to facilitate specific operation of the
# ADS1256, the defaults are designed to be compatible with the Waveforms
# High Precision AD/DA board
SPI_MODE = 1
SPI_CHANNEL = 1
SPI_FREQUENCY = 1000000  # The ADS1256 supports 768kHz to 1.92MHz
DRDY_TIMEOUT = 0.5  # Seconds to wait for DRDY when communicating
DATA_TIMEOUT = 0.00001  # 10uS delay for sending data
SCLK_FREQUENCY = 7680000  # default clock rate is 7.68MHz

# The RPI GPIO to use for chip select and ready polling
CS_PIN = 15
DRDY_PIN = 11
RESET_PIN = 12
PDWN_PIN = 13

# Register addresses
REG_STATUS = 0x00
REG_MUX = 0x01
REG_ADCON = 0x02
REG_DRATE = 0x03
REG_IO = 0x04
REG_OFC0 = 0x05
REG_OFC1 = 0x06
REG_OFC2 = 0x07
REG_FSC0 = 0x08
REG_FSC1 = 0x09
REG_FSC2 = 0x0A
NUM_REG = 11

"""
DRATE Register: A/D Data Rate Address 0x03 The 16 valid Data Rate settings are shown below. Make sure to select a
valid setting as the invalid settings may produce unpredictable results.

Bits 7-0 DR[7: 0]: Data Rate Setting(1)

    11110000 = 30,000SPS (default)
    11100000 = 15,000SPS
    11010000 = 7,500SPS
    11000000 = 3,750SPS
    10110000 = 2,000SPS
    10100001 = 1,000SPS
    10010010 = 500SPS
    10000010 = 100SPS
    01110010 = 60SPS
    01100011 = 50SPS
    01010011 = 30SPS
    01000011 = 25SPS
    00110011 = 15SPS
    00100011 = 10SPS
    00010011 = 5SPS
    00000011 = 2.5SPS

    (1) for fCLKIN = 7.68MHz. Data rates scale linearly with fCLKIN
"""
# sample rates
DRATE_30000 = 0b11110000  # 30,000SPS (default)
DRATE_15000 = 0b11100000  # 15,000SPS
DRATE_7500 = 0b11010000  # 7,500SPS
DRATE_3750 = 0b11000000  # 3,750SPS
DRATE_2000 = 0b10110000  # 2,000SPS
DRATE_1000 = 0b10100001  # 1,000SPS
DRATE_500 = 0b10010010  # 500SPS
DRATE_100 = 0b10000010  # 100SPS
DRATE_60 = 0b01110010  # 60SPS
DRATE_50 = 0b01100011  # 50SPS
DRATE_30 = 0b01010011  # 30SPS
DRATE_25 = 0b01000011  # 25SPS
DRATE_15 = 0b00110011  # 15SPS
DRATE_10 = 0b00100011  # 10SPS
DRATE_5 = 0b00010011  # 5SPS
DRATE_2_5 = 0b00000011  # 2.5SPS

# Commands
CMD_WAKEUP = 0x00  # Completes SYNC and exits standby mode
CMD_RDATA = 0x01  # Read data
CMD_RDATAC = 0x03  # Start read data continuously
CMD_SDATAC = 0x0F  # Stop read data continuously
CMD_RREG = 0x10  # Read from register
CMD_WREG = 0x50  # Write to register
CMD_SELFCAL = 0xF0  # Offset and gain self-calibration
CMD_SELFOCAL = 0xF1  # Offset self-calibration
CMD_SELFGCAL = 0xF2  # Gain self-calibration
CMD_SYSOCAL = 0xF3  # System offset calibration
CMD_SYSGCAL = 0xF4  # System gain calibration
CMD_SYNC = 0xFC  # Synchronize the A/D conversion
CMD_STANDBY = 0xFD  # Begin standby mode
CMD_RESET = 0xFE  # Reset to power-on values

"""
Status Register Configuration - logically OR all desired options together
to form a 1 byte command and write it to the STATUS register

STATUS REGISTER - ADDRESS 0x00
Bits 7-4 ID3, ID2, ID1, ID0 Factory Programmed Identification Bits 
(Read Only)

Bit 3 ORDER: Data Output Bit Order

    0 = Most Significant Bit First (default)
    1 = Least Significant Bit First

    Input data is always shifted in most significant byte and bit first.
    Output data is always shifted out most significant byte first. The
    ORDER bit only controls the bit order of the output data within the
    byte.

Bit 2 ACAL: Auto-Calibration

    0 = Auto-Calibration Disabled (default)
    1 = Auto-Calibration Enabled

    When Auto-Calibration is enabled, self-calibration begins at the
    completion of the WREG command that changes the PGA (bits 0-2 of ADCON
    register), DR (bits 7-0 in the DRATE register) or BUFEN (bit 1 in the
    STATUS register) values.

Bit 1 BUFEN: Analog Input Buffer Enable

    0 = Buffer Disabled (default)
    1 = Buffer Enabled

Bit 0 DRDY: Data Ready (Read Only)

    This bit duplicates the state of the DRDY pin, which is inverted logic.
"""
STATUS_BUFFER_ENABLE = 0x02
STATUS_AUTOCAL_ENABLE = 0x04
STATUS_ORDER_LSB = 0x08

"""
A/D Control Register - Address 0x02

Bit 7 Reserved, always 0 (Read Only)

Bits 6-5 CLK1, CLK0: D0/CLKOUT Clock Out Rate Setting

    00 = Clock Out OFF
01 = Clock Out Frequency = fCLKIN (default)
10 = Clock Out Frequency = fCLKIN/2
11 = Clock Out Frequency = fCLKIN/4

When not using CLKOUT, it is recommended that it be turned off. These
bits can only be reset using the RESET pin.

Bits 4-3 SDCS1, SCDS0: Sensor Detect Current Sources

00 = Sensor Detect OFF (default)
01 = Sensor Detect Current = 0.5uA
10 = Sensor Detect Current = 2uA
11 = Sensor Detect Current = 10uA

The Sensor Detect Current Sources can be activated to verify the
integrity of an external sensor supplying a signal to the ADS1255/6.
A shorted sensor produces a very small signal while an open-circuit
sensor produces a very large signal.

Bits 2-0 PGA2, PGA1, PGA0: Programmable Gain Amplifier Setting
    000 = 1 (default)
    001 = 2
    010 = 4
    011 = 8
    100 = 16
    101 = 32
    110 = 64
    111 = 64
"""
# Gain levels
AD_GAIN_1 = 0x00
AD_GAIN_2 = 0x01
AD_GAIN_4 = 0x02
AD_GAIN_8 = 0x03
AD_GAIN_16 = 0x04
AD_GAIN_32 = 0x05
AD_GAIN_64 = 0x06

# Sensor Detect Current Sources
AD_SDCS_500pA = 0x08
AD_SDCS_2uA = 0x10
AD_SDCS_10uA = 0x18

# Clock divider
AD_CLK_EQUAL = 0x20
AD_CLK_HALF = 0x40
AD_CLK_FOURTH = 0x60
