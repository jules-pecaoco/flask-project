from flask import redirect, render_template, request
import bcrypt

from config import cursor, session, connection, USER
from app.home import home
from app.auth.routes import USERNAME



# ROUTES
@home.route('/')
def index():
  data = getJoin()
  return render_template('base.html', table=data ,currentURL='dashboard')


@home.route('/dashboard')
def dashboard():
  data = getJoin()
  return render_template('content/dashboard.html', table=data, currentURL='dashboard')

@home.route('/table/<name>')
def renderTable(name):
  data = getData(name)
  columns = getColumnInfo(name)
  return render_template('content/tables.html', table=data, currentURL=name, tableHeaders=columns)


@home.route('/table/update/<name>', methods=['POST', 'GET'])
def editTable(name):
  table = name.capitalize()
  req = request.json
  data = updateData(table ,req)
  data = getData(table)
  columns = getColumnInfo(name)

  return render_template('content/tables.html', table=data, currentURL=table, tableHeaders=columns)


@home.route('/table/delete/<name>', methods=['POST', 'GET'])
def deleteTable(name):
  table = name.capitalize()
  req = request
  data = deleteData(table, req)
  data = getData(table)
  columns = getColumnInfo(name)

  return render_template('content/tables.html', table=data, currentURL=table, tableHeaders=columns)


@home.route('/table/add/<name>', methods=['POST', 'GET'])
def addTable(name):
  table = name.capitalize()
  req = request
  data = adddData(table, req)
  data = getData(table)
  columns = getColumnInfo(name)

  return render_template('content/tables.html', table=data, currentURL=table, tableHeaders=columns)
  



@home.route('/admin')
def admin():
  data = getUser()
  return render_template('content/admin.html', table=data, username=USERNAME, currentURL='admin')


@home.route('/admin/add', methods=['POST'])
def addAdmin():
  data = getUser()
  table = 'Admin'
  user = request.form['username']
  password = request.form['password']
  role = request.form['role']
  registerUser(user, password, role)
  data = getUser()

  return render_template('auth/admin.html', table=data, currentURL=table)


@home.route('/admin/update', methods=['POST'])
def updateAdmin():
  data = getUser()
  req = request.json
  updateUser(req)

  return render_template('auth/admin.html', table=data, currentURL='admin')

@home.route('/admin/delete', methods=['POST'])
def deleteAdmin():
  data = getUser()
  req = request.json
  deleteAdmin(req)

  return render_template('auth/admin.html', table=data, currentURL='admin')


def getUser():
  cursor.execute(f"SELECT AdminID, Username, Role FROM [Admin]")
  data = cursor.fetchall()
  cursor.commit()
  return data


def updateUser(request):
  data = request
  query = f"UPDATE [Admin] SET Username = '{data[1]}', Role = '{data[2]}' WHERE AdminID = '{data[0]}'"
  cursor.execute(query)
  cursor.commit()
  cursor.close()

def deleteUser(request):
  data = request.json
  query = f"DELETE FROM [Admin] WHERE [AdminID] = '{data}'"
  cursor.execute(query)
  
  cursor.commit()
  cursor.close()


def registerUser(username, password, role):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)

    new_user = USER(Username=username, Password=password, Role=role )
    session.add(new_user)
    session.commit()


@home.route('/logout')
def logout():
      return redirect('/auth')




  
# DATA RETRIEVAL AND MANIPULATION
def getData(TABLE):
  cursor.execute(f"SELECT * FROM [{TABLE}]")
  data = cursor.fetchall()
  cursor.commit()
  return data


def updateData(TABLE, request):
  data = request
  column = getColumnInfo(TABLE)
  did = data[0]
  cid = column[0]

  for index, col in enumerate(column):
    if index == 0:
      continue
    else: 
      data[index] = data[index].strip()
      if not data[index] or data[index] == 'None':
        query = f"UPDATE [{TABLE}] SET {col[0]} = NULL WHERE {cid[0]} = '{did}'"
      else:
        query = f"UPDATE [{TABLE}] SET {col[0]} = '{data[index]}' WHERE {cid[0]} = '{did}'"
      
      cursor.execute(query)

  connection.commit()
  cursor.close()


# DELETE ROUTE
def deleteData(TABLE, request):
  cursor = connection.cursor()
  data = request.json
  column = getColumnInfo(TABLE)
  cid = column[0]
  query = f"DELETE FROM [{TABLE}] WHERE {cid[0]} = '{data}'"
  cursor.execute(query)
  
  cursor.commit()
  cursor.close()

def adddData(TABLE, request):
  cursor = connection.cursor()
  data = request.json
  counter = 0
  q = ""

  # ALLOW INSERTION OF NULL/EMPTY
  for key, value in data.items():
    if counter == len(data) - 1:
      if not value:
        q += f"NULL"
      else:
        q += f"'{value}'"
      break

    if not value:
      q += f"NULL,"
    else:
      q += f"'{value}',"

    counter += 1
  

  query = f"INSERT INTO [{TABLE}] VALUES ({q})"
  try:
    cursor.execute(query)
  except Exception as e:
    result = {"message": str(e)}
    return result

  cursor.commit()
  cursor.close()






def getColumnInfo(TABLE):
  cursor = connection.cursor()
  query = f"""
    SELECT 
        c.name AS column_name,
        ic.DATA_TYPE AS data_type,
        CASE 
            WHEN c.is_nullable = 1 THEN 'Yes' 
            ELSE 'No' 
        END AS allows_null
    FROM 
        sys.columns c
    INNER JOIN 
        sys.tables t ON c.object_id = t.object_id
    INNER JOIN 
        INFORMATION_SCHEMA.COLUMNS ic ON t.name = ic.TABLE_NAME AND c.name = ic.COLUMN_NAME
    WHERE 
    t.name = '{TABLE}'
  """
  cursor.execute(query)
  columns = cursor.fetchall()
  cursor.commit()
  cursor.close()

  return columns

def getJoin():
  cursor.execute(f"""
                SELECT Customer.Customer, Books.Title, [Transaction].Quantity, [Transaction].Book_Unit_Price
                FROM [Transaction]
                INNER JOIN [Invoice] ON Invoice.InvoiceNumber = [Transaction].InvoiceID
                INNER JOIN [Customer] ON Customer.CustomerID = Invoice.CustomerID
                INNER JOIN Books on Books.ISBN = [Transaction].ISBN
                 """)
  data = cursor.fetchall()
  cursor.commit()
  return data


