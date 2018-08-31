# re_interactivemotor
Reverse engineering of the LEGO(R)(TM) Interactive Motor from the BOOST set 

Sharing my findings with the motor.
Used two cheap Logic Analyzers (Bus Pirate and BitScope) to sniff the communincation.

The motor uses the UART of an internal microcontroller to send to the LEGO Hubs (for now the bOOST Move Hub and the Powered Up Smart Hub) the status of the encoder.

Protocol is 115200 bps 8N1
