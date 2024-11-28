##MODELO PARA REALIZAR LAS DISTINTAS CONSULTAS
##
from flask import jsonify, request
from modelo.coneccion import db_connection

#funcion que busca a un determinado usuario: reporte y   borrar
def buscar_usuario(codigo):
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("""select cedula_identidad,nombre,primer_apellido,segundo_apellido,
        to_char(fecha_nacimiento,'YYYY-MM-DD') as fecha_nacimiento FROM usuarios WHERE cedula_identidad = %s""", (codigo,))
        datos = cur.fetchone()
        conn.close()
        if datos != None:
            usuario = {'cedula_identidad': datos[0], 'nombre': datos[1],
                       'primer_apellido': datos[2], 'segundo_apellido': datos[3],
                       'fecha_nacimiento': datos[4]}
            return usuario
        else:
            return None
    except Exception as ex:
            raise ex

class UsuarioModel():
    @classmethod
    def listar_usuarios(self):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""select cedula_identidad,nombre,primer_apellido,segundo_apellido,
             to_char(fecha_nacimiento,'YYYY-MM-DD') as fecha_nacimiento from usuarios""")
            datos = cur.fetchall()
            usuarios = []
            for fila in datos:
                usuario = {'cedula_identidad': fila[0],
                       'nombre': fila[1],
                       'primer_apellido': fila[2],
                       'segundo_apellido': fila[3],
                       'fecha_nacimiento': fila[4]}
                usuarios.append(usuario)
            conn.close()
            return jsonify({'usuarios': usuarios, 'mensaje': "Usuarios listados.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Errorr", 'exito': False})

    @classmethod
    def lista_usuario(self,codigo):
        try:
            usuario = buscar_usuario(codigo)
            if usuario != None:
                return jsonify({'usuarios': usuario, 'mensaje': "usuario encontrado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})
        
    @classmethod
    def registrar_usuario(self):
        try:
            usuario = buscar_usuario(request.json['cedula_identidad'])
            if usuario != None:
                return jsonify({'mensaje': "Cedula de identidad  ya existe, no se puede duplicar.", 'exito': False})
            else:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute('INSERT INTO usuarios values(%s,%s,%s,%s,%s)', (request.json['cedula_identidad'], request.json['nombre'], request.json['primer_apellido'],
                                                                            request.json['segundo_apellido'], request.json['fecha_nacimiento']))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Usuario registrado.", 'exito': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

    @classmethod
    def eliminar_usuario(self,codigo):
        try:
            usuario = buscar_usuario(codigo)
            if usuario != None:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM usuarios WHERE cedula_identidad = %s", (codigo,))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Usuario eliminado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

    @classmethod
    def actualizar_usuario(self,codigo):
        try:
            usuario = buscar_usuario(codigo)
            if usuario != None:
                conn = db_connection()
                cur = conn.cursor()
                cur.execute("""UPDATE usuarios SET nombre=%s, primer_apellido=%s, segundo_apellido=%s,
                fecha_nacimiento=%s WHERE cedula_identidad=%s""",
                        (request.json['nombre'], request.json['primer_apellido'], request.json['segundo_apellido'], request.json['fecha_nacimiento'], codigo))
                conn.commit()
                conn.close()
                return jsonify({'mensaje': "Usuario actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Usuario no encontrado.", 'exito': False})
        except Exception as ex:
                return jsonify({'mensaje': "Error", 'exito': False})

    @classmethod
    def promedio_edad(self):
        try:
            conn = db_connection()
            cur = conn.cursor()
            cur.execute("""select avg(extract(year from age(now(),fecha_nacimiento))) 
            as promedio_edades from usuarios""")
            datos = cur.fetchone()
            conn.close()
            if datos != None:
                return jsonify({'promedioEdad': datos[0], 'exito': True})
            else:
                return jsonify({'mensaje': "No existe promedio.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error", 'exito': False})

    @classmethod
    def estado(self):
        return jsonify({"nameSystem": "api-users", "version": "0.0.1", 
                        "developer": "Orlando Choque Ayma", "email":"orlando_choque@hotmail.com",
                        'exito': True})
        