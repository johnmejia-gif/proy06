import re
import flask
from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
import os
from datetime import datetime, date, time, timedelta
from flask_mail import Mail
from flask_mail import Message
from random import randint, uniform,random,randrange,choice
import random
import string
from flask import flash
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

canchasprserrezuela=[1,2,3,4,7,8]
canchasclserrezuela=[9,10,11,12,13,14,15,16,17,18]
class Campos:
    def __init__(self):
        self.lista=[]
    def iniciarCampos(self):
        archivo=open('campos','a')
        archivo.close()
    def leerCampos(self):
        archivo=open('campos', 'r')
        linea=archivo.readline()
        if linea:
            while linea:
                if linea[-1] =='\n':
                    linea = linea[:-1]
                self.lista.append(linea)
                linea=archivo.readline()
        archivo.close()
    def buscarCampos(self,campo):
        for elemento in self.lista:
            arreglo=elemento.split('$*!$')
            if campo == arreglo[0]:
                listacampos=arreglo
                return listacampos
    def devolverCampos(self):  #genera una lista de cmapos
        listacampos=[]
        for elemento in self.lista:
            arreglo=elemento.split('$*!$')
            listacampos.append(arreglo[0])
        return listacampos

'''USUARIOS'''
def existeUsuarios(co): #revisa la base de datos para saber si el usuario existe, devueve si ó n0
    query=" SELECT nombre FROM usuarios WHERE correo = %s "
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query, (co,))
        row=cursor.fetchone()
        if row is not None:
            encontrado='si'
        else:
            encontrado='no'
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return encontrado
def datotalUsuarios(co,tal): #recupera un dato (tal) de la base de usuairios del ucuairo (correo)
    dbconfig = read_db_config()
    q1="SELECT "
    q2=" FROM usuarios WHERE correo = %s"
    query=q1+tal+q2
    data=(tal,co)
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,(co,))
        try:
            row=cursor.fetchone()
            dato=row[0]
        except:
            dato='errror'
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
    return dato
def crearUsuario(co,no,ap,cn,id,cl,ac,cf,ind,fr,ty): #Escribe un usuairo nuevo en la base de datos usuarios
    dbconfig = read_db_config()
    q1="INSERT INTO usuarios (correo,nombre,apellido,contrasena,telefono,club,aval_club,codigo_fed,indice,fecha_registro,tipo) VALUES ("
    q2=")"
    query=q1+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+q2
    print(query)
    data=(co,no,ap,cn,id,cl,ac,cf,ind,fr,ty)
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        print(co)
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
        conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def cambiodatoUsauarios(co,dato,valor): #cambia el valor de un dato de la base de datos entrando por correo
    dbconfig = read_db_config()
    q1="UPDATE usuarios SET "
    q2= " = %s WHERE "
    q3=" = %s"
    query=q1+dato+q2+"correo"+q3
    data=(valor,co)
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
def todosdatosUsuarios(co): #Devuelve una lista de los datos del ususario co
    dbconfig = read_db_config()
    query="SELECT * FROM usuarios WHERE correo = %s"
    datusuario=[]
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,(co,))
        try:
            row=cursor.fetchone()
            datusuario=row
        except:
            dato='errror'
    except Error as error:
        print(error)
        dato='errror'
    finally:
        cursor.close()
        conn.close()
    return datusuario
def sinavalUsuarios(cl):#Devuelve una lista con los datos de los jugadores que tinen en aval_club = NO
    dbconfig = read_db_config()
    query="SELECT * FROM usuarios WHERE club = %s AND aval_club='NO'"
    sinaval=[]
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,(cl,))
        try:
            row=cursor.fetchone()
            while row is not None:
                sinaval.append(row)
                print(row)
                row = cursor.fetchone()
        except:
            dato='errror'
    except Error as error:
        print(error)
        dato='errror'
    finally:
        cursor.close()
        conn.close()
    return sinaval
'''AGENDA DE GOLF'''
def creaAgendaGolf(clu,cam,fec,turnos,fm,tac,numjug):
    dbconfig = read_db_config()
    q1="INSERT INTO agenda_golf (club,campo,fecha,frecuencia,tac,turnostotal,hora,turno,ju1,ju2,ju3,ju4,vacios,crea) VAlUES ("
    q2=")"
    query=q1+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+q2
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        tt=len(turnos)
        tur=0
        numjug=int(numjug)
        jugs=[]
        bloquear= 4 - numjug
        for i in range (bloquear):
            jugs.append('club@club.com')
        for i in range(bloquear,4):
            jugs.append('vacio')
        ju1=jugs[0]
        ju2=jugs[1]
        ju3=jugs[2]
        ju4=jugs[3]
        for i in range(tt):
            hor=turnos[i]
            tur=tur+1
            vac=numjug
            hoy=date.today()
            hoy=str(hoy)
            user=flask.session["username"]
            crea=hoy+'&/&'+user #en posición 9 se almacena: (fecha actua/usuario:creacion desde cero)
            data=(clu,cam,fec,fm,tac,tt,hor,tur,ju1,ju2,ju3,ju4,vac,crea)
            cursor.execute(query,data)
            conn.commit()
    except Error as error:
        dato='errror'
    finally:
        cursor.close()
        conn.close()
def existeAgendaGolf(clu,cam,fec):
    query=" SELECT hora FROM agenda_golf WHERE club = %s AND campo = %s AND fecha = %s AND turno=1"
    data=(clu,cam,fec)
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
def recuperaAgendaGolf(clu,cam,fec):
    query=" SELECT * FROM agenda_golf WHERE club = %s AND campo = %s AND fecha = %s "
    data=(clu,cam,fec)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,data)
        progclubcampo=cursor.fetchall()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return progclubcampo
def recuperaturnoAgendaGolf(clu,cam,fec,tur):
    lineaturno=[]
    query=" SELECT * FROM agenda_golf WHERE club = %s AND campo = %s AND fecha = %s AND turno = %s "
    data=(clu,cam,fec,tur)
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
def cambiadatotalAgendaGolf(clu,cam,fec,tur,dato,valor):
    dbconfig = read_db_config()
    q1="UPDATE agenda_golf SET "
    q2= " = %s WHERE club = %s AND campo=%s AND fecha=%s AND turno=%s"
    query=q1+dato+q2
    data=(valor,clu,cam,fec,tur)
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
def turnosjuadorAgendaGolf(usuario,fec):
    turnosjugador=[]
    query=" SELECT * FROM agenda_golf WHERE fecha = %s "
    data=(fec)
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query,(data,))
        row=cursor.fetchone()
        while row is not None:
            for i in range(8,12):
                if row[i]==usuario:
                    turnosjugador.append(row)
            row = cursor.fetchone()
    except Error as error:
        print(error)
    finally:
        cursor.close()
        conn.close()
    return turnosjugador
'''AGENDA DE TENIS'''
def creaAgendaTenis(clu,can,fec,turnos,fm,tipo):
    dbconfig = read_db_config()
    q1="INSERT INTO agenda_tenis (club,cancha,fecha,frecuencia,tipo_cancha,hora,turno,crea,jugador,profesor) VAlUES ("
    q2=")"
    query=q1+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+",'vacio','vacio'"+q2
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
            user=flask.session["username"]
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
def profesdispoTenis(clu,fec,tur):#Devuelve lista con los profesores de tenis disponibles
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
''' AGENDA ESQUI'''
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
            user=flask.session["username"]
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

'''TARJETAS DE GOLF'''
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
'''FUNCIONES TURNOS'''
def TotalTurnos(hi,mi,fm,hf,mf,txr,desa):#devuelve una lista con [numero de turnos antes del cruce, turnos en total del día]
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
    tiempox18 = (desa+(2*txr))
    turnosantescruce=int((desa+txr)/frecuencia) #grupoturnos
    horasoperacion = horacierre - horaincio
    rondasdisponibles = horasoperacion/tiempox18
    realrondas=int(rondasdisponibles)
    saldo = float(rondasdisponibles-realrondas)
    saldoturnos = saldo * turnosantescruce * 2
    saldoturnos = int(saldoturnos)
    if saldoturnos < turnosantescruce:
        turnosad=saldoturnos+1
    else:
        turnosad=turnosantescruce
    turnostotal=((realrondas-1)*turnosantescruce)+turnosad
    turnos=[turnosantescruce ,turnostotal]
    return turnos
