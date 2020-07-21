''' BASE DE DATOS JUGADORES '''
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

def existeUsuarios(co):
    query=" SELECT nombre FROM usuarios WHERE correo = %s "
    dbconfig = read_db_config()
    try:
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        print(co)
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
def datotalUsuarios(co,tal):
    dbconfig = read_db_config()
    q1="SELECT "
    q2=" FROM usuarios WHERE correo = %s"
    query=q1+tal+q2
    # query=" SELECT %s FROM usuarios WHERE correo = %s "
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
        print(error)
        dato='errror'
    finally:
        cursor.close()
        conn.close()
    return dato
def crearUsuario(co,no,ap,cn,id,cl,ac,cf,ind,fr,ty):
    dbconfig = read_db_config()
    q1="INSERT INTO usuarios (correo,nombre,apellido,contrasena,telefono,club,aval_club,codigo_fed,indice,fecha_registro,tipo) VALUES ("
    q2=")"
    query=q1+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+","+"%s"+q2
    data=(co,no,ap,cn,id,cl,ac,cf,ind,fr,ty)
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
def cambiodatoUsauarios(co,dato,valor):
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
def todosdatosUsuarios(co):
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
def sinavalUsuarios(cl):
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

def main():
    # co=input('escriba el coreo: ')
    # tal=input('campo a leer: ')
    # # encontrado=existeUsuarios(co=co)
    # print(encontrado)
    # co='jcmejia@live.com'
    # tal='contrasena'
    # dato = datotalUsuarios(co=co,tal=tal)
    # print(dato)
    # co='aaaxpr@prueba.com'
    # no='name prueba'
    # ap='apellido prueba'
    # cn='dlfjd324'
    # id=''
    # cl='Serrezuela'
    # cf=''
    # ind=2.6
    # fr='2020-06-20'
    # ty=1
    # ac='NO'
    # crearUsuario(co=co,no=no,ap=ap,cn=cn,id=id,cl=cl,ac=ac,cf=cf,ind=ind,fr=fr,ty=ty)
    # co=input('escriba el coreo: ')
    # dato=input('campo que desea cambiar: ')
    # valor= input('nuevo valor: ')
    # cambiodatoUsauarios(co=co,dato=dato,valor=valor)
    # co=input('escriba el coreo: ')
    # datusuario=todosdatosUsuarios(co=co)
    # print('los datos del usuairo son:')
    # print(datusuario)
    cl=input('escriba el club: ')
    sinaval=sinavalUsuarios(cl=cl)
    print('los jugadores sin aval son:')
    print(sinaval)

if __name__ == '__main__':
    main()
