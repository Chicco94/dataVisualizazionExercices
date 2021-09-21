import BAC0
from dataclasses import dataclass
from datetime import datetime
from time import sleep


@dataclass
class CaldaiaData:
	CACS_AS39001_T_Esterna:float
	CACS_AS39001_T_Mand_Caldaia:float
	CACS_AS39001_T_Rit_Caldaia:float
	CACS_AS39001_T_AccACS_Caldaia:float
	CACS_AS39001_T_Mand_Solare:float
	CACS_AS39001_T_Rit_Solare:float
	CACS_AS39001_T_AccACS_Solare:float
	CACS_AS39001_T_IngrAFS:float
	CACS_AS39001_T_Mand_ACS:float
	CACS_AS39001_ACS_SP_Caldaia:float
	CACS_AS39001_Caldaia_SttExt:str
	CACS_AS39001_PRicACS_SttExt:str

	def __repr__(self):
		return "{:7.2f} | {:7.2f} | {:7.2f} | {:7.2f} | {:7.2f} | {:7.2f} | {:7.2f} | {:7.2f} | {:7.2f} | {:7.2f} | {:10s} | {:10s}".format(self.CACS_AS39001_T_Esterna,
				self.CACS_AS39001_T_Mand_Caldaia,
				self.CACS_AS39001_T_Rit_Caldaia,
				self.CACS_AS39001_T_AccACS_Caldaia,
				self.CACS_AS39001_T_Mand_Solare,
				self.CACS_AS39001_T_Rit_Solare,
				self.CACS_AS39001_T_AccACS_Solare,
				self.CACS_AS39001_T_IngrAFS,
				self.CACS_AS39001_T_Mand_ACS,
				self.CACS_AS39001_ACS_SP_Caldaia,
				self.CACS_AS39001_Caldaia_SttExt,
				self.CACS_AS39001_PRicACS_SttExt)

KIEBACK_VARIABLES = {
	"CACS_AS39001_T_Esterna":{'object_instance':2796203,'object': 'analogValue'}, 
	"CACS_AS39001_T_Mand_Caldaia":{'object_instance':2796204,'object': 'analogValue'}, 
	"CACS_AS39001_T_Rit_Caldaia":{'object_instance':2796205,'object': 'analogValue'}, 
	"CACS_AS39001_T_AccACS_Caldaia":{'object_instance':2796206,'object': 'analogValue'}, 
	"CACS_AS39001_T_Mand_Solare":{'object_instance':2796207,'object': 'analogValue'}, 
	"CACS_AS39001_T_Rit_Solare":{'object_instance':2796208,'object': 'analogValue'}, 
	"CACS_AS39001_T_AccACS_Solare":{'object_instance':2796209,'object': 'analogValue'}, 
	"CACS_AS39001_T_IngrAFS":{'object_instance':2796210,'object': 'analogValue'}, 
	"CACS_AS39001_T_Mand_ACS":{'object_instance':2796211,'object': 'analogValue'}, 
	"CACS_AS39001_ACS_SP_Caldaia":{'object_instance':2796213,'object': 'analogValue'}, 
	"CACS_AS39001_Caldaia_SttExt":{'object_instance': 2796211,'object': 'binaryValue'},
	"CACS_AS39001_PRicACS_SttExt":{'object_instance': 2796212,'object': 'binaryValue'}
}
SLEEP_TIME = 10


def read_variable(channel,variable):
	to_be_red = '192.168.0.2 {object} {object_instance} presentValue'.format(object=variable['object'],object_instance=variable['object_instance'])
	return channel.read(to_be_red)


def write_variable(channel,variable,value):
	to_be_written = '192.168.0.2 {object} {object_instance} presentValue {value}'.format(object=variable['object'],object_instance=variable['object_instance'],value=value)
	return channel.write(to_be_written)


def read_variables(channel,dict_of_variables):
	temp_dict = {}
	for key,var in dict_of_variables.items():
		temp_dict[key]=read_variable(channel,var)
	return CaldaiaData(*temp_dict.values())


def log(caldaia_data):
	with open('caldaia.log','a') as log_file:
		log_file.write("{data_e_ora} | {dati_caldaia}\n".format(data_e_ora=datetime.now(),dati_caldaia=caldaia_data))


def main():
	bacnet = BAC0.connect(ip='192.168.0.29/24')
	device_name = bacnet.read('192.168.0.2 device 39001 objectName')
	print(device_name)
	
	print(read_variable(bacnet,KIEBACK_VARIABLES['CACS_AS39001_Caldaia_SttExt']))
	write_variable(bacnet,KIEBACK_VARIABLES['CACS_AS39001_Caldaia_SttExt'],'active')
	print(read_variable(bacnet,KIEBACK_VARIABLES['CACS_AS39001_Caldaia_SttExt']))
	write_variable(bacnet,KIEBACK_VARIABLES['CACS_AS39001_Caldaia_SttExt'],'inactive')
	print(read_variable(bacnet,KIEBACK_VARIABLES['CACS_AS39001_Caldaia_SttExt']))

	while True:
		log(read_variables(bacnet,KIEBACK_VARIABLES))
		sleep(SLEEP_TIME)

if __name__ == '__main__':
	main()