def generahorarios(hi,mi,fm,hf,mf,turnos): #Entrega los horaios de los turnos en una lista (decimal)
    tac=int(turnos[0])
    tt=int(turnos[1])
    horasagenda=[]
    hi=int(hi)
    mi=float(mi)
    fm=float(fm)
    hf=int(hf)
    mf=float(mf)
    mia = mi/60
    mfa = mf/60
    inicioturno = hi+mia+0.00001
    rondas=int(tt/tac)
    for i in range((rondas)):
        j=1
        while j<(tac+1):
            horasagenda.append(inicioturno)
            inicioturno=inicioturno+(fm/60)+0.00001
            j=j+1
        inicioturno=inicioturno+(tac*fm/60)
    restoturnos=tt-(rondas*tac)
    for i in range((restoturnos)):
        horasagenda.append(inicioturno)
        inicioturno=inicioturno+(fm/60)+0.00001
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
def InsertaCruces(turnossexa,tur): #inserta los cruces para mostrar los horarios
    mostrarturnos=[]
    if tur[0] != 0:
        partes=tur[1]/tur[0]
        partesenteras=int(partes)
        saldo=(partes-partesenteras)*tur[0]
        saldo=int(saldo)
        j=0
        for i in range(partesenteras):
            for k in range((tur[0])):
                mostrarturnos.append(turnossexa[j])
                j=j+1
            cruce='C_R_U_C_E_S'
            mostrarturnos.append(cruce)
        if saldo>0:
            for m in range(saldo):
                mostrarturnos.append(turnossexa[j])
                j=j+1
            mostrarturnos.append(cruce)
        return mostrarturnos
    else:
        mensaje='NO HAY AGENDA DISPONIBLE'
        mostrarturnos.append(mensaje)
        return mostrarturnos
def GeneraClave():
    clavej='asdfghjklqwertyuiopzxcvbnm1203456789AZQWSXCDERFVBGTYHNMJUIKLOP'
    c1=random.choice(clavej)
    c2=random.choice(clavej)
    c3=random.choice(clavej)
    c4=random.choice(clavej)
    c5=random.choice(clavej)
    c6=random.choice(clavej)
    c7=random.choice(clavej)
    c8=random.choice(clavej)
    contrasegna=c1+c2+c3+c4+c5+c6+c7+c8
    return contrasegna#Genera clave aleatoria de 8 dígitoS
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

app = Flask(__name__) #esto crea un objeto que lo llamamos app
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME']= 'tee.shot.principal@gmail.com'
app.config['MAIL_PASSWORD'] = 'Tshot2009'
mail=Mail(app)


@app.route('/', methods=["GET", "POST"]) #es como decirle: esta  es la página principal, es la turata p4ra la apgina principal
def home():
    flask.session["logged_in"] = False
    flask.session["name"]=''
    flask.session["username"]=''
    flask.session["course"]=''
    flask.session["tusu"]=''
    return render_template('autenticacion.html')

@app.route('/logout', methods=["GET","POST"])
def logout():
    flask.session["logged_in"] = False
    flask.session["name"]=''
    flask.session["username"]=''
    flask.session["course"]=''
    flask.session["tusu"]=''
    return flask.redirect(flask.url_for("home"))

@app.route('/autentication', methods=["POST","GET"])   #Valida los datos que viene del formulario de autenticacion en 'inicio'
def autenticar():
    if (flask.request.method == "POST"):
        flask.session["logged_in"]=False
        usuario = flask.request.form["usuario"]
        contrasena = flask.request.form["contrasena"]
        encontrado=existeUsuarios(co=usuario) #devuelve si ó no , encontró el usuario?
        if encontrado=='si':
            contrasenabase=datotalUsuarios(co=usuario,tal='contrasena')
            if contrasena==contrasenabase:
                flask.session["logged_in"]=True
                flask.session["name"]=datotalUsuarios(co=usuario,tal='nombre')
                flask.session["surname"]=datotalUsuarios(co=usuario,tal='apellido')
                flask.session["username"]=usuario
                flask.session["course"]=datotalUsuarios(co=usuario,tal='club')
                tusuario=datotalUsuarios(co=usuario,tal='tipo') #lee el tipo de usuario
                flask.session["tusu"]=tusuario
                if tusuario==1:
                    return flask.render_template("res_pos_jug_autentic.html") #direcciona a formulario positivo de autenticacion de jugador
                elif tusuario==2:
                    return flask.render_template("res_pos_adclu_autentic.html") # direcciona a formulario positivo de autenticacion administrador de club
                elif tusuario==0:
                    return flask.render_template("res_pos_admin.html")
                    tusu = tusu #************construir el menu de administrador
            else:
                return flask.render_template("res_neg_autentic.html",dato='Contraseña incorrecta') #direcciona a error de autenticación
        else:
            return flask.render_template("res_neg_autentic.html", dato='No está registrado en Tee-Shot')
    else:
        return flask.redirect(flask.url_for("home"))

@app.route('/administrator_club', methods=["GET","POST"])
def inicioadclub(): #procedimiento para direccionar al menu inicial del administrador del club
    return render_template("res_pos_adclu_autentic.html")

@app.route('/players', methods=["GET","POST"])
def iniciojugadores():#procedimiento para direccionar al menu inicial del jugador
    return render_template("res_pos_jug_autentic.html")

@app.route('/generate_new_password', methods=["GET", "POST"]) #se usara para la seccion de olvido su contraseña
def olvidocontrasegna():
    return render_template('olvido_contra.html')

@app.route('/generate_new_password/assing', methods=["GET", "POST"])
def procolvidocontrasegna():
    usuario=flask.request.form["usuario"]
    encontrado=existeUsuarios(co=usuario)
    mensajerapido=''
    if encontrado=='si':
        contra1=GeneraClave()
        cambiodatoUsauarios(co=usuario,dato='contrasena',valor=contra1)
    else:
        mensajerapido='Usuario no registrado en TEE-SHOT'
    if mensajerapido=='':
        flash('Hemos enviado una nueva contraseña a su correo electrónico.')
        msg = Message('Reestablecimiento de contraseña en TEE-SHOT', sender = app.config['MAIL_USERNAME'], recipients=[usuario])
        msg.html = render_template('mail03.html',contrasegna=contra1)
        mail.send(msg)
        return render_template('olvido_contra.html')
    else:
        flash(mensajerapido)
        return render_template('olvido_contra.html')

@app.route('/registration_TEE_SHOT', methods=["GET","POST"]) # Crear usuario como jugador
def registro():
    campos=Campos()
    campos.leerCampos()
    lista_campos=campos.devolverCampos()
    largo=len(lista_campos)
    return render_template('registro.html',campos=lista_campos, largo=largo) # Direcciona al formulario de registro de usuario jugador

@app.route('/condiciones_uso',methods=["GET","POST"])
def condiciones_uso():
    return render_template('condiciones_uso.html')

@app.route('/registration_TEE_SHOT/result_registration', methods=["POST"])
def terminaregistro():
    registro=False
    if(flask.request.method == "POST"):
        usuario = flask.request.form["usuario"]
        nombre = flask.request.form["nombre"]
        apellido = flask.request.form["apellido"]
#        contrasena1 = flask.request.form["contrasena1"]
#        contrasena2 = flask.request.form["contrasena2"]
        identificacion = flask.request.form["identificacion"]
        club = flask.request.form["club"]
        indice_fedegolf = flask.request.form["indice_fedegolf"]
        cod_fedegolf = flask.request.form["cod_fedegolf"]
        aval_club='NO'     #validar los avales mas adelante
        tipo_usuario=1
        fecha=date.today()
        fecha=str(fecha)
        contrasegna=GeneraClave()
        encontrado=existeUsuarios(co=usuario)
        print(encontrado)
        if encontrado=='si':
            return render_template('error_registro.html', error='****ERROR****    Usuario Ya Registrado en TEE-SHOT')
        else:
            crearUsuario(co=usuario,no=nombre,ap=apellido,cn=contrasegna,id=identificacion,cl=club,ac=aval_club,cf=cod_fedegolf,ind=indice_fedegolf,fr=fecha,ty=tipo_usuario)
            msg = Message('Gracias por inscribirse en TEE-SHOT', sender = app.config['MAIL_USERNAME'], recipients=[usuario])
            msg.html = render_template('mail01.html', nombre=nombre,usuario=usuario, contrasegna=contrasegna)
            mail.send(msg)
            return render_template('result_registro.html', mensaje='Felicitaciones. Su registro en TEE-SHOT ha sido exitoso')
    else:
        return render_template("autenticacion.html")

@app.route('/autentication/user_profile', methods=["GET","POST"])
def perfilusuario():
    usuario=flask.session["username"]
    datusuario=todosdatosUsuarios(co=usuario)
    return render_template('cambioperfil.html',datusuario=datusuario)

@app.route('/autentication/change_password', methods=["GET","POST"])
def cambiocontrasegna():
    return render_template('cambiopasword.html')

