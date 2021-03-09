from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os.path
import pandas
from geopy.geocoders import Nominatim

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template("homepage.html")


@app.route('/success', methods=['POST'])
def uploaded():
    global new_file
    if request.method == 'POST':
        file = request.files["file"]
        file.save("Uploaded" + secure_filename(file.filename))
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1]
        if file_ext == ".csv":
            df = pandas.read_csv(file)
        elif file_ext == ".xlsx":
            df = pandas.read_excel(file)
        else:
            return render_template("homepage.html", text="Please make sure that you upload only csv file or excel file")
        list_of_columns = df.columns
        if ("address" in list_of_columns) or ("Address" in list_of_columns):
            geolocator = Nominatim(user_agent="app")
            if "Address" in list_of_columns:
                for a in df["Address"]:
                    location = geolocator.geocode(a)
                    df["Latitude"] = location.latitude
                    df["Longitude"] = location.longitude
            elif "address" in list_of_columns:
                for a in df["address"]:
                    location = geolocator.geocode(a)
                    df["Latitude"] = location.latitude
                    df["Longitude"] = location.longitude
            new_file = df.to_csv("Your File.csv")
            return render_template("success.html", data=df)
        else:
            return render_template("homepage.html",
                                   text="Please make sure that you have a column named address or Address in your file")
    return render_template("homepage.html")


@app.route('/download')
def download():
    return send_file("Your File.csv", attachment_filename="Your File.csv", as_attachment=True)

if __name__ == "__main__":
    app.debug = True
    app.run()
