import pyvisa


rm = visa.ResourceManager()

#create instances of our instruments
voltmeter = rm.open_resource('GPIB0::2::INSTR')
scanner = rm.open_resource('GPIB0::7::INSTR')
currentSource = rm.open_resource('GPIB0::12::INSTR')

#configuring the voltmeter based on the labview word file
voltmeter.write('GOX')
voltmeter.write('B1X')
voltmeter.write('I0X')
voltmeter.write('N1X')
voltmeter.write('W0X')
voltmeter.write('Z0X')
voltmeter.write('R0X')
voltmeter.write('S0X')
voltmeter.write('P2X')
voltmeter.write('T5X')
voltmeter.write('S0P1X')

#configuring the Scanner
scanner.write('RX')
scanner.write('A0X')
scanner.write('B071X')
scanner.write('C071X')
scanner.write('N071X')

#functionGenerator
currentSource.write('k0X')
currentSource.write('F1X')
currentSource.write('L1X')
currentSource.write('B1X')
currentSource.write('V1.00000E+1X')
currentSource.write('W1.000E+0X')

currentSource.write('I0.035E+0X')
print(voltmeter.query_ascii_values('CURV?'))
