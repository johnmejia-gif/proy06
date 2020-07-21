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
    inicioturno = hi+mia
    for i in range(tt):
        horasagenda.append(inicioturno)
        inicioturno=inicioturno+(fm/60)
    return horasagenda
def ConvierteTurnoenHorarios(turnos,): #convierte los turnos de decimal a sexadecimal para mostrar en una lista
    devuelve=[]
    for turnito in turnos:
        enteroturnito=int(turnito)
        decimaturnito=turnito-enteroturnito
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
def creaAgendaTenis(clu,can,fec,turnos,fm,tipo):
    dbconfig = read_db_config()
    q1="INSERT INTO agenda_tenis (club,cancha,fecha,frecuencia,tipo_cancha,hora,turno,crea) VAlUES ("
    q2=")"
    query=q1+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+q2
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
            data=(clu,can,fec,fm,tipo,hor,tur,crea)
            cursor.execute(query,data)
            conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def creaAgendaProfeTenis(clu,fec,turnos,fm,profe):
    dbconfig = read_db_config()
    q1="INSERT INTO agenda_profes_tenis (club,profesor,fecha,hora,turno,jugador) VAlUES ("
    q2=")"
    query=q1+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+",'vacio'"+q2
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        tt=len(turnos)
        tur=0
        for i in range(tt):
            hor=turnos[i]
            tur=tur+1
            data=(clu,profe,fec,hor,tur)
            cursor.execute(query,data)
            conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def existeAgendaTenis(clu,fec):
    query=" SELECT hora FROM agenda_tenis WHERE club = %s AND fecha = %s AND turno=1"
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
def recuperaAgendaTenis(clu,fec):
    query=" SELECT * FROM agenda_tenis WHERE club = %s AND fecha = %s "
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
def recuperaturnoAgendaTenis(clu,can,fec,tur):
    lineaturno=[]
    query=" SELECT * FROM agenda_tenis WHERE club = %s AND cancha = %s AND fecha = %s AND turno = %s "
    data=(clu,can,fec,tur)
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
def profesdispoTenis(clu,fec,tur):
    query=" SELECT profesor FROM agenda_profes_tenis WHERE club = %s AND fecha = %s AND turno=%s AND jugador='vacio' "
    data=(clu,fec,tur)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        lista=cursor.fetchall()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    profesdispo=[]
    for item in lista:
        profesdispo.append(item[0])
    return profesdispo
def cambiadatotalAgendaTenis(clu,can,fec,tur,dato,valor):
    dbconfig = read_db_config()
    q1="UPDATE agenda_tenis SET "
    q2= " = %s WHERE club = %s AND cancha=%s AND fecha=%s AND turno=%s"
    query=q1+dato+q2
    data=(valor,clu,can,fec,tur)
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
def cambiadatoAgendaProfTenis(clu,profe,fec,tur,jugador):
    dbconfig = read_db_config()
    q1="UPDATE agenda_profes_tenis SET jugador "
    q2= " = %s WHERE club = %s AND profesor=%s AND fecha=%s AND turno=%s"
    query=q1+q2
    data=(jugador,clu,profe,fec,tur)
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
def turnosjuadorAgendaTenis(jugador,fec):
    turnosjugador=[]
    query=" SELECT * FROM agenda_tenis WHERE fecha = %s AND jugador = %s "
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

    a=['4','2','j','3','e','1','j']
    if 'j' in a:
        print('yo soy un duro')
    
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
    # tur=TotalTurnosTenis(hi=7,mi=0,fm=90,hf=16,mf=30) # tur es el número de turnos totales
    # turnos=GenerahorariosTenis(hi=7,mi=0,fm=90,hf=16,mf=30,turnostotal=tur)
    # turnossexa=ConvierteTurnoenHorarios(turnos) #conviertelos turnos decimales en formato horas
    # creaAgendaTenis(clu='Serrezuela',can='id cancha',fec='2020-07-10',turnos=turnossexa,fm=90,tipo='pr')
    # creaAgendaTenis(clu='Serrezuela',can='id cancha',fec='2020-07-10',turnos=turnossexa,fm=90,tipo='cl')
    # creaAgendaProfeTenis(clu='Serrezuela',fec='2020-07-10',turnos=turnossexa,fm=90,profe='Profe1')

#*************   ANTERIOR *****************
#***************
    # clu='Serrezuela'
    # cam='Hoyo1Serrezuela'
    # fec='2020-07-01'
    # hora=consultadatoAgendaGolf(clu=clu,cam=cam,fec=fec,tur=3,dato='hora')
    # print(hora)
#****************
    # turnosjugador=turnosjuadorAgendaGolf(usuario='jcmejia@live.com',fec='2020-07-01')
    # print('******* los turnos del jugador son: **********')
    # print(turnosjugador)
#****************

#*******************

#'****************
    # clu='Serrezuela'
    # cam='Hoyo1Serrezuela'
    # fec='2020-07-01'
    # tur=3
    # dato='huella'
    # valor='chorrera de cosasa que se escriban de acuerdo a los cambios'
    # cambiadatotalAgendaGolf(clu=clu,cam=cam,fec=fec,tur=tur,dato=dato,valor=valor)


if __name__ == '__main__':
    main()