@app.route('/autentication/change_password/realize', methods=["GET","POST"])
def realizacambiocontrasegna():
    contra0=flask.request.form["contra0"]
    contra1=flask.request.form["contra1"]
    contra2=flask.request.form["contra2"]
    usuario=flask.session["username"]
    print(contra0)
    print(contra1)
    print(contra2)
    mensajeerror=''
    if contra1 == contra2:
        contrasegna=datotalUsuarios(co=usuario,tal='contrasena')
        if contra0 == contrasegna:
            cambiodatoUsauarios(co=usuario,dato='contrasena',valor=contra1)
        else:
            mensajeerror='Su contraseña actual está errada'
    else:
        mensajeerror='Las contraseñas son diferentes'
    if mensajeerror =='':
        flash('Contraseña cambiada de manera Exitosa')
        msg = Message('Cambio de contraseña en TEE-SHOT', sender = app.config['MAIL_USERNAME'], recipients=[usuario])
        msg.html = render_template('mail02.html')
        mail.send(msg)
        return render_template('cambiopasword.html')
    else:
        flash(mensajeerror)
        return render_template('cambiopasword.html')

@app.route('/players/cards', methods=["GET","POST"])
def tarjetasjugador():#juador define quien va a ser su marcador en la tajeta
    fecha=date.today()
    usuario=flask.session["username"]
    turnosjugador=turnosjuadorAgendaGolf(usuario=usuario,fec=fecha)
    lturnosjugador=len(turnosjugador)
    if lturnosjugador !=0:
        clubjugado=[]
        colegas=['club@club.com']
        horas=[]
        for turno in turnosjugador:
            clubjugado.append(turno[0])
            hora=turno[6]
            horas.append(hora)
            for i in range (8,12):
                if turno[i]!=usuario:
                    colegas.append(turno[i])
        return render_template('menuju05.html',clubjugado=clubjugado,colegas=colegas,turnosjugador=turnosjugador,fecha=fecha,horas=horas)
    else:
        mensajerapido='*** Usted no tiene agendado juego para hoy, debe estar agendado para entregar tarjeta de juego ***'
        flash(mensajerapido)
        return render_template('res_pos_jug_autentic.html')

@app.route('/players/cards/send', methods=["GET","POST"])
def tarjetasjugadorsend():#Jugador llene los escores de la tajeta y la envíe para que la firme el marcador
    if(flask.request.method=="POST"):
        club=flask.request.form["club"]
        marcador=flask.request.form["marcador"]
        hora=flask.request.form["hora"]
        co=flask.session["username"]
        hoy=date.today()
        encontrado=existeTarjetasGolf(fec=hoy,hora=hora,co=co)
        if encontrado=='no':
            return render_template('menuju06.html',club=club,marcador=marcador,hoy=hoy,hora=hora)
        else:
            flash('Ya tiene una tarjeta registrada')
            return render_template('res_pos_jug_autentic.html')
    else:
        return render_template("autenticacion.html")

@app.route('/players/cards/send/record', methods=["GET","POST"])
def rectarjetajugador():#graba en la base de datos la tarjeta envida por el jugador
    if(flask.request.method=="POST"):
        fec=date.today()
        co=flask.session["username"]
        mc=flask.request.form["marcador"]
        cam=flask.request.form["club"]
        hora=flask.request.form["hora"]
        encontrado=existeTarjetasGolf(fec=fec,hora=hora,co=co)
        if encontrado=='no':
            tarjeta=[]
            tarjeta.append(fec)
            tarjeta.append(hora)
            tarjeta.append(co)
            tarjeta.append(mc)
            tarjeta.append(cam)
            ida=0
            for i in range(1,10):
                adicion=str(i)
                hoyo='hoyo'+adicion
                golpes=flask.request.form[hoyo]
                tarjeta.append(golpes)
                golpes=int(golpes)
                ida=ida+golpes
            tarjeta.append(ida)
            vuelta=0
            for i in range(10,19):
                adicion=str(i)
                hoyo='hoyo'+adicion
                golpes=flask.request.form[hoyo]
                tarjeta.append(golpes)
                golpes=int(golpes)
                vuelta=vuelta+golpes
            tarjeta.append(vuelta)
            total=ida+vuelta
            tarjeta.append(total)
            tarjeta.append(co)
            creaTarjetasGolf(tarjeta=tarjeta)
            ida=str(ida)
            vuelta=str(vuelta)
            total=str(total)
            flash('Tarjeta enviada para firma del marcador. Ida= '+ida+ ' Vuelta= '+vuelta+ ' Total= ' +total)
            return render_template("res_pos_jug_autentic.html")
        else:
            flash('Ya se envió la tajeta')
            return render_template("res_pos_jug_autentic.html")

    else:
        return render_template("autenticacion.html")

@app.route('/players/cards/send/record/validate', methods=["GET","POST"])
def tarjetascolega():
    mc=flask.session["username"]
    respuesta=marcadorTarjetasGolf(mc=mc)
    asignadomarcador=respuesta[0]
    if asignadomarcador=='si':
        tars0=respuesta[1]
        tars=[]
        for tarjeta in tars0:
            if tarjeta[27]==None:
                tars.append(tarjeta)
                mensaje=''
        if tars==[]:
            mensaje='No tiene tarjetas pendientes por firmar como marcador'
    else:
        mensaje='No tiene tarjetas pendientes por firmar como marcador'
    if mensaje=='':
        return render_template('menuju07.html',respuesta=respuesta,tars=tars)
    else:
        flash(mensaje)
        return render_template('res_pos_jug_autentic.html')

@app.route('/players/cards/send/record/validate/show', methods=["GET","POST"])
def tarjetafirmada():
    mc=flask.session["username"]
    fec=flask.request.form["fec"]
    co=flask.request.form["co"]
    hora=flask.request.form["hora"]
    print(fec)
    print(hora)
    print(co)
    print(mc)
    cambiadatotalTarjetaGolf(fec=fec,hora=hora,co=co,dato='firma_marcador',valor=mc)

    flash('La tarjeta avalada por usted, ha sido enviada con exito')
    return render_template('res_pos_jug_autentic.html')

@app.route('/creating_agenda', methods=["GET","POST"])
def formturnos():
        usuario=flask.session["username"]
        club=flask.session["course"]
        course=Campos()
        course.leerCampos()
        campos=course.buscarCampos(campo=club)
        campo1=campos[1]
        largo=len(campos)
        hoy=date.today()
        fecha1=hoy+timedelta(days=1)
        fecha2=hoy+timedelta(days=10)
        return render_template("menuac02.html",club=club, campos=campos, largo=largo, fecha1=fecha1, fecha2=fecha2)

@app.route('/creating_agneda/view01', methods=["GET","POST"])
def clubcreaagendadia():#CREAR DIA Agenda para un campo específico
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fechainicial"]
        numjug=flask.request.form["numjug"]
        hora_apertura=flask.request.form["hora_apertura"]
        hora_cierre=flask.request.form["hora_cierre"]
        frecuencia=flask.request.form["frecuencia"]
        txrhu=flask.request.form["txrh"] #Horas por ronda
        txrmu=flask.request.form["txrm"] #minutos por ronda
        desau=flask.request.form["desa"] #minutos para desayuno
        numjug=int(numjug)
        txrhu=int(txrhu)
        txrmu=int(txrmu)
        txr= txrhu + (txrmu/60)
        desau=int(desau)
        desa= desau/60
        hora1=[]
        hora1=hora_apertura.split(':')
        hi=float(hora1[0])
        mi=float(hora1[1])
        hi=int(hi)
        mi=int(mi)
        hora2=[]
        hora2=hora_cierre.split(':')
        hf=float(hora2[0])
        mf=float(hora2[1])
        hf=int(hf)
        mf=int(mf)
        usuario=flask.session["username"]
        club=flask.session["course"]
        course=Campos()
        course.leerCampos()
        campos=course.buscarCampos(campo=club) #Genera lista de campos del club, almacena en vaiable campos
        clu=club
        lcampos=len(campos)
        cam=campos[1]
        fec=fecha
        fm=frecuencia
        tur=TotalTurnos(hi=hi,mi=mi,fm=fm,hf=hf,mf=mf,txr=txr,desa=desa) # tur=[turnos entre cruces, turnos totales]
        turnos=generahorarios(hi=hi,mi=mi,fm=fm,hf=hf,mf=mf,turnos=tur)  #genera los tunos en hora decimales
        turnossexa=ConvierteTurnoenHorarios(turnos) #conviertelos turnos decimales en formato horas
        mostrarturnos=InsertaCruces(turnossexa=turnossexa,tur=tur)
        lmt=len(mostrarturnos)
        tac=tur[0]
        tt=tur[1]
        checkagenda=existeAgendaGolf(clu=clu,cam=cam,fec=fec) #comprueba si existe agenda para ese club,campo y fecha
        if checkagenda == 'no':
            for i in range(1,len(campos)):
                cam=campos[i]
                creaAgendaGolf(clu=clu,cam=cam,fec=fec,turnos=turnossexa,fm=fm,tac=tac,numjug=numjug)
            return render_template("menu03ac.html", f1=fec, h1=hora_apertura, h2=hora_cierre,fr=frecuencia,tur=tur,turnos=mostrarturnos,campos=campos,club=club,lcampos=lcampos,lmt=lmt,numjug=numjug)
        else:
            return render_template("menu03ac_error.html", f1=fec,club=club,mensajeerror='YA HAY AGENDA PROGRAMADA PARA LA FECHA SELECCIONADA')
    else:
        return render_template("autenticacion.html")

