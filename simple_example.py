from furhat import connect_to_iristk


FURHAT_IP = '137.195.27.135' # Furhat IP address
FURHAT_AGENT_NAME = 'system' # Furhat agent name. Can be found under "Connections" in the furhat web-GUI


with connect_to_iristk(FURHAT_IP,debug=True) as furhat_client:
    def event_callback(event):
        if event['event_name'] == 'furhatos.event.monitors.MonitorGaze':
            return
        print(event) # Receives each event the furhat sends out.

    furhat_client.start_listening(event_callback) # register our event callback receiver
    furhat_client.say(FURHAT_AGENT_NAME, 'hello') # Make furhat say hello

    input() # Press enter to quit
