import psycopg2

try:
    # 1. Plug the cable into the PostgreSQL engine
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="Rahuln04"  # <-- Put your real pgAdmin password here!
    )

    # 2. Open a pointer/marker channel to write commands
    cursor = connection.cursor()

    # 3. Tell the channel what SQL command you want to execute
    cursor.execute("DELETE FROM users WHERE id = 4;")

    # 4. CRITICAL: Save your changes permanently to the disk
    connection.commit()

    print("Success! Python successfully deleted the user through the bridge.")

except Exception as error:
    print("Something went wrong:", error)

finally:
    # 5. Always unplug your cables when finished to save memory
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()