@app.route('/view_agenda_parameters', methods=["GET","POST"])
def vaparameters(): #Direcciona al administrador del club para que pueda ver agenda de alguno de sus campos
    usuario=flask.session["username"]
    club=flask.session["course"]
    course=Campos()
    course.leerCampos()
    campos=course.buscarCampos(campo=club)
    campo1=campos[1]
    largo=len(campos)
    del course
    return render_template("menuac04.html",club=club,campos=campos,largo=largo)

@app.route('/view_agenda_parameters/visulization', methods=["GET","POST"])
def clubveragenda(): #El club puede ver la agenda en un día específico
    if(flask.request.method=="POST"):
        club=flask.session["course"]
        campo=flask.request.form["campo"]
        fecha=flask.request.form["fecha"]
        existeagenda=existeAgendaGolf(clu=club,cam=campo,fec=fecha)
        if existeagenda=='si':
            progclubcampo=recuperaAgendaGolf(clu=club,cam=campo,fec=fecha)

            return render_template("menuac05.html", club=club,campo=campo,fecha=fecha,progclubcampo=progclubcampo)
        else:
            mensajeerror='No existe agenda para el día seleccionado'
            return render_template("menuac_error05.html", mensajeerror=mensajeerror)
    else:
        return render_template("autenticacion.html")

@app.route('/view_agenda_parameters/visualization/changes', methods=["GET","POST"])
def clubcambioagenda():#procedimiento para que el club escriba los cambios de algún turno de la agenda
    if(flask.request.method=="POST"):
        club=flask.session["course"]
        campo=flask.request.form["campo"]
        fecha=flask.request.form["fecha"]
        turno=flask.request.form["turno"]
        filaagenda=recuperaturnoAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno)
        return render_template("menuac06.html",filaagenda=filaagenda,campo=campo,fecha=fecha,turno=turno)

    else:
        return render_template("autenticacion.html")

@app.route('/view_agenda_parameters/visualization/changes/record', methods=["GET","POST"])
def clubrealizacambioagenda(): #procedimiento para grabar los cambios definidos pór el club para algún truno de la agenda
    if(flask.request.method=="POST"):
        club=flask.session["course"]
        co=flask.session["username"]
        campo=flask.request.form["campo"]
        fecha=flask.request.form["fecha"]
        turno=flask.request.form["turno"]
        jug01=flask.request.form["jug01"]
        jug02=flask.request.form["jug02"]
        jug03=flask.request.form["jug03"]
        jug04=flask.request.form["jug04"]
        jugadores=[jug01,jug02,jug03,jug04]
        mensajeerror=''
        for jugador in jugadores:
            if jugador != '':
                if jugador !='vacio':
                    existejug=existeUsuarios(co=jugador)
                    if existejug=='no':
                        mensajeerror='Solo puede inscribir usuarios registrados en TEE-SHOT, '+jugador+' no está registrado en TEE-SHOT. *** Invítalo a inscribirse ***'
        if mensajeerror == '':
            filaagenda=recuperaturnoAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno)
            p1=filaagenda #lista de agendamiento que se va a modificar
            pjug=8
            vacios=0
            for i in range(4): #actualza jugadores respecto a la solicitud del club y lo que había en la agenda.
                if jugadores[i]=='':
                    jugadores[i]=p1[pjug]
                if jugadores[i]=='vacio':
                    vacios=vacios+1 #actualiza cuántos cupos quedan
                pjug=pjug+1
            if vacios > 0:
                nuevojugadores=[]
                for jugador in jugadores:
                    if jugador !='vacio':
                        nuevojugadores.append(jugador)
                for i in range(vacios):
                    nuevojugadores.append('vacio')
                for i in range(4):
                    jugadores[i]=nuevojugadores[i]
            hoy=date.today()
            hoy=str(hoy)
            huella=str(p1[14])
            if len(huella)<100:
                huella=huella+hoy+'&/&'+co+'$/$'
            else:
                huella=hoy+'&/&'+co+'$/$'
            cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno,dato='ju1',valor=jugadores[0])
            cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno,dato='ju2',valor=jugadores[1])
            cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno,dato='ju3',valor=jugadores[2])
            cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno,dato='ju4',valor=jugadores[3])
            cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno,dato='vacios',valor=vacios)
            cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=turno,dato='huella',valor=huella)
            return render_template("menuac07.html",jugadores=jugadores,club=club,campo=campo,fecha=fecha,turno=turno)
        else:
            return render_template("menuac07_error.html",mensajeerror=mensajeerror)


    else:
        return render_template("autenticacion.html")

@app.route('/recognition_playerbyclub',methods=["GET","POST"])
def avalarjugadoresclub(): #inicia el aval del club para los jugadores del mismo club
    club=flask.session["course"]
    sinaval=sinavalUsuarios(cl=club)
    return render_template('menuac10.html',sinaval=sinaval)

@app.route('/recognition_playerbyclub/tramit',methods=["GET","POST"])
def daravalxclub():
    co=flask.request.form["co"]
    valor='SI'
    cambiodatoUsauarios(co=co,dato="aval_club",valor=valor)
    flash('Autorizado '+co+ 'para agendar')
    return render_template('res_pos_adclu_autentic.html')

@app.route('/players/begin', methods=["GET","POST"])
def inicioagendajugador():
    ya=datetime.now()
    hora=ya.hour
    minuto=ya.minute
    if flask.session['course']=='Serrezuela':
#*****************************************************************************************************
        if hora<24 and hora>=1: #hora en el servidor donde está alojada la aplicación  HORASERVIDOR de 12 a 20
#*****************************************************************************************************
            co=flask.session["username"]
            aval=datotalUsuarios(co=co,tal="aval_club")
            club=flask.session["course"]
            if aval == 'SI':
                return render_template("menu01ju.html", club=club)
            else:
                flash('No tiene aval de del club '+club+' para pedir turnos')
                return render_template('res_pos_jug_autentic.html')
        else:
            flash('SERREZUELA definió que el horario para ingresar a seleccionar turno es de 7 am a 3 pm')
            return render_template('res_pos_jug_autentic.html')
    else:
        co=flask.session["username"]
        aval=datotalUsuarios(co=co,tal="aval_club")
        if aval == 'SI':
            club=flask.session["course"]
            return render_template("menu01ju.html", club=club)
        else:
            club=flask.session["course"]
            flash('No tiene aval de del club '+club+' para pedir turnos')
            return render_template('res_pos_jug_autentic.html')

@app.route('/players/begin/add_players', methods=["POST","GET"])
def rejugrupo(): #revisa la viavilidad de los jugadores para inscribirse
    if(flask.request.method == "POST"):
        jugadores=[]
        jug01=flask.session["username"]
        jugadores.append(jug01)
        jug02=flask.request.form["jug02"]
        jug03=flask.request.form["jug03"]
        jug04=flask.request.form["jug04"]
        club=flask.request.form["clu"]
        error_jugador=''
        if jug02 != '':
            existejug2=existeUsuarios(co=jug02)
            if existejug2=='si':
                jugadores.append(jug02)
            else:
                error_jugador='Solo puede inscribir usuarios registrados en TEE-SHOT, '+jug02+' No está registrado. *** invítalo a inscribirse ***'
        if jug03 != "":
            existejug3=existeUsuarios(co=jug03)
            if existejug3=='si':
                jugadores.append(jug03)
            else:
                error_jugador='Solo puede inscribir usuarios registrados en TEE-SHOT, '+jug03+' No está registrado. *** invítalo a inscribirse ***'
        if jug04 != "":
            existejug4=existeUsuarios(co=jug04)
            if existejug4=='si':
                jugadores.append(jug04)
            else:
                error_jugador='Solo puede inscribir usuarios registrados en TEE-SHOT, '+jug04+' No está registrado. *** invítalo a inscribirse ***'
        if error_jugador == '':
            j2=[]
            for k in range(len(jugadores)):
                j2.append(jugadores[k])
            j2.sort()
            for i in range(len(j2)):
                if len(jugadores)!=1:
                    if j2[i]==j2[i-1]:
                        error_jugador='No se puede repetir jugador'
            if error_jugador == '':
                ljugadores=len(jugadores)
                fecha0=date.today()
                fecha1=date.today()+timedelta(days=1)
                fecha2=fecha0+timedelta(days=1)
                archivo2=Campos()
                archivo2.leerCampos()
                campos=archivo2.buscarCampos(campo=club)
                lcampos=len(campos)
                return render_template("menu02ju.html",jugadores=jugadores,ljugadores=ljugadores,fecha1=fecha1,fecha2=fecha2,campos=campos,lcampos=lcampos,club=club)
            else:
                return render_template("menu02ju_error.html", mensaje=error_jugador)

        else:
            return render_template("menu02ju_error.html", mensaje=error_jugador)
    else:
        return render_template("autenticacion.html")

