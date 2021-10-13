from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from config import _MYSQL_HOST, _MYSQL_USER, _MYSQL_PASSWORD, _MYSQL_DB, _SECRET_KEY_APP
from flask_cors import CORS

# init
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# connection
app.config["MYSQL_HOST"] = _MYSQL_HOST
app.config["MYSQL_USER"] = _MYSQL_USER
app.config["MYSQL_PASSWORD"] = _MYSQL_PASSWORD
app.config["MYSQL_DB"] = _MYSQL_DB

mysql = MySQL(app)

# settings
app.secret_key = _SECRET_KEY_APP


# routes
@app.route("/clients", methods=["GET"])
def get_all_clients():
    """
    CLIENTS
    GET ALL
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM clients")
    data = cursor.fetchall()
    cursor.close()
    data_res = []
    for d in data:
        data_res.append({"id": d[0], "name": d[1]})
    message = {"message": "clients listed", "data": data_res}
    response = jsonify(message)
    response.status_code = 200
    return response


@app.route("/clients/<id>", methods=["GET"])
def get_one_client(id):
    """
    CLIENTS
    GET ONE
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM clients WHERE id = %s", (id))
    data = cursor.fetchall()
    cursor.close()
    data_res = {"id": data[0][0], "name": data[0][1]}
    message = {"message": "client listed", "data": data_res}
    response = jsonify(message)
    response.status_code = 200
    return response


# users
# get all
@app.route("/users", methods=["GET"])
def get_all_users():
    """
    USERS
    GET ALL
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    cursor.close()
    data_res = []
    for d in data:
        data_res.append({"id": d[0], "name": d[1], "team": d[2]})
    message = {"message": "users listed", "data": data_res}
    response = jsonify(message)
    response.status_code = 200
    return response


# get one
@app.route("/users/<id>", methods=["GET"])
def get_one_user(id):
    """
    USERS
    GET ONE
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id))
    data = cursor.fetchall()
    cursor.close()
    print(data)
    data_res = {"id": data[0][0], "name": data[0][1], "teamId": data[0][2]}
    message = {"message": "user listed", "data": data_res}
    response = jsonify(message)
    response.status_code = 200
    return response


# teams
# get all
@app.route("/teams", methods=["GET"])
def get_all_teams():
    """
    TEAMS
    GET ALL
    """
    cursor = mysql.connection.cursor()
    cursor.execute("select * from teams")
    data = cursor.fetchall()
    cursor.close()
    data_res = []
    for d in data:
        data_res.append({"id": d[0], "name": d[1]})
    message = {"message": "teams listed", "data": data_res}
    response = jsonify(message)
    response.status_code = 200
    return response


# get one
@app.route("/teams/<id>", methods=["GET"])
def get_one_team(id):
    """
    TEAMS
    GET ONE
    """
    cursor = mysql.connection.cursor()
    cursor.execute(
        "select  u.id as 'User id',u.name as 'User',t.id as 'Team Id', t.name as 'Team' from teams as t, users as u where u.teamId = t.id  and t.id =%s",
        (id),
    )
    data = cursor.fetchall()
    cursor.close()
    data_res = []
    for d in data:
        data_res.append({"id": d[0], "name": d[1], "teamId": d[2], "team": d[3]})
    # data_res = {"id": data[0][0], "name": data[0][1], "user": data[0][2], "userId": data[0][3]}
    message = {"message": "team listed", "data": data_res}
    response = jsonify(message)
    response.status_code = 200
    return response


# get sales by user
@app.route("/sales/users/<id>", methods=["GET"])
def get_sales_by_user(id):
    """
    sales
    GET by user
    """
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT s.id AS 'Id Venta', s.createdAt AS 'Fecha Venta',c.name AS 'Nombre Cliente',s.amount AS 'Monto',u.name AS 'Nombre Usuario',t.name AS 'Nombre Equipo'FROM sales AS s, users AS u, clients AS c, teams AS t WHERE s.userId = u.id and u.id = %s AND s.clientId = c.id AND u.teamId = t.id GROUP BY  s.id order by s.id",
        (id),
    )
    data = cursor.fetchall()
    cursor.close()
    data_res = []
    for d in data:
        data_res.append(
            {
                "id": d[0],
                "createdAt": d[1],
                "clientName": d[2],
                "amount": d[3],
                "userName": d[4],
                "teamName": d[5],
            }
        )
    message = {"message": "sales by user", "data": data_res}
    response = jsonify(message)
    response.status_code = 200
    return response


# get sales by teams
@app.route("/sales/teams/<id>", methods=["GET"])
def get_sales_by_teams(id):
    """
    sales
    GET by teams
    """
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT s.id AS 'Id Venta', s.createdAt AS 'Fecha Venta',c.name AS 'Nombre Cliente',s.amount AS 'Monto',u.name AS 'Nombre Usuario',t.name AS 'Nombre Equipo'FROM sales AS s, users AS u, clients AS c, teams AS t WHERE s.userId = u.id and t.id = %s AND s.clientId = c.id AND u.teamId = t.id GROUP BY  s.id order by s.id",
        (id),
    )
    data = cursor.fetchall()
    cursor.close()
    data_res = []
    for d in data:
        data_res.append(
            {
                "id": d[0],
                "createdAt": d[1],
                "clientName": d[2],
                "amount": d[3],
                "userName": d[4],
                "teamName": d[5],
            }
        )
    message = {"message": "sales by teams", "data": data_res}
    response = jsonify(message)
    response.status_code = 200
    return response


# get all
@app.route("/sales", methods=["GET"])
def get_all_sales():
    """
    sales
    GET ALL
    """
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT s.id AS 'Id Venta', s.createdAt AS 'Fecha Venta',c.name AS 'Nombre Cliente',s.amount AS 'Monto',u.name AS 'Nombre Usuario',t.name AS 'Nombre Equipo'FROM sales AS s, users AS u, clients AS c, teams AS t WHERE s.userId = u.id AND s.clientId = c.id AND u.teamId = t.id GROUP BY  s.id order by s.id",
    )
    data = cursor.fetchall()
    cursor.close()
    data_res = []
    for d in data:
        data_res.append(
            {
                "id": d[0],
                "createdAt": d[1],
                "clientName": d[2],
                "amount": d[3],
                "userName": d[4],
                "teamName": d[5],
            }
        )
    message = {"message": "sales listed", "data": data_res}
    response = jsonify(message)
    response.status_code = 200
    return response


@app.errorhandler(404)
def not_found(error=None):
    message = {"message": "Resource Not Found " + request.url, "status": 404}
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
