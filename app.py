from flask import Flask, render_template, request, redirect, url_for, jsonify

# Create an instance of the Flask class
app = Flask(__name__)

# Define the home route
@app.route('/')
def home():
    return render_template('index.html')  # Rendering the index template

# Define an additional route (example)
@app.route('/about')
def about():
    return render_template('about.html')  # Rendering the about template

# Define a route that accepts POST requests (for forms)
# @app.route('/submit', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         data = request.form['user_data']  # Grab data from form input
#         # Handle the data here
#         return redirect(url_for('home'))  # Redirect to home page after form submission
@app.route('/colleges')
def colleges():
    import config
    import mysql.connector as sql
    search_query = request.args.get('search', '').strip()

    mydb = sql.connect(
      host=f"{config.DB_CONFIG['host']}",
      user=f"{config.DB_CONFIG['user']}",
      password=f"{config.DB_CONFIG['password']}",
      database=f"{config.DB_CONFIG['database']}"
    )
    mycursor = mydb.cursor()

    # Fetch filtered or all colleges based on search
    if search_query:
        sql_query = """
            SELECT * FROM Colleges 
            WHERE name LIKE %s 
            OR location LIKE %s
        """
        params = (f"%{search_query}%", f"%{search_query}%")
        mycursor.execute(sql_query, params)
    else:
        mycursor.execute("SELECT * FROM Colleges")

    data = mycursor.fetchall()
    colleges_list = []
    for row in data:
        college = {
            "name": row[1],        # Adjust indices to match your table schema
            "location": row[2],
            "courses_offered": row[3],
            "fees": row[4],
            "ranking": row[5],
            "facilities": row[6],
            "website": row[7]
        }
        colleges_list.append(college)

    mycursor.close()
    mydb.close()
    return jsonify(colleges_list)
    
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