@app.route('/players/begin/add_players/select_option_game', methods=["POST","GET"])
def moptjug(): # mostrar opciones para que el jugador defina un turno
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fecha_deseada"]
        campo=flask.request.form["campo"]
        jugadores=flask.request.form["jugadores"]
        ljugadores=flask.request.form["ljugadores"]
        club=flask.request.form["club"]
        listajugadores=re.findall("[a-zA-Z0-0]\S+@\S+[a-zA-Z]",jugadores)
        consulta1=existeAgendaGolf(clu=club,cam=campo,fec=fecha)
        if consulta1 == 'si':
            contador=0
            for jugador in listajugadores:
                turnosjugador=turnosjuadorAgendaGolf(usuario=jugador,fec=fecha)
                if turnosjugador!=[]:
                    mensajerapido=jugador+' ya tiene turno para la fecha seleccionada'
                    contador=contador+1
            if contador==0:
                progclubcampo=recuperaAgendaGolf(clu=club, cam=campo,fec=fecha)
                ljugadores=int(ljugadores)
                return render_template("menu03ju.html",fecha=fecha,campo=campo,jugadores=jugadores,ljugadores=ljugadores,club=club,consulta1=consulta1,progclubcampo=progclubcampo)
            else:
                flash(mensajerapido)
                return render_template("res_pos_jug_autentic.html")
        else:
            flash('No hay agenda de GOLF por parte del club para ese día')
            return render_template("res_pos_jug_autentic.html")
    else:
        return render_template("autenticacion.html")

@app.route('/players/begin/add_players/select_option_game/record_aggend', methods=["GET","POST"])
def brabagenjugador(): #grabar la opción decidida por el jugador en la agenda del club
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fecha"]
        co=flask.session["username"]
        campo=flask.request.form["campo"]
        jugadores=flask.request.form["jugadores"]
        ljugadores=flask.request.form["ljugadores"]
        club=flask.request.form["club"]
        turno_sel=flask.request.form["tur"]
        listajugadores=re.findall("[a-zA-Z0-0]\S+@\S+[a-zA-Z]",jugadores)
        contador=0
        for jugador in listajugadores:
            turnosjugador=turnosjuadorAgendaGolf(usuario=jugador,fec=fecha)
            if turnosjugador!=[]:
                mensajerapido=jugador+' ya tiene turno para la fecha seleccionada'
                contador=contador+1
        if contador==0:
            tur=int(turno_sel)
            filaagenda=recuperaturnoAgendaGolf(clu=club,cam=campo,fec=fecha,tur=tur)
            p1=filaagenda
            cupos=int(p1[12]) #cupos
            ljugadores=int(ljugadores) #cuántos voy a inscribir
            if ljugadores <= cupos: #si voy a inscribir menos que los cupos disponibles
                inicial=8+(4-(cupos))
                final=inicial+(ljugadores)
                cupos=cupos - ljugadores
                for i in range (ljugadores):
                    digito=inicial-7+i
                    digito=str(digito)
                    player='ju'+digito
                    cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=tur,dato=player,valor=listajugadores[i])
                cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=tur,dato='vacios',valor=cupos)
                hoy=date.today()
                hoy=str(hoy)
                huella=str(p1[14])
                if len(huella)<100:
                    huella=huella+hoy+'&/&'+co+'$/$'
                else:
                    huella=hoy+'&/&'+co+'$/$'
                cambiadatotalAgendaGolf(clu=club,cam=campo,fec=fecha,tur=tur,dato='huella',valor=huella)
                titulo='Confirmación de turnno TEE-SHOT__'+club+' '+fecha
#***************ACTIVAR EN PRODUCCION SOLAMENTE
                # msg = Message(titulo, sender = app.config['MAIL_USERNAME'], recipients=listajugadores)
                # msg.html = render_template('mail04.html',clu=club,cam=campo,fec=fecha,usuario=co,filaagenda=filaagenda)
                # mail.send(msg)
                return render_template("menu04ju.html",fecha=fecha,campo=campo,jugadores=jugadores,ljugadores=ljugadores,club=club,turno_sel=turno_sel,filaagenda=filaagenda)
            else:
                mensajeerror='No hay cupos disponibles en la selección, por favor vuelva escoger un horaio deseado'
                return render_template("menu04ju_error.html", mensaje=mensajeerror)
        else:
            flash(mensajerapido)
            return render_template("res_pos_jug_autentic.html")
    else:
        return render_template("autenticacion.html")

@app.route('/viewcards', methods=["GET","POS"])
def selclubtarjetas():#Procedimiento para que el club selccione la fecha que desea ver tarjetas
    return render_template('menuac08.html')

@app.route('/viewcards/showdatecards',methods=["GET","POST"])
def vertarjetasclub():
    cam=flask.session["course"]
    fecha=flask.request.form["fecha"]
    fecha=str(fecha)
    tarjetas=recuperaTarjetasGolf(fec=fecha,cam=cam)
    listatarjetas=[]
    for tarjeta in tarjetas:
        nombre=datotalUsuarios(co=tarjeta[2],tal='nombre')
        apellido=datotalUsuarios(co=tarjeta[2],tal='apellido')
        cf=datotalUsuarios(co=tarjeta[2],tal='codigo_fed')
        card=[nombre,apellido,cf]
        for i in range(5,14):
            card.append(tarjeta[i])
        for i in range(15,24):
            card.append(tarjeta[i])
        card.append(tarjeta[26])
        card.append(tarjeta[27])
        listatarjetas.append(card)

    return render_template('menuac09.html',fecha=fecha,tarjetas=listatarjetas)

@app.route('/tenis_creating_agenda', methods=["GET","POST"])
def formturnostenis():#club define los parámetros iniciales para agenda tenis
        usuario=flask.session["username"]
        club=flask.session["course"]
        hoy=date.today()
        fecha1=hoy+timedelta(days=1)
        fecha2=hoy+timedelta(days=10)
        return render_template("menuac11.html",club=club, fecha1=fecha1, fecha2=fecha2)

@app.route('/tenis_creating_agenda/name_courts', methods=["GET","POST"])
def canchasyprofestenis():#club asigna nombre a las canchas y define disponibilidad de profesores
    if(flask.request.method == "POST"):
        try:
            fecha=flask.request.form["fecha"]
            club=flask.session["course"]
            checkagenda=existeAgendaTenis(clu=club,fec=fecha)
            if checkagenda=='no':
                canchaspr=int(flask.request.form["canchaspr"])
                canchascl=int(flask.request.form["canchascl"])
                hora_apertura=flask.request.form["hora_apertura"]
                hora_cierre=flask.request.form["hora_cierre"]
                frecuencia=flask.request.form["frecuencia"]
                profesores=['prof1','prof2','prof3','prof4','prof5','prof6','prof7','prof8','prof9']
                lprofesores=len(profesores)
                ncpr=[]
                for i in range(canchaspr):
                    indice=str(i)
                    aa='cpr'+indice
                    ncpr.append(aa)
                nccl=[]
                for i in range(canchascl):
                    indice=str(i)
                    aa='ccl'+indice
                    nccl.append(aa)
                nps=[]
                for i in range(lprofesores):
                    indice=str(i)
                    aa='ps'+indice
                    nps.append(aa)

                return render_template("menuac12.html",club=club,fecha=fecha, canchaspr=canchaspr,canchascl=canchascl, hora_apertura=hora_apertura,hora_cierre=hora_cierre,frecuencia=frecuencia,profesores=profesores,ncpr=ncpr,nccl=nccl,nps=nps,lprofesores=lprofesores)
            else:
                flash('YA EXISTE AGENDA DE TENIS PARA EL DIA SELECCIONADO')
                return render_template("res_pos_adclu_autentic.html")
        except:
            return render_templete("res_pos_adclu_autentic.html")
    else:
        return render_template("res_pos_adclu_autentic.html")

