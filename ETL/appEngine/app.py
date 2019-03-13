# [Start App]
import os
import ingestUSChildNamesBQ
import flask

# [START Config]
app = flask.Flask(__name__)

# [END Config]

@app.route('/')
def welcome():
    return 'Testing out app engine'

@app.route('/ingest')
def ingestNames():
    ingestUSChildNamesBQ.ingestNextYear()

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]

