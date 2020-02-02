from gtfs_helper import *
from flask_socketio import SocketIO, emit
from flask import render_template, request, Flask, escape, Response
from time import sleep
from threading import Thread, Event
#stop_ids = pd.read_csv('https://openmobilitydata-data.s3-us-west-1.amazonaws.com/public/feeds/mta/79/20181221/original/stops.txt')
stop_ids = pd.read_csv('stop_ids.csv')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)

thread = Thread()
thread_stop_event = Event()
stop = ''
direction = ''

def generate_update():
    while not thread_stop_event.isSet():
        global stop
        global direction
        update=get_time(stop, direction)
        socketio.emit('trip_updates', {'update': update}, namespace='/test')
        socketio.sleep(1)
    else:
        print("No request received")

@app.route('/')
def getupdate():
    stop_names =  set(stop_ids['stop_name'].to_list())
    return render_template('update.html',
                           stop_names = stop_names,
                         )

@socketio.on('form submit', namespace='/test')
def form_submit(msg):
    print(msg['stop'], msg['direction'])
    global stop
    global direction
    stop = msg['stop']
    direction = msg['direction']
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(generate_update)

# @app.route('/raw_update', methods=["POST"])
# def getRaw():
#     stop_names =  set(stop_ids['stop_name'].to_list())
#     # stop = 'None'
#     # direction = 'None'
#     if request.method == 'POST':
#         stop = request.form.get('stops')
#         direction = request.form.get('direction')
#     return render_template('update.html',
#                            update=get_time(stop, direction),
#                            stop_names = stop_names,
#                            stop = stop,
#                            direction = direction)
if __name__ == "__main__":
    socketio.run(app)
    # app.run(debug=True)