@app.route('/tenis_creating_agneda/view01', methods=["GET","POST"])
def clubcreaagendadiatenis():#CREAR DIA Agenda  tenis para un campo específico y las agendas de los porfesores
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fecha"]
        canchaspr=int(flask.request.form["canchaspr"])
        canchascl=int(flask.request.form["canchascl"])
        hora_apertura=flask.request.form["hora_apertura"]
        hora_cierre=flask.request.form["hora_cierre"]
        frecuencia=flask.request.form["frecuencia"]
        club=flask.session["course"]
        profesores=['prof1','prof2','prof3','prof4','prof5','prof6','prof7','prof8','prof9']
        lprofesores=len(profesores)
        todascanchas=[]
        canchaspractica=[]
        for i in range(canchaspr):
            algo=str(i)
            ncancha='cpr'+algo
            cancha=flask.request.form[ncancha]
            canchaspractica.append(cancha)
            todascanchas.append(cancha)
        canchasclase=[]
        for i in range(canchascl):
            algo=str(i)
            ncancha='ccl'+algo
            cancha=flask.request.form[ncancha]
            canchasclase.append(cancha)
            todascanchas.append(cancha)
        disponibleprofesor=[]
        for i in range(lprofesores):
            algo=str(i)
            ncancha='ps'+algo
            cancha=flask.request.form[ncancha]
            disponibleprofesor.append(cancha)
        todascanchas.sort()
        ltodascanchas=len(todascanchas)
        repetido='no'
        for i in range(ltodascanchas-1):
            j=i+1
            if todascanchas[i] == todascanchas[j]:
                repetido='si'
        if repetido=='no':
            hora1=[]
            hora1=hora_apertura.split(':')
            hi=int(hora1[0])
            mi=int(hora1[1])
            hora2=[]
            hora2=hora_cierre.split(':')
            hf=int(hora2[0])
            mf=int(hora2[1])
            fm=int(frecuencia)
            tur=TotalTurnosTenis(hi=hi,mi=mi,fm=fm,hf=hf,mf=mf) # total de turnos por cancha
            turnos=GenerahorariosTenis(hi=hi,mi=mi,fm=fm,hf=hf,mf=mf,turnostotal=tur) # genera los turnos en hora decimales
            turnossexa=ConvierteTurnoenHorarios(turnos) #conviertelos turnos decimales en formato horas
            checkagenda=existeAgendaTenis(clu=club,fec=fecha) #comprueba si existe agenda de tenis para ese club en esa fecha
            if checkagenda == 'no':
                for i in range(len(canchaspractica)):
                    can=canchaspractica[i]
                    can=str(can)
                    creaAgendaTenis(clu=club,can=can,fec=fecha,turnos=turnossexa,fm=fm,tipo='pr')
                for i in range(len(canchasclase)):
                    can=canchasclase[i]
                    can=str(can)
                    creaAgendaTenis(clu=club,can=can,fec=fecha,turnos=turnossexa,fm=fm,tipo='cl')
                for i in range(lprofesores):
                    if disponibleprofesor[i]=='SI':
                        creaAgendaProfeTenis(clu=club,fec=fecha,turnos=turnossexa,fm=fm,profe=profesores[i])
                return render_template("menuac13.html",fecha=fecha, canchaspr=canchaspr,canchascl=canchascl, hora_apertura=hora_apertura,hora_cierre=hora_cierre,frecuencia=frecuencia,profesores=profesores,canchaspractica=canchaspractica,canchasclase=canchasclase,disponibleprofesor=disponibleprofesor,lprofesores=lprofesores)
            else:
                flash('YA HAY AGENDA PROGRAMADA PARA LA FECHA SELECCIONADA')
                return render_template('res_pos_adclu_autentic.html')
        else:
            flash('No puede repetir identificación de cancha')
            return render_template('res_pos_adclu_autentic.html')
    else:
        return render_template("autenticacion.html")

@app.route('/view_agenda_parameters_tenis', methods=["GET","POST"])
def vaparameterstenis(): #Direcciona al administrador del club para que pueda ver agenda de tenis de algun dia
    usuario=flask.session["username"]
    club=flask.session["course"]
    return render_template("menuac14.html",club=club)

@app.route('/view_agenda_parameters/visulization_tenis', methods=["GET","POST"])
def clubveragendatenis(): #El club puede ver la agenda en un día específico
    if(flask.request.method=="POST"):
        club=flask.session["course"]
        fecha=flask.request.form["fecha"]
        existeagenda=existeAgendaTenis(clu=club,fec=fecha)
        if existeagenda=='si':
            progclubtenis=recuperaAgendaTenis(clu=club,fec=fecha)
            progclubcampo=[]
            for agenda in progclubtenis:
                agendita=[]
                for i in range(len(agenda)):
                    agendita.append(agenda[i])
                clave=str(agenda[1])+'$/$'+str(agenda[6])
                agendita.append(clave)
                progclubcampo.append(agendita)
            return render_template("menuac15.html", club=club,fecha=fecha,progclubcampo=progclubcampo)
        else:
            flash('NO EXISTE AGENDA DE TENIS PARA EL DIA SELECCIONADO')
            return render_template("res_pos_adclu_autentic.html")
    else:
        return render_template("res_pos_adclu_autentic.html")

@app.route('/view_agenda_parameters/visualization/changes_tenis', methods=["GET","POST"])
def clubcambioagendatenis():#procedimiento para que el club escriba los cambios de algún turno de la agenda
    if(flask.request.method=="POST"):
        club=flask.session["course"]
        linea=flask.request.form["linea"] #me trae la cancha y el turno
        fecha=flask.request.form["fecha"]
        arreglo=linea.split('$/$')
        cancha=arreglo[0]
        turno=int(arreglo[1])
        filaagenda=recuperaturnoAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno)
        profesdispo=profesdispoTenis(clu=club,fec=fecha,tur=turno)
        tprof=len(profesdispo)
        return render_template("menuac16.html",fecha=fecha,linea=linea,cancha=cancha,turno=turno,filaagenda=filaagenda,profesdispo=profesdispo,tprof=tprof)
    else:
        return render_template("autenticacion.html")

@app.route('/view_agenda_parameters/visualization/changes/record_tenis', methods=["GET","POST"])
def clubrealizacambioagendatenis(): #procedimiento para grabar los cambios definidos pór el club para algún truno de la agenda tenis
    if(flask.request.method=="POST"):
        club=flask.session["course"]
        co=flask.session["username"]
        cancha=flask.request.form["cancha"]
        fecha=flask.request.form["fecha"]
        turno=flask.request.form["turno"]
        jugador=flask.request.form["jugador"]
        profesor=flask.request.form["profesor"]
        mensajeerror=''
        if jugador != '':
            if jugador !='vacio':
                existejug=existeUsuarios(co=jugador)
                if existejug=='no':
                    mensajeerror='Solo puede inscribir usuarios registrados en TEE-SHOT, '+jugador+' no está registrado en TEE-SHOT. *** Invítalo a inscribirse ***'
        if mensajeerror == '':
            filaagenda=recuperaturnoAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno)
            p1=filaagenda #lista de agendamiento que se va a modificar
            if jugador=='':
                jugador=p1[6]
            hoy=date.today()
            hoy=str(hoy)
            huella=str(p1[9])
            if len(huella)<100:
                huella=huella+hoy+'&/&'+co+'$/$'
            else:
                huella=hoy+'&/&'+co+'$/$'
            if profesor!=filaagenda[8]:
                cambiadatotalAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno,dato='profesor',valor=profesor)
                cambiadatoAgendaProfTenis(clu=club,profe=profesor,fec=fecha,tur=turno,jugador=jugador)
            cambiadatotalAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno,dato='jugador',valor=jugador)
            cambiadatotalAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno,dato='huella',valor=huella)
            return render_template("menuac17.html",jugador=jugador,club=club,cancha=cancha,fecha=fecha,turno=turno,profesor=profesor)
        else:
            flash(mensajeerror)
            return render_template('res_pos_adclu_autentic.html')
    else:
        return render_template("autenticacion.html")

@app.route('/players/begin_tenis', methods=["GET","POST"])
def inicioagendajugador_tenis():
    ya=datetime.now()
    hora=ya.hour
    minuto=ya.minute
    fecha0=date.today()
    fecha1=date.today()+timedelta(days=1)
    fecha2=fecha0+timedelta(days=1)
    if flask.session['course']=='Serrezuela':
#*****************************************************************************************************
        if hora<24 and hora>=1: #hora en el servidor donde está alojada la aplicación  HORASERVIDOR de 12 a 20
#*****************************************************************************************************
            co=flask.session["username"]
            aval=datotalUsuarios(co=co,tal="aval_club")
            club=flask.session["course"]
            if aval == 'SI':
                return render_template("menuju08.html", club=club,fecha1=fecha1,fecha2=fecha2)
            else:
                flash('No tiene aval de del club '+club+' para pedir turnos')
                return render_template('res_pos_jug_autentic.html')
        else:
            flash('SERREZUELA definió que el horario para ingresar a seleccionar turno es de 7 am a 3 pm')
            return render_template('res_pos_jug_autentic.html')
    else:
        co=flask.session["username"]
        aval=datotalUsuarios(co=co,tal="aval_club")
        if aval == 'SI':
            club=flask.session["course"]
            return render_template("menuju08.html", club=club)
        else:
            club=flask.session["course"]
            flash('No tiene aval de del club '+club+' para pedir turnos')
            return render_template('res_pos_jug_autentic.html')

