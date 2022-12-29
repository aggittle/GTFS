from gtfs_helper import *

#stop_ids = pd.read_csv('https://openmobilitydata-data.s3-us-west-1.amazonaws.com/public/feeds/mta/79/20181221/original/stops.txt')
stop_ids = pd.read_csv('stop_ids.csv')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

app.config.update(
CELERY_BROKER_URL = 'redis://localhost:6379/0',
CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

socketio = SocketIO(app, async_mode='eventlet',logger=True,message_queue='redis://localhost:6379/0', engineio_logger=True)
celery = make_celery(app)
init = 0
result = None
thread = Thread()
thread_stop_event = Event()
stop = ''
direction = ''

_update = {}

# def global_funct(update):
#     print('global funct triggered')
#     socketio.emit('celery_message', {'update': _update}, namespace='/test')

@celery.task(name="task.message", bind=True, base=AbortableTask)
def generate_update(self, stop, direction):
    global _update
    local_socketio = SocketIO(message_queue='redis://',  async_mode='threading')
    print('local_socketio: ',local_socketio)
    print('Celery task starting..')
    while True:
        if self.is_aborted():
            return
        new_update=get_time(stop, direction)
        if new_update != _update and new_update != {}:
            _update = new_update
            print('**Emitting update: ', _update)
            # global_funct(_update)
            local_socketio.emit('trip_updates', {'update': _update}, namespace='/test')
            local_socketio.sleep(0)
        else:
            print("No new update")

@app.route('/')
def getupdate():
    stop_names =  set(stop_ids['stop_name'].to_list())
    return render_template('update.html',
                           stop_names = stop_names,
                         )

@socketio.on('client_connect', namespace='/test')
def print_connect_message(msg):
    print(msg['data'])

@socketio.on('celery_message', namespace='/test')
def send_to_client(msg):
    print('CELERY MESSAGE RECEIVED')
    update = msg['update']
    socketio.emit('trip_updates', {'update': update}, namespace='/test')

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Disconnected')

@socketio.on('form submit', namespace='/test')
def form_submit(msg):
    global init
    global result
    global stop
    global direction
    print(msg['stop'], msg['direction'])
    print('INIT: ' + str(init))

    stop = msg['stop']
    direction = msg['direction']
    # need visibility of the global thread object
    # global thread
    if init == 0:
        init += 1
        result = generate_update.delay(stop, direction)
        # result.wait()
    else:
        result.abort()
        result = generate_update.delay(stop, direction)
        # result.wait()



    #Start the random number generator thread only if the thread has not been started before.
    # if not thread.is_alive():
    #     print("Starting Thread")
    #     thread = socketio.start_background_task(generate_update)

@app.route('/raw_update', methods=["POST"])
def getRaw():
    stop_names =  set(stop_ids['stop_name'].to_list())
    # stop = 'None'
    # direction = 'None'
    if request.method == 'POST':
        stop = request.form.get('stops')
        direction = request.form.get('direction')
    return render_template('update.html',
                           update=get_time(stop, direction),
                           stop_names = stop_names,
                           stop = stop,
                           direction = direction)
if __name__ == "__main__":
    socketio.run(app, debug=True)
    app.run(debug=True)
