''' BASE DE DATOS AGENDA DE TENIS '''
from datetime import datetime, date, time, timedelta
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

def TotalTurnosTenis(hi,mi,fm,hf,mf):#calcula el número de turnos por cancha
    hi=int(hi)
    mi=float(mi)
    fm=float(fm)
    hf=int(hf)
    mf=float(mf)
    mia = mi/60
    mfa = mf/60
    horaincio = hi+mia
    horacierre = hf+mfa
    frecuencia=fm/60
    horasoperacion = horacierre - horaincio
    turnostotal=int(horasoperacion/frecuencia)
    return turnostotal
def GenerahorariosTenis(hi,mi,fm,hf,mf,turnostotal): #Entrega los horaios de los turnos en una lista (decimal)
    tt=int(turnostotal)
    horasagenda=[]
    hi=int(hi)
    mi=float(mi)
    fm=float(fm)
    hf=int(hf)
    mf=float(mf)
    mia = mi/60
    mfa = mf/60
    inicioturno = hi+mia+0.00001
    for i in range(tt):
        horasagenda.append(inicioturno)
        inicioturno=inicioturno+(fm/60)+0.00001
    return horasagenda
def ConvierteTurnoenHorarios(turnos,): #convierte los turnos de decimal a sexadecimal para mostrar en una lista
    devuelve=[]
    for turnito in turnos:
        enteroturnito=int(turnito)
        decimaturnito=(turnito-enteroturnito)
        minuto=int(decimaturnito*60)
        if minuto < 10:
            minuto=str(minuto)
            minuto=('0'+minuto)
        else:
            minuto=str(minuto)
        if enteroturnito<10:
            enteroturnito=str(enteroturnito)
            enteroturnito=('0'+enteroturnito)
        else:
            enteroturnito=str(enteroturnito)
        horaturno=(enteroturnito+":"+minuto)
        devuelve.append(horaturno)
    return devuelve

def creaAgendaEsqui(clu,fec,turnos,fm):
    dbconfig = read_db_config()
    q1="INSERT INTO agenda_esqui (club,fecha,frecuencia,hora,turno,crea,jugador) VAlUES ("
    q2=")"
    query=q1+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+",'vacio'"+q2
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        tt=len(turnos)
        tur=0
        for i in range(tt):
            hor=turnos[i]
            tur=tur+1
            hoy=date.today()
            hoy=str(hoy)
            user="serrezuela@serrezuela.com"#**************** COLOCAR EL USUARIO DE FLASK *************
            crea=hoy+'&/&'+user
            data=(clu,fec,fm,hor,tur,crea)
            cursor.execute(query,data)
            conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def existeAgendaEsqui(clu,fec):
    query=" SELECT hora FROM agenda_esqui WHERE club = %s AND fecha = %s AND turno=1"
    data=(clu,fec)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        row=cursor.fetchone()
        if row is not None:
            encontrado='si'
            while row is not None:
                row=cursor.fetchone()
        else:
            encontrado='no'
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return encontrado
def recuperaAgendaEsqui(clu,fec):
    query=" SELECT * FROM agenda_esqui WHERE club = %s AND fecha = %s "
    data=(clu,fec)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        progclubtenis=cursor.fetchall()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return progclubtenis
def recuperaturnoAgendaEsqui(clu,fec,tur):
    lineaturno=[]
    query=" SELECT * FROM agenda_esqui WHERE club = %s AND fecha = %s AND turno = %s "
    data=(clu,fec,tur)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        lineaturno=cursor.fetchone()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return lineaturno
def cambiadatotalAgendaEsqui(clu,fec,tur,dato,valor):
    dbconfig = read_db_config()
    q1="UPDATE agenda_esqui SET "
    q2= " = %s WHERE club = %s AND fecha=%s AND turno=%s"
    query=q1+dato+q2
    data=(valor,clu,fec,tur)
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
def turnosjuadorAgendaEsqui(jugador,fec):
    turnosjugador=[]
    query=" SELECT * FROM agenda_esqui WHERE fecha = %s AND jugador = %s "
    data=(fec,jugador)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        row=cursor.fetchone()
        while row is not None:
            turnosjugador.append(row)
            row = cursor.fetchone()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return turnosjugador

def consultadatoAgendaGolf(clu,cam,fec,tur,dato):
    q1=" SELECT "
    q2=" FROM agenda_golf WHERE club=%s AND campo=%s AND fecha = %s AND turno=%s "
    query=q1+dato+q2
    data=(clu,cam,fec,tur)
    dbconfig = read_db_config()
    hora:''
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        row=cursor.fetchone()
        hora=row[0]
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return hora

def main():
    tur=TotalTurnosTenis(hi=7,mi=0,fm=20,hf=16,mf=30) # tur es el número de turnos totales
    turnos=GenerahorariosTenis(hi=7,mi=0,fm=20,hf=16,mf=30,turnostotal=tur)
    turnossexa=ConvierteTurnoenHorarios(turnos) #conviertelos turnos decimales en formato horas
    print(tur)
    print(turnos)
    print(turnossexa)
    creaAgendaSqui(clu='Serrezuela',fec='2020-07-19',turnos=turnossexa,fm=20)

#**************
    # turnosjugador=turnosjuadorAgendaTenis(jugador='jcmejia@live.com',fec='2020-07-18')
    # print(turnosjugador)
    # print(len(turnosjugador))
#****************
    # clu='Serrezuela'
    # fec='2020-07-16'
    # tur=1
    # profes=profesdispoTenis(clu=clu,fec=fec,tur=tur)
    # print(profes)
    # print(profes[0])
#**************
    # clu='Serrezuela'
    # can='2'
    # fec='2020-07-15'
    # lineaturno=recuperaturnoAgendaTenis(clu=clu,can=can,fec=fec,tur=1)
    # print(lineaturno)
    # print(lineaturno[12])
    # lineaturno[12]="6"
    # print(lineaturno[12])
#******************
    # clu='Serrezuela'
    # fec='2020-07-14'
    # progclubtenis=recuperaAgendaTenis(clu=clu,fec=fec)
    # print(progclubtenis)
    # todo=[]
    # for agenda in progclubtenis:
    #     agendita=[]
    #     for i in range(len(agenda)):
    #         agendita.append(agenda[i])
    #     clave=str(agenda[0])+'$/$'+str(agenda[1])+'$/$'+str(agenda[2])+'$/$'+str(agenda[6])
    #     agendita.append(clave)
    #     todo.append(agendita)
    # print(len(progclubtenis))
    # print('*****+')
    # print(todo[0])
#***************
    # clu='Serrezuela'
    # fec='2020-07-15'
    # encont=existeAgendaTenis(clu=clu,fec=fec)
    # print(encont)
#*****************



if __name__ == '__main__':
    main()