@app.route('/players/begin/add_players/select_option_game_tenis', methods=["POST","GET"])
def moptjugtenis(): # mostrar opciones para que el jugador defina un turno de práctica o de clase
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fecha_deseada"]
        tipo=flask.request.form["tipo"]
        club=flask.session["course"]
        jugador=flask.session["username"]
        consulta1=existeAgendaTenis(clu=club,fec=fecha)
        print('*********  TIPO ********')
        print(tipo)
        if consulta1 == 'si':
            turnosjugador=turnosjuadorAgendaTenis(jugador=jugador,fec=fecha)
            lturnosjugador=len(turnosjugador)
            contador=0
            if lturnosjugador>1:
                mensajerapido=jugador+' ya tiene 2 turnos para la fecha seleccionada'
                contador=1

            if contador==0:
                progclubtenis=recuperaAgendaTenis(clu=club,fec=fecha)
                progclubcampo=[]
                for agenda in progclubtenis:
                    agendita=[]
                    for i in range(len(agenda)):
                        agendita.append(agenda[i])
                    clave=str(agenda[1])+'$/$'+str(agenda[6])
                    agendita.append(clave)
                    progclubcampo.append(agendita)
                if tipo =='PRACTICA':
                    return render_template("menuju09.html",progclubcampo=progclubcampo,tipo=tipo,fecha=fecha,club=club)
                if tipo == 'CLASE':
                    return render_template("menuju11.html",progclubcampo=progclubcampo,tipo=tipo,fecha=fecha,club=club)
            else:
                flash(mensajerapido)
                return render_template("res_pos_jug_autentic.html")
        else:
            flash('No hay agenda de TENIS por parte del club para ese día')
            return render_template("res_pos_jug_autentic.html")
    else:
        return render_template("autenticacion.html")

@app.route('/players/begin/add_players/select_option_game/record_aggend_tenispr', methods=["GET","POST"])
def grabagenjugadortenispr(): #grabar la opcion del jugador para practica de tenis
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fecha"]
        jugador=flask.session["username"]
        linea=flask.request.form["linea"]
        club=flask.request.form["club"]
        turnosjugador=turnosjuadorAgendaTenis(jugador=jugador,fec=fecha)
        lturnosjugador=len(turnosjugador)
        contador=0
        if lturnosjugador>1:
            mensajerapido=jugador+' ya tiene 2 turnos para la fecha seleccionada'
            contador=1
        if contador==0:
            arreglo=linea.split('$/$')
            cancha=arreglo[0]
            turno=int(arreglo[1])
            filaagenda=recuperaturnoAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno)
            if filaagenda[7]=='vacio':
                hoy=date.today()
                hoy=str(hoy)
                huella=str(filaagenda[9])
                if len(huella)<100:
                    huella=huella+hoy+'&/&'+jugador+'$/$'
                else:
                    huella=hoy+'&/&'+co+'$/$'
                cambiadatotalAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno,dato='jugador',valor=jugador)
                cambiadatotalAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno,dato='huella',valor=huella)
                titulo='Confirmación de turnno TEE-SHOT__'+club+' '+fecha

#***************ACTIVAR EN PRODUCCION SOLAMENTE
                # msg = Message(titulo, sender = app.config['MAIL_USERNAME'], recipients=listajugadores)
                # msg.html = render_template('mail05.html',clu=club,can=cancha,fec=fecha,usuario=jugador,filaagenda=filaagenda)
                # mail.send(msg)
                return render_template("menuju10.html",fecha=fecha,cancha=cancha,jugador=jugador,club=club,filaagenda=filaagenda)
            else:
                flash('No hay cupos disponibles en la selección, por favor vuelva escoger un horaio deseado')
                return render_template("res_pos_jug_autentic.html")
        else:
            flash(mensajerapido)
            return render_template("res_pos_jug_autentic.html")
    else:
        return render_template("autenticacion.html")

@app.route('/players/begin/add_players/select_option_game/select_trainner', methods=["GET","POST"])
def jugadorescogeprofetenis():
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fecha"]
        jugador=flask.session["username"]
        linea=flask.request.form["linea"]
        club=flask.request.form["club"]
        arreglo=linea.split('$/$')
        cancha=arreglo[0]
        turno=int(arreglo[1])
        filaagenda=recuperaturnoAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno)
        hora=filaagenda[5]
        profesdispo=profesdispoTenis(clu=club,fec=fecha,tur=turno)
        tprof=len(profesdispo)
        return render_template("menuju12.html",filaagenda=filaagenda,profesdispo=profesdispo,tprof=tprof)
    else:
        return render_template("autenticacion.html")

@app.route('/players/begin/add_players/select_option_game/record_aggend_teniscl', methods=["GET","POST"])
def grabagenjugadorteniscl(): #grabar la opcion del jugador para practica de tenis
    if(flask.request.method == "POST"):
        jugador=flask.session["username"]
        club=flask.request.form["club"]
        fecha=flask.request.form["fecha"]
        turno=flask.request.form["turno"]
        cancha=flask.request.form["cancha"]
        profesor=flask.request.form["profesor"]
        turnosjugador=turnosjuadorAgendaTenis(jugador=jugador,fec=fecha)
        lturnosjugador=len(turnosjugador)
        contador=0
        if lturnosjugador>1:
            mensajerapido=jugador+' ya tiene 2 turnos para la fecha seleccionada'
            contador=1
        if contador==0:
            filaagenda=recuperaturnoAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno)
            print('********')
            print(profesor)
            print(club)
            print(cancha)
            print(fecha)
            print(turno)
            print('********')

            print(filaagenda)
            if filaagenda[7]=='vacio':
                profesdispo=profesdispoTenis(clu=club,fec=fecha,tur=turno)
                if profesor in profesdispo:
                    hoy=date.today()
                    hoy=str(hoy)
                    huella=str(filaagenda[9])
                    if len(huella)<100:
                        huella=huella+hoy+'&/&'+jugador+'$/$'
                    else:
                        huella=hoy+'&/&'+co+'$/$'
                    cambiadatotalAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno,dato='profesor',valor=profesor)
                    cambiadatoAgendaProfTenis(clu=club,profe=profesor,fec=fecha,tur=turno,jugador=jugador)
                    cambiadatotalAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno,dato='jugador',valor=jugador)
                    cambiadatotalAgendaTenis(clu=club,can=cancha,fec=fecha,tur=turno,dato='huella',valor=huella)
                    titulo='Confirmación de turnno TEE-SHOT__'+club+' '+fecha
#***************ACTIVAR EN PRODUCCION SOLAMENTE
                    # msg = Message(titulo, sender = app.config['MAIL_USERNAME'], recipients=listajugadores)
                    # msg.html = render_template('mail05.html',clu=club,can=cancha,fec=fecha,usuario=jugador,filaagenda=filaagenda)
                    # mail.send(msg)
                    return render_template("menuju10.html",fecha=fecha,cancha=cancha,jugador=jugador,club=club,filaagenda=filaagenda)
                else:
                    flash('Alguien más reservó primero con el profesor, realice nuevamente su selección')
                    return render_template("res_pos_jug_autentic.html")

            else:
                flash('No hay cupos disponibles en la selección, por favor vuelva escoger un horaio deseado')
                return render_template("res_pos_jug_autentic.html")
        else:
            flash(mensajerapido)
            return render_template("res_pos_jug_autentic.html")
    else:
        return render_template("autenticacion.html")

@app.route('/squi_creating_agenda', methods=["GET","POST"])
def formturnosesqui():#club define los parámetros iniciales para agenda esqui
        usuario=flask.session["username"]
        club=flask.session["course"]
        hoy=date.today()
        fecha1=hoy+timedelta(days=1)
        fecha2=hoy+timedelta(days=10)
        return render_template("menuac18.html",club=club, fecha1=fecha1, fecha2=fecha2)

@app.route('/squi_creating_agneda/view01', methods=["GET","POST"])
def clubcreaagendadiaesqui():#CREAR DIA Agenda esqui
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fecha"]
        hora_apertura=flask.request.form["hora_apertura"]
        hora_cierre=flask.request.form["hora_cierre"]
        frecuencia=flask.request.form["frecuencia"]
        club=flask.session["course"]
        hora1=[]
        hora1=hora_apertura.split(':')
        hi=int(hora1[0])
        mi=int(hora1[1])
        hora2=[]
        hora2=hora_cierre.split(':')
        hf=int(hora2[0])
        mf=int(hora2[1])
        fm=int(frecuencia)
        tur=TotalTurnosTenis(hi=hi,mi=mi,fm=fm,hf=hf,mf=mf) # total de turnos por cancha
        turnos=GenerahorariosTenis(hi=hi,mi=mi,fm=fm,hf=hf,mf=mf,turnostotal=tur) # genera los turnos en hora decimales
        turnossexa=ConvierteTurnoenHorarios(turnos) #conviertelos turnos decimales en formato horas
        checkagenda=existeAgendaEsqui(clu=club,fec=fecha) #comprueba si existe agenda de Esqui esa fecha
        if checkagenda == 'no':
            creaAgendaEsqui(clu=club,fec=fecha,turnos=turnossexa,fm=fm)
            return render_template("menuac19.html",fecha=fecha,hora_apertura=hora_apertura,hora_cierre=hora_cierre,frecuencia=frecuencia)
        else:
            flash('Ya hay Agenda de ESQUI programda para la fecha selccionada')
            return render_template('res_pos_adclu_autentic.html')

    else:
        return render_template("autenticacion.html")

