import mysql.connector

def connect_to_db(config) -> bool:
	try:
		conn = mysql.connector.connect(**config)
		print("Connessione con database stabilita")
	except mysql.connector.Error as SQL_ERR:
		print("Errore nella connesione: ", SQL_ERR)
		return None
	return conn

def disconnect_from_db(connection) -> bool:
	connection.close()
	print("Connessione con db terminata")
	return True

def insert(connection, table, dict_of_data):
	''' Inserisce una lista di oggetti a database specificandone i campi
	'''
	try:
		connection.reconnect()
		mycursor = connection.cursor(dictionary=True)
		columns = ', '.join([ str(k)			 for k in dict_of_data.keys()])
		values  = ', '.join([ ("%("+str(v)+")s") for v in dict_of_data.keys()])
		query = ( """INSERT INTO {}
				  ({})
				  VALUES ({})""".format(table,columns,values))
		mycursor.execute(query,dict_of_data)
		connection.commit()
		mycursor.close()
		return (True,query)
	except Exception as e:
		print(e)
		print(query)
		return (False,e)

DB_CONFIG = {
  'user' : 'devdb',
  'password' : 'devdb',
  'host' : '192.168.50.185',
  'port' : 3306,
  'database' : 'ml_sintesi'
}

def row_to_dict(row,split_char=","):
	splitted_row = row.split(split_char)
	return {
		"timestamp":splitted_row[0],
		"T_Esterna":splitted_row[1].replace(" ",""),
		"T_Mand_Ca":splitted_row[2].replace(" ",""),
		"T_Rit_Cal":splitted_row[3].replace(" ",""),
		"T_AcACS_C":splitted_row[4].replace(" ",""),
		"T_Mand_So":splitted_row[5].replace(" ",""),
		"T_Rit_Sol":splitted_row[6].replace(" ",""),
		"T_AcACS_S":splitted_row[7].replace(" ",""),
		"T_IngrAFS":splitted_row[8].replace(" ",""),
		"T_Man_ACS":splitted_row[9].replace(" ",""),
		"ACS_SP_Ca":splitted_row[10].replace(" ",""),
		"CLD_EnCld":splitted_row[11].replace(" ",""),
		"AFS_VolTot":splitted_row[12].replace(" ",""),
		"A1_ACS_VolTot":splitted_row[13].replace(" ",""),
		"A2_ACS_VolTot":splitted_row[14].replace(" ",""),
		"A3_ACS_VolTot":splitted_row[15].replace(" ",""),
		"A4_ACS_VolTot":splitted_row[16].replace(" ",""),
		"A5_ACS_VolTot":splitted_row[17].replace(" ",""),
		"Cald_SttExt":1 if splitted_row[18].replace(" ","") == 'active' else 0,
		"PRicACS_SttExt": 1 if splitted_row[19].replace(" ","") else 0
	}

def main():
	db_conn = connect_to_db(DB_CONFIG)
	if db_conn is None: return 0

	with open("caldaia.log","r") as log_file:
		rows = log_file.read().split("\n")
		 # skip intestazione
		rows = rows[1:]
		rows.reverse()
		for row in rows:
			if len(row)>3:
				row_as_dict = row_to_dict(row,split_char="|")
				insert(db_conn,"cremaCaldaia",row_as_dict)
	
	disconnect_from_db(db_conn)




if __name__ == "__main__":
	main()


	
	
	
	
	
	
	
	
	
	
	
	
	