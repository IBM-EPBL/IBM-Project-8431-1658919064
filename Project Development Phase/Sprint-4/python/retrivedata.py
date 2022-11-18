import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;PROTOCOL=TCPIP;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mbd73622;PWD=DxrsqQuuiC8JEIN1",'','')

#To retrive all the records from DB2

sql = "SELECT * FROM PLASMADONOR"
stmt = ibm_db.exec_immediate(conn, sql)
dictionary = ibm_db.fetch_both(stmt)
values=dictionary
while dictionary != False:
    #print(dictionary)
    print ("The Name is : ",  dictionary["NAME"])
    print ("The Email is : ", dictionary["EMAIL"])
    print ("The Phone is : ", dictionary["PHONE"])
    print(" ******************* ")
    values.update(dictionary)
    dictionary = ibm_db.fetch_both(stmt)

print(values)
