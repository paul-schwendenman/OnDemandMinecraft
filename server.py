from flask import Flask, render_template, request
from flask_cors import CORS
from configuration import Config
import boto3
import time

app = Flask(__name__)
CORS(app)

# Main endpoint for loading the webpage
@app.route('/')
def loadIndex():
    return render_template('index.html')

@app.route('/initServerMC', methods=['POST'])
def initServerMC():
    inputPass = request.form['pass']

    message = "Password Incorrect!"

    if inputPass == Config.SERVER_PASSWORD:
        # Instantiate server here or return ip address if already running
        client = boto3.client(
            'ec2',
            aws_access_key_id=Config.ACCESS_KEY,
            aws_secret_access_key=Config.SECRET_KEY,
            region_name=Config.ec2_region
        )
        message = manageServer(client)

    print(message)
    return render_template('index.html', ipMessage=message)


# Gets IP Address for return to webpage otherwise boots server
def manageServer(client):
    returnString = 'ERROR'

    instanceIds = [Config.INSTANCE_ID]
    response = client.describe_instances(InstanceIds=instanceIds)
    reservations = response['Reservations']
    reservation = reservations[0]

    instances = reservation['Instances']

    print("\nSERVER INSTANCES\n")
    print(instances)
    print("\n")
    if len(instances) > 0:
        instance = instances[0]
        state = instance['State']
        stateName = state['Name']

        if (stateName == 'stopped') or (stateName == 'shutting-down'):
            #SETUP MULTIPROCESSING HERE INSTEAD OF REDIS
            returnString = startServer(client)
        elif stateName == 'running':
            returnString = 'IP: ' + instance['PublicIpAddress']
        else:
            returnString = 'ERROR'
    return returnString


# Starts the specified AWS Instance from the configuration
def startServer(client):
    # Gets proper variables to attempt to instantiate EC2 instance
    returnString = 'ERROR'
    instanceIds = [Config.INSTANCE_ID]
    response = client.start_instances(InstanceIds=instanceIds)

    stateCode = 0

    while not (stateCode == 16):
        time.sleep(3)

        print('\nAWS EC2 START RESPONSE\n')
        print(str(response))
        print('\n')

        response = client.describe_instances(InstanceIds=instanceIds)
        reservations = response['Reservations']
        reservation = reservations[0]

        instances = reservation['Instances']
        instance = instances[0]

        state = instance['State']
        stateCode = state['Code']

        print("\nSERVER INSTANCES\n")
        print(instances)
        print("\n")

    ipAddress = instance['PublicIpAddress']
    returnString = 'Server is starting, this may take a few minutes.\nIP: ' + ipAddress
    return returnString


if __name__ == "__main__":
    app.run()
