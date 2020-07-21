''' BASE DE DATOS TARJETAS DE GOLF'''
from datetime import datetime, date, time, timedelta
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config


def creaTarjetasGolf(tarjeta):
    dbconfig = read_db_config()
    q1="INSERT INTO tarjetas_golf (fecha, hora, jugador, marcador, campo, h01, h02, h03, h04, h05, h06, h07, h08, h09, ida, h10, h11, h12 ,h13 ,h14 ,h15 ,h16 ,h17 ,h18 ,vuelta ,total ,firma_jugador) VALUES ("
    q2="%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    query=q1+q2
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,tarjeta)
        conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def existeTarjetasGolf(fec,hora,co):
    query=" SELECT campo FROM tarjetas_golf WHERE fecha = %s AND hora = %s AND jugador = %s "
    data=(fec,hora,co)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        row=cursor.fetchone()

        if row is not None:
            encontrado='si'
            row=cursor.fetchone()
        else:
            encontrado='no'
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return encontrado
def marcadorTarjetasGolf(mc):
    query="SELECT * FROM tarjetas_golf WHERE marcador = %s and fecha= %s"
    dbconfig = read_db_config()
    asignadomarcador='no'
    tars=[]
    fec=date.today()
    fec=str(fec)
    data=(mc,fec)
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        row=cursor.fetchone()
        while row is not None:
            asignadomarcador='si'
            tars.append(row)
            row=cursor.fetchone()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    respuesta=[asignadomarcador,tars]
    return respuesta
def cambiadatotalTarjetaGolf(fec,hora,co,dato,valor):
    dbconfig = read_db_config()
    q1="UPDATE tarjetas_golf SET "
    q2= " = %s WHERE fecha = %s AND hora=%s AND jugador=%s "
    query=q1+dato+q2
    data=(valor,fec,hora,co)
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def recuperaTarjetasGolf(fec,cam):
    tarjetas=[]
    query=" SELECT * FROM tarjetas_golf WHERE fecha= %s AND campo = %s "
    data=(fec,cam)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        tarjetas=cursor.fetchall()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return tarjetas

def main():
    tarjetas=recuperaTarjetasGolf(fec='2020-07-03',cam='Serrezuela')
    print(tarjetas)
    print('Hay un total de : ')
    print(len(tarjetas))
#*******************
    # cambiadatotalTarjetaGolf(fec='2020-07-03',hora='07:45',co='jcmejia@live.com',dato='firma_marcador',valor='prueba@pr.com')
#*********************
    # respuesta=marcadorTarjetasGolf(mc='club@club.com')
    # print(respuesta)
    # for asig in respuesta[1]:
    #     print(asig[0])
    #     print(asig[27])
    # if asig[27]==None:
    #     print('afirmativo')
    # else:
    #     print('negativo')
#*********************
    # encontrado=existeTarjetasGolf(fec='2020-07-01',hora='6:30',co='german@german.com')
    # print(encontrado)
#*************************
    # tarjeta=['2020-07-01','6:30','german@german.com','mario@hot.com','Serrezuela',3,4,5,3,4,5,2,6,5,51,3,6,8,9,6,4,6,7,9,48,99,'german@german.com']
    # creaTarjetasGolf(tarjeta)


if __name__ == '__main__':
    main()
