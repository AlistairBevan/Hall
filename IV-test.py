import pyvisa


rm = visa.ResourceManager()

#create instances of our instruments
voltmeter = rm.open_resource('GPIB0::#::INSTR')
functionGenerator = rm.open_resource('GPIB0::#::INSTR')
currentSource = rm.open_resource('GPIB0::#::INSTR')

#configuring the voltmeter based on the labview word file
voltmeter.write('GO')
voltmeter.write('B1')
voltmeter.write('I0')
voltmeter.write('N1')
voltmeter.write('W0')
voltmeter.write('Z0')
voltmeter.write('R0')
voltmeter.write('S0')
voltmeter.write('P2')
voltmeter.write('T5')
voltmeter.write('S0P1')

#functionGenerator
