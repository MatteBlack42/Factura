from flask import Flask, render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL


app = Flask(__name__)



#conexion bd
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="Factura"
mysql = MySQL(app)

#sesion
app.secret_key="mysecretkey"

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/Index")
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts")
    data=cur.fetchall()
    return render_template("index.html", contacts = data)
@app.route("/Mostrar")
def Mostrar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts")
    data=cur.fetchall()
    return render_template("editCli.html", contacts = data)

@app.route("/add_contact", methods=["POST"])
def add_contact():
    if request.method=="POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        direccion = request.form["direccion"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts (nombre, telefono, email,direccion) VALUES (%s,%s,%s,%s)",
            (nombre,telefono,email,direccion))
        mysql.connection.commit()
        flash("Cliente agregado")
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE idCliente = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('editar_cliente.html', contact = data[0])
@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        direccion = request.form['direccion']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET nombre = %s,
                email = %s,
                telefono = %s,
                direccion= %s,
            WHERE id = %s
        """, (nombre, email, telefono, idCliente))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Mostrar'))

@app.route('/eliminar/<string:id>', methods = ['POST','GET'])
def eliminar_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE idCliente = {0}'.format(id))
    mysql.connection.commit()
    flash('El Cliente fue eliminado')
    return redirect(url_for("Mostrar"))
######################################################
#Producto
@app.route("/Producto")
def Producto():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto")
    data=cur.fetchall()
    return render_template("Producto.html", producto = data)


@app.route("/agregar_Producto", methods=["POST"])
def agregar_Producto():
    if request.method=="POST":
        idPro = request.form["idPro"]
        nombrePro = request.form["nombrePro"]
        precio = request.form["precio"]
        stock = request.form["stock"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO producto (idPro, nombrePro, precio,stock) VALUES (%s,%s,%s,%s)",
            (idPro,nombrePro,precio,stock))
        mysql.connection.commit()
        flash("El producto fue agregado")
        return redirect(url_for('Producto'))

@app.route("/eliminar_Producto/<string:idPro>" , methods = ['POST','GET'])
def eliminar_Producto(idPro):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM producto WHERE idPro = {0}'.format(idPro))
    mysql.connection.commit()
    flash('El Producto fue eliminado')
    return redirect(url_for('Producto'))
##############################################################################
#Factura
@app.route("/lista", methods = ["POST","GET"])
def lista(idProd):
    cur = mysql.connection.cursor()
    cur.execute("SELECT FROM producto WHERE idPro={idProd}")
    mysql.connection.commit()
    return redirect(url_for('Index'), producto= data)

@app.route("/factura")
def factura():
    return redirect("/factura.html")
     

























if __name__ =='__main__':
    app.run(port=3000,debug=True)