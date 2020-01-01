from gtfs_helper import *
from flask import render_template, request, Flask, escape

#stop_ids = pd.read_csv('https://openmobilitydata-data.s3-us-west-1.amazonaws.com/public/feeds/mta/79/20181221/original/stops.txt')
stop_ids = pd.read_csv('stop_ids.csv')


app = Flask(__name__)



@app.route('/', methods=["POST", "GET", "PUT"])
def getupdate():
    stop_names =  set(stop_ids['stop_name'].to_list())
    stop = 'None'
    direction = 'None'
    if request.method == 'POST':
        stop = request.form.get('stops')
        direction = request.form.get('direction')
    return render_template('update.html',
                           update=get_time(stop, direction),
                           stop_names = stop_names)

if __name__ == "__main__":
    app.run(debug=True)
