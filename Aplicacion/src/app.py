#Request, redirect , url for: Para redireccionar
#Flash enviar mensajes entre vistas:
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from flask_mysqldb import MySQL
#Para enviar email
import os
from email.message import EmailMessage
import ssl
import smtplib



app = Flask(__name__)

#MySql Connnection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '!Qpasdb'
app.config['MYSQL_DB'] = 'QEOApp'
mysql = MySQL(app)

#Settings (session guardada en memoria)
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    return showMenu()

@app.route('/menu')
def showMenu():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM menu')
    data = cur.fetchall()
    return render_template('menu.html', menuTupla = data)

@app.route('/add_order', methods=['POST'])
def add_order():
    if request.method =='POST':
        #default
        idCliente = 1

        total = 222

        #sin facturar
        facturado = 0
        
        #fecha
        now = datetime.utcnow()
        idMesa = request.form['idMesa']
        
        #Listas con el menu y las cantidades del form
        listadoMenu = request.form.getlist('idMenu')
        cantidad = request.form.getlist('iCantidad')
        comentarios = request.form.getlist('txtComentarios')
        
        print(comentarios)

        #Insertar cabezado
        cur= mysql.connection.cursor()
        cur.execute('INSERT INTO orden (id_cliente, id_mesa, fecha, total, facturado, id_estado, id_metodo_pago) VALUES(  %s, %s,%s, %s, %s, %s, %s)', (idCliente, int(idMesa), now.strftime('%Y-%m-%d %H:%M:%S'), total, facturado,1,1) )
        mysql.connection.commit()

        #ultimo registro insertado, suena medio peligroso de esta forma.
        cur.execute('SELECT LAST_INSERT_ID() FROM orden')
        data = cur.fetchall()
     
        #crear diccionario con ordenes.
        order = dict(zip(listadoMenu,cantidad))
        orderComent = dict(zip(listadoMenu,comentarios))

       
        for idMenu, cantidad in order.items():
            if cantidad != '0':
                #traer comentario
                comentario = orderComent[idMenu]
                #Insertar registros
                add_order_detail(data[0],idMenu, cantidad, comentario)

        #flash('Orden Agregado OK')
        return redirect(url_for('medioPago', id=data[0][0]))
       
def add_order_detail(idOrden, idMenu, cantidad, comentario):
    if idOrden:
        cur= mysql.connection.cursor()
        cur.execute('SELECT precio_venta FROM menu WHERE id_menu = %s', idMenu)
        precio = cur.fetchall() 

        cur= mysql.connection.cursor()
        cur.execute('INSERT INTO orden_detalle (id_orden, id_menu, id_estado, precio,comentarios, cantidad)  VALUES( %s, %s,%s, %s,%s, %s)',(idOrden,idMenu,1,precio, comentario, cantidad) )
        
        #Actualizar total de factura
        updateTotalFactura(idOrden)
        
        mysql.connection.commit()
    pass

def updateTotalFactura(id):
    cur= mysql.connection.cursor()
    cur.execute('SELECT SUM(precio*cantidad) FROM orden_detalle WHERE id_orden = %s ' , id)
    total = cur.fetchall() 
    
    cur.execute("""
                    UPDATE orden SET total = %s WHERE id_orden = %s
                """,(total, id))


@app.route('/mediopago/<id>')
def medioPago(id):
    return render_template('medioPago.html', data = id)

@app.route('/add_medioPago/<id>', methods=['POST'])
def add_medioPago(id):
    if request.method == 'POST':
        #traer valores del form
        numeroOrden = id
        nombreCompleto = request.form['nombreCompleto']
        telefono = request.form['telefono']
        email = request.form['email']
        
        medioPago = request.form.get('radioMedioPago')
        
        #Cur = variable para realizar consultas
        cur= mysql.connection.cursor()
        cur.execute('INSERT INTO clientes (email, nombrecompleto, telefono) VALUES( %s, %s, %s)',(email,nombreCompleto,telefono) )
        mysql.connection.commit()
        
        #ultimo cliente registrado
        cur.execute('SELECT LAST_INSERT_ID() FROM clientes')
        resultados = cur.fetchone()
        
        idcliente = resultados[0]
        
        operacion = 'UPDATE orden SET id_cliente = '+ str(idcliente) +', id_metodo_pago = '+ str(medioPago) +' WHERE id_orden ='+numeroOrden
        cur.execute(operacion)
        mysql.connection.commit()
        
        #enviar mail
        tipoMail = 'altaOrden'
        enviar_mail(email,numeroOrden,nombreCompleto,tipoMail)
        
        flash('Gracias por su Pedido - Revise su correo electronico -El numero de pedido es: '+ numeroOrden )
       
        #return redirect(url_for('showMenu'))
        return render_template('ordenRecibida.html', ordenes = numeroOrden)


