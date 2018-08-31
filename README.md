# re_interactivemotor
Reverse engineering of the LEGO(R)(TM) Interactive Motor from the BOOST set 

Sharing my findings with the motor.
Used two cheap Logic Analyzers (Bus Pirate and BitScope) to sniff the communincation.

The motor uses the UART of an internal microcontroller to send to the LEGO Hubs (for now the bOOST Move Hub and the Powered Up Smart Hub) the status of the encoder.

Protocol is 115200 bps 8N1

I'm using a FTDI Beefy 3 breakout board to communicate with the Motor from my laptop:

![Beefy 3](https://github.com/JorgePe/re_interactivemotor/blob/master/photos/IMG_20180831_114748.jpg)

Wiring is simple:
* FTDI GND (black wire) to pin 3
* FTDI 3V3 (red wire) to pin 4
* FTDI TX(white/grey wire) to pin 5
* FTDI RX (green wire) to pin 6

Confusing progress history in [my blog](https://ofalcao.pt/blog/series/sniffing-the-lego-interactive-motor)

Status:
- can read encoder status (speed and position)

To be done:
- combine FTDI adapter with a H-bridge and control the motor from laptop and Raspberry Pi
- use the FTDI adapter to emulate a motor connected to BOOST

Some unorganized details:

The motor needs some kind of warm up, I'm sending almost 1 second of zeros (tried a break command, didn't work).
I think the motor needs this to leave sleep mode. If connection to motor is lost for too much time, the motor needs this warm up again and previous position is lost.

The motor requires a Init command. When the motor is not initialized, he keeps sending a short message.

After initialization, if we keep sending a 1-byte message ('02h') the motor returns a 10-byte message containing its encoder status:

SB SPEED D0=LSB D1 D2 D3=MSB 00 00 00 CRC

* SB is the Start Byte and is always 'D8h'.
* SPEED is positive when motor is rotating clockwise. Not sure about units used.
* D0..D3 contain the position in degrees. It's the same value we can read in BOOST notifications (but not values are reported by BOOST, it misses a few)
* I already have silly function to calculate CRC but will try to simplify it before writing it here

