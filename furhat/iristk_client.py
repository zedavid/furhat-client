import json
import uuid
from threading import Thread


class IristkClient(object):

    def __init__(self, client, client_name, callback=None):
        self.client = client
        self.client_name = client_name
        self._is_listening = False

    def start_listening(self, callback):
        self._is_listening = True
        thread = Thread(target=self.socket_listener, args=(self.client, callback))
        thread.deamon = True
        thread.start()

    def socket_listener(self, client, callback):
        data = ''
        while self._is_listening:
            packet = client.recv(1)
            if not packet:
                # The socket has been closed.
                break
            data += packet.decode()
            if '\n' in data:
                data = data.replace('\n', '')
                if not data.startswith('EVENT') and not data.startswith('SUBSCRIBE'):
                    try:
                        json_data = json.loads(data)
                        callback(json_data)
                    finally:
                        data = ''
                else:
                    data = ''

    def disconnect(self):
        self._is_listening = False
        if self.client:
            self.client.send('CLOSE\n'.encode())

    def attend_user(self, agent, user):
        self._send_event('action.attend', agent, {'target': user})

    def attend_nobody(self, agent):
        self._send_event('action.attend', agent, {'target': 'nobody'})

    def attend_all(self, agent):
        self._send_event('action.attend.all', agent, {})

    def attend_location(self, agent, location, mode='default'):
        self._send_event('action.attend', agent, {'location': location, 'mode': mode})

    def gaze(self, agent, location, mode='default'):
        self._send_event('furhatos.event.actions.ActionGaze', {'location': location, 'speed': 2})

    def gesture(self, agent, gesture_name):
        self._send_event('furhatos.event.actions.ActionGesture', {'name': gesture_name})

    def say(self, agent, text, audio_file=None):
        event_data = {'text': text}
        if audio_file:
            event_data['audio'] = audio_file
        self._send_event('furhatos.event.actions.ActionSpeech', event_data)

    def _send_event(self, event_name, specialised_event):
        event = {
            'event_name': event_name
        }
        event.update(specialised_event)
        event_msg = '{}\n'.format(json.dumps(event)).encode('utf8')
        self.client.send('EVENT {} -1 {}\n'.format(event_name, len(event_msg)).encode())
        self.client.send(event_msg)


