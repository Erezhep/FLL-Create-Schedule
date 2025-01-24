from flask import Flask, render_template, url_for, request
from schedule import read_excel_file


html = '<script>alert("bad")</script>'

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", active_page = "home")


@app.route("/create_schedule", methods = ['GET', 'POST'])
def create_schedule():
    if request.method == 'GET':
        return render_template("create_schedule.html", active_page = "create", upload_file = '')
    if request.method == 'POST':
        
        file = request.files.get('excel_file')  # Adjust the field name to match the form's file input name
        
        if not file:
            # If no file is uploaded, display an error message on the form
            return render_template("create_schedule.html", active_page="create", upload_file='upload', error = '')
        try:
            data = read_excel_file(file)

            matches = ['Тренировачная игра', 'Официальная игра 1', 'Официальная игра 2', 'Официальная игра 3']

            # After processing the file, render the result page
            return render_template("result.html", data = data, games = matches)
        except Exception as e:
            return render_template("create_schedule.html", active_page="create", upload_file='upload', error = f'{e}')
        
    
if __name__ == "__main__":
    app.run(host="localhost",
            port=8000,
            debug=True)