@app.route('/listado_orden')
def listado_orden():
    cur = mysql.connection.cursor()
    #cur.execute('SELECT * FROM orden')
    
    cur.execute("""
                SELECT * FROM orden o 
                    INNER JOIN clientes c
                        on o.id_cliente = c.id_cliente
                    INNER JOIN mesa m
                        on o.id_mesa = m.id_mesa
                """)

    data = cur.fetchall()
    return render_template('listado-orden.html', ordenes = data)

#listado de ordenes a editar
@app.route('/edit-orden/<id>')
def edit_orden(id):
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT * FROM orden o 
                    INNER JOIN mesa m
                        on o.id_mesa = m.id_mesa
                WHERE o.id_orden= %s
                """, [id])
    data = cur.fetchall()
    return render_template('edit-orden.html', ordenes = data[0])

@app.route('/update-orden/<id>', methods = ['POST'])
def update_orden(id):
    if request.method == 'POST':
        facturado = request.form['sFacturado']
        entregado = request.form['sEntregado']
        lugarEntrega = request.form['sLugarEntrega']
        cur = mysql.connection.cursor()
        #los parametros los obtengo del form edit-cliente.html y el id por parametro

        cur.execute("""
            UPDATE orden
                SET facturado = %s,
                    id_estado = %s,
                    id_mesa = %s
            WHERE id_orden = %s

        """,(facturado, entregado ,str(lugarEntrega) ,id))

        #Ejecutar la conexion!
        mysql.connection.commit()
        
        #Si esta pendiente a retirar, enviar mail
        if (entregado =='2'):
            print("aca esto")
            cur = mysql.connection.cursor()
            cur.execute("""
                SELECT c.email, c.nombreCompleto
                    FROM orden o
                        INNER JOIN clientes c
                            ON o.id_cliente = c.id_cliente 
                WHERE o.id_orden = %s
                """,[id])
            resultados = cur.fetchone()
            email = resultados[0]
            nombreCompleto = resultados[1]
            tipoMail = 'estadoEntrega'
            
            enviar_mail(email,id,nombreCompleto,tipoMail)

        flash('Orden Actualizada Correctamente')
        return redirect(url_for('listado_orden'))
    pass

@app.route('/delete-orden/<string:id>')
def delete_orden(id):
    #Aca seria ideal manejar update de estado para ocultar y no hacer delete.
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM orden_detalle WHERE id_orden = {0}' .format(id))
    mysql.connection.commit()

    cur.execute('DELETE FROM orden WHERE id_orden = {0}' .format(id))
    mysql.connection.commit()

    flash('Orden Eliminada Correctamente')
    return redirect(url_for('listado_orden'))

#Delete de medio de pago por necesidad de redirect a Index
@app.route('/delete-orden/mp/<string:id>')
def delete_orden_medioPago(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM orden_detalle WHERE id_orden = {0}' .format(id))
    mysql.connection.commit()

    cur.execute('DELETE FROM orden WHERE id_orden = {0}' .format(id))
    mysql.connection.commit()

    #flash('Orden Eliminada')
    return redirect(url_for('Index'))   

def enviar_mail(email,OrdenId,NombreCompleto, tipoMail):
    #Queria usar un mail de gmil, pero no funcionaba el validador de telefono
    #Ideal ocultar la passwd con variable de entorno
    email_sender = 'pp3@jbanime.com'
    email_passwd= 'Srfl7Qf8ciWP2xx'
    email_receiver= email
    subjectName = NombreCompleto
    #parametros en tipoMail: altaOrden, estadoEntrega
    emailtype = tipoMail

    if(tipoMail =='altaOrden'):
        subject= 'Pedido Confirmado: ' + str(OrdenId)
        body="""
            Estimado {0}, 
            Su pedido {1} ya fue confirmado y esta proximo a prepararse.
            Gracias por elegirnos.

        """ .format(NombreCompleto,OrdenId)

    if(tipoMail =='estadoEntrega'):
            subject= 'Pedido: ' + str(OrdenId) + ' listo para retirar.'
            body="""
                Estimado {0}, 
                Su pedido {1} ya se encuentra listo para ser retirado.
                Gracias por elegirnos.

            """ .format(NombreCompleto,OrdenId)

    #objeto de EmalMessage
    em = EmailMessage()

    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('cpanel140.wnpservers.net',465, context=context) as smtp:
        smtp.login(email_sender,email_passwd)
        smtp.sendmail(email_sender,email_receiver, em.as_string())
    
    print('enviado')  

@app.route('/ordenRecibida')
def ordenRecibida():
   return render_template('ordenRecibida.html')

if __name__ == '__main__':
    app.run(port=4000, debug = True )


