import json
import datetime
import psycopg2



def credenciales(usuario):
    # Specify the filename
    filename = "database_config.json"

    # Load the JSON data from the file
    with open(filename, "r") as json_file:
        data = json.load(json_file)

    # Choose a user (e.g., "Admin" or "SanPedro")
    chosen_user = usuario

    # Get the attributes for the chosen user
    user_attributes = data.get(chosen_user, None)
    return user_attributes


def crearTablasPostgres(credenciales):
    import psycopg2

    conn = psycopg2.connect(
        database=credenciales["database"],
        user=credenciales["user"],
        password=credenciales["password"],
        host=credenciales["host"],
        port=credenciales["port"]
    )

    cursor = conn.cursor()
    table_name = 'huellacarbono'
    cursor.execute(
        f"SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_name='{table_name}'")
    result = cursor.fetchone()

    if result is None:
        ## If the table doesn't exist, create it
        cursor.execute('''CREATE TABLE huellacarbono (
            ID SERIAL PRIMARY KEY,
            CampoID TEXT,
            Valor REAL,
            Planta TEXT,
            fecha TEXT
        );''')

    conn.commit()  # Don't forget to commit the changes after creating tables
    conn.close()


def columnaLogs(credenciales):
    conn = psycopg2.connect(
        database=credenciales["database"],
        user=credenciales["user"],
        password=credenciales["password"],
        host=credenciales["host"],
        port=credenciales["port"]
    )

    cursor = conn.cursor()
    cursor.execute('''
            ALTER TABLE huellacarbono
            ADD logfecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        END''')
    conn.commit()  # Don't forget to commit the changes after creating tables
    conn.close()


def pruebaHuella(credenciales,campoid, Valor, Planta, fecha):

        conn = psycopg2.connect(
            database=credenciales["database"],
            user=credenciales["user"],
            password=credenciales["password"],
            host=credenciales["host"],
            port=credenciales["port"]
        )

        cursor = conn.cursor()

        query = f'''
        INSERT INTO huellacarbono (
            campoid, valor, planta, fecha
        ) VALUES ('{campoid}', '{Valor}', '{Planta}', '{fecha}')
        '''

        cursor.execute(query)

        # Commit the transaction
        conn.commit()

        # Close the connection
        conn.close()


def pruebaHuellaDf(credenciales, df):
    # Connect to the database
    conn = psycopg2.connect(
        database=credenciales["database"],
        user=credenciales["user"],
        password=credenciales["password"],
        host=credenciales["host"],
        port=credenciales["port"]
    )

    cursor = conn.cursor()

    try:
        # Iterate over the rows of the DataFrame
        for index, row in df.iterrows():
            # Extract values from the DataFrame
            campoid = row['campoid']
            Valor = row['valor']
            Planta = row['planta']
            fecha = row['fecha']
            logfecha=datetime.datetime.now()

            # Construct the SQL query
            query = f'''
                    INSERT INTO huellacarbono (
                        campoid, valor, planta, fecha,logfecha
                    ) VALUES ('{campoid}', '{Valor}', '{Planta}', '{fecha}','{logfecha}')
                    '''

            # Execute the SQL query
            cursor.execute(query)

        # Commit the transaction
        conn.commit()
        print("Data inserted successfully!")

    except psycopg2.Error as e:
        # Print the error message
        print("Error:", e)

    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()


def datosConsolidados(credenciales):

    conn = psycopg2.connect(
        database=credenciales["database"],
        user=credenciales["user"],
        password=credenciales["password"],
        host=credenciales["host"],
        port=credenciales["port"]
    )

    cursor = conn.cursor()

    cursor.execute("select * from huellacarbono")

    # Fetch the result
    queryData = cursor.fetchall()

    return queryData

def borrar_pruebas(credenciales):
    # Establecer la conexión
    conn = psycopg2.connect(
        database=credenciales["database"],
        user=credenciales["user"],
        password=credenciales["password"],
        host=credenciales["host"],
        port=credenciales["port"]
    )
    cursor = conn.cursor()

    query = "DELETE FROM huellacarbono;"
    cursor.execute(query)


    conn.commit()
    # Cerrar el cursor y la conexión
    conn.close()



# cred=credenciales("admin")
# borrar_pruebas(cred)
# columnaLogs(cred)
# pruebaHuella(cred,'7ya',77,'Cartagena','2024-05-02')


