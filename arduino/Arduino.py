import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serial_inst = serial.Serial()

ports_list = []

for port in ports:
    ports_list.append(str(port))
    print(str(port))

val: str = input('Select Port: COM')

for i in range(len(ports_list)):
    if ports_list[i].startswith(f'COM{val}'):
        port_var = ports_list[i] #f'COM{val}'
        print(port_var)

serial_inst.baudrate = 9600
serial_inst.port = port_var
serial_inst.open()

while True:
    # for now command = x_y_UPDATE
    #(UPDATE is indicating that the cordinates are sent from Python)
    command = "90:90"
    serial_inst.write(command.encode('utf-8'))

    if command == 'EXIT':
        exit(0)
        