@app.route('/view_agenda_parameters_esqui', methods=["GET","POST"])
def vaparametersesqui(): #Direcciona al administrador del club para que pueda ver agenda de tenis de algun dia
    usuario=flask.session["username"]
    club=flask.session["course"]
    return render_template("menuac20.html",club=club)

@app.route('/view_agenda_parameters/visulization_esqui', methods=["GET","POST"])
def clubveragendaesqui(): #El club puede ver la agenda en un día específico
    if(flask.request.method=="POST"):
        club=flask.session["course"]
        fecha=flask.request.form["fecha"]
        existeagenda=existeAgendaEsqui(clu=club,fec=fecha)
        if existeagenda=='si':
            progclubesqui=recuperaAgendaEsqui(clu=club,fec=fecha)
            return render_template("menuac21.html", club=club,fecha=fecha,progclubcampo=progclubesqui)
        else:
            flash('NO EXISTE AGENDA DE TENIS PARA EL DIA SELECCIONADO')
            return render_template("res_pos_adclu_autentic.html")
    else:
        return render_template("res_pos_adclu_autentic.html")

@app.route('/view_agenda_parameters/visualization/changes_esqui', methods=["GET","POST"])
def clubcambioagendaesqui():#procedimiento para que el club escriba los cambios de algún turno de la agenda
    if(flask.request.method=="POST"):
        club=flask.session["course"]
        turno=flask.request.form["turno"] #me trae el turno selecionado
        fecha=flask.request.form["fecha"]
        filaagenda=recuperaturnoAgendaEsqui(clu=club,fec=fecha,tur=turno)
        return render_template("menuac22.html",fecha=fecha,turno=turno,filaagenda=filaagenda)
    else:
        return render_template("autenticacion.html")

@app.route('/view_agenda_parameters/visualization/changes/record_squi', methods=["GET","POST"])
def clubrealizacambioagendaesqui(): #procedimiento para grabar los cambios definidos pór el club para algún truno de la agenda esqui
    if(flask.request.method=="POST"):
        club=flask.session["course"]
        co=flask.session["username"]
        fecha=flask.request.form["fecha"]
        turno=flask.request.form["turno"]
        jugador=flask.request.form["jugador"]
        mensajeerror=''
        if jugador != '':
            if jugador !='vacio':
                existejug=existeUsuarios(co=jugador)
                if existejug=='no':
                    mensajeerror='Solo puede inscribir usuarios registrados en TEE-SHOT, '+jugador+' no está registrado en TEE-SHOT. *** Invítalo a inscribirse ***'
        if mensajeerror == '':
            filaagenda=recuperaturnoAgendaEsqui(clu=club,fec=fecha,tur=turno)
            p1=filaagenda #lista de agendamiento que se va a modificar
            if jugador=='':
                jugador=p1[5]
            hoy=date.today()
            hoy=str(hoy)
            huella=str(p1[7])
            if len(huella)<100:
                huella=huella+hoy+'&/&'+co+'$/$'
            else:
                huella=hoy+'&/&'+co+'$/$'
            cambiadatotalAgendaEsqui(clu=club,fec=fecha,tur=turno,dato='jugador',valor=jugador)
            cambiadatotalAgendaEsqui(clu=club,fec=fecha,tur=turno,dato='huella',valor=huella)
            return render_template("menuac23.html",jugador=jugador,club=club,fecha=fecha,turno=turno)
        else:
            flash(mensajeerror)
            return render_template('res_pos_adclu_autentic.html')
    else:
        return render_template("autenticacion.html")

@app.route('/players/begin_esqui', methods=["GET","POST"])
def inicioagendajugador_esqui():
    ya=datetime.now()
    hora=ya.hour
    minuto=ya.minute
    fecha0=date.today()
    fecha1=date.today()+timedelta(days=1)
    fecha2=fecha0+timedelta(days=1)
    if flask.session['course']=='Serrezuela':
#*****************************************************************************************************
        if hora<24 and hora>=1: #hora en el servidor donde está alojada la aplicación  HORASERVIDOR de 12 a 20
#*****************************************************************************************************
            co=flask.session["username"]
            aval=datotalUsuarios(co=co,tal="aval_club")
            club=flask.session["course"]
            if aval == 'SI':
                return render_template("menuju13.html", club=club,fecha1=fecha1,fecha2=fecha2)
            else:
                flash('No tiene aval de del club '+club+' para pedir turnos')
                return render_template('res_pos_jug_autentic.html')
        else:
            flash('SERREZUELA definió que el horario para ingresar a seleccionar turno es de 7 am a 3 pm')
            return render_template('res_pos_jug_autentic.html')
    else:
        co=flask.session["username"]
        aval=datotalUsuarios(co=co,tal="aval_club")
        if aval == 'SI':
            club=flask.session["course"]
            return render_template("menuju13.html", club=club)
        else:
            club=flask.session["course"]
            flash('No tiene aval de del club '+club+' para pedir turnos')
            return render_template('res_pos_jug_autentic.html')

@app.route('/players/begin/add_players/select_option_game_esqui', methods=["POST","GET"])
def moptjugesqui(): # mostrar opciones para que el jugador defina un turno de esqui que desea
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fecha_deseada"]
        club=flask.session["course"]
        jugador=flask.session["username"]
        consulta1=existeAgendaEsqui(clu=club,fec=fecha)
        if consulta1 == 'si':
            turnosjugador=turnosjuadorAgendaEsqui(jugador=jugador,fec=fecha)
            lturnosjugador=len(turnosjugador)
            contador=0
            if lturnosjugador>1:
                mensajerapido=jugador+' ya tiene 2 turnos para la fecha seleccionada'
                contador=1

            if contador==0:
                progclubesqui=recuperaAgendaEsqui(clu=club,fec=fecha)
                return render_template("menuju14.html",progclubcampo=progclubesqui,fecha=fecha,club=club)
            else:
                flash(mensajerapido)
                return render_template("res_pos_jug_autentic.html")
        else:
            flash('No hay agenda de TENIS por parte del club para ese día')
            return render_template("res_pos_jug_autentic.html")
    else:
        return render_template("autenticacion.html")

@app.route('/players/begin/add_players/select_option_game/record_aggend_esqui', methods=["GET","POST"])
def grabagenjugadoresqui(): #grabar la opcion del jugador de esqui
    if(flask.request.method == "POST"):
        fecha=flask.request.form["fecha"]
        jugador=flask.session["username"]
        club=flask.request.form["club"]
        turno=flask.request.form["turno"]
        turnosjugador=turnosjuadorAgendaEsqui(jugador=jugador,fec=fecha)
        lturnosjugador=len(turnosjugador)
        contador=0
        if lturnosjugador>1:
            mensajerapido=jugador+' ya tiene 2 turnos para la fecha seleccionada'
            contador=1
        if contador==0:
            filaagenda=recuperaturnoAgendaEsqui(clu=club,fec=fecha,tur=turno)
            if filaagenda[5]=='vacio':
                hoy=date.today()
                hoy=str(hoy)
                huella=str(filaagenda[7])
                if len(huella)<100:
                    huella=huella+hoy+'&/&'+jugador+'$/$'
                else:
                    huella=hoy+'&/&'+co+'$/$'
                cambiadatotalAgendaEsqui(clu=club,fec=fecha,tur=turno,dato='jugador',valor=jugador)
                cambiadatotalAgendaEsqui(clu=club,fec=fecha,tur=turno,dato='huella',valor=huella)
                titulo='Confirmación de turnno TEE-SHOT__'+club+' '+fecha

#***************ACTIVAR EN PRODUCCION SOLAMENTE
                # msg = Message(titulo, sender = app.config['MAIL_USERNAME'], recipients=listajugadores)
                # msg.html = render_template('mail05.html',clu=club,can=cancha,fec=fecha,usuario=jugador,filaagenda=filaagenda)
                # mail.send(msg)
                return render_template("menuju15.html",fecha=fecha,jugador=jugador,club=club,filaagenda=filaagenda)
            else:
                flash('No hay cupos disponibles en la selección, por favor vuelva escoger un horaio deseado')
                return render_template("res_pos_jug_autentic.html")
        else:
            flash(mensajerapido)
            return render_template("res_pos_jug_autentic.html")
    else:
        return render_template("autenticacion.html")


if __name__ == '__main__':  #para mantener activa la página
    app.run(debug=True, port=7000)
    mail.init_app(app)
