import ghasedak
SMS = ghasedak.Ghasedak('5c4fe5bf481fc9882613f70b003b6319e54a76a76a1114924f72b2440920685d')
print(SMS.send({'message': 'Appointment available at Turkey embassy', 
'receptor' : '09029279793', 
'linenumber': '5000121212'}))