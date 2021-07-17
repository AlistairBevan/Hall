import pyvisa


rm = pyvisa.ResourceManager()

#create instances of our instruments
voltmeter = rm.open_resource('GPIB0::2::INSTR')
scanner = rm.open_resource('GPIB0::7::INSTR')
currentSource = rm.open_resource('GPIB0::12::INSTR')

#configuring the voltmeter based on the labview word file
voltmeter.write('G0B1I0N1W0Z0R0S0P1O0T5')

#configuring the Scanner
scanner.write(':clos (@1!1!1,1!2!2,1!3!3,1!4!4)')

#functionGenerator
currentSource.write('F1XL1 B1')

currentSource.write('I0.035E+0X')
voltmeter.write('X')
print(voltmeter.read())
input('turn off?')
currentSource.write('I0.000E+0X')
#print(voltmeter.query_ascii_values('CURV?'))
