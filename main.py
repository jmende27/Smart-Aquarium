from kivy.lang import Builder
from kivy.app import App
from kivy.network.urlrequest import UrlRequest
from kivy.properties import NumericProperty, StringProperty, DictProperty
#import json
import urllib
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

KV = '''
#:import json json
#:import C kivy.utils.get_color_from_hex

GridLayout:
    cols: 1
    spacing: '1dp'
    padding: '0.1dp', '0.1dp', '0.1dp', '0.1dp'
    Button:
        text: 'Set lights to Normal Mode'
        background_normal: ''
        background_color: 1,.7,0,1
        on_press: app.send_message("normal")
    Button:
        text: 'Set lights to Morning Mode'
        background_normal: ''
        background_color: 1,.7,0,1
        on_press: app.send_message("morning")
    Button:
        text: 'Set lights to Midday Mode'
        background_normal: ''
        background_color: 1,.7,0,1
        on_press: app.send_message("midday")
    Button:
        text: 'Set lights to Afternoon Mode'
        background_normal: ''
        background_color: 1,.7,0,1
        on_press: app.send_message("afternoon")
    Button:
        text: 'Lights off'
        background_normal: ''
        background_color: .1,.1,.1,1
        on_press: app.send_message("off")
    Button:
        text: 'GET'
        on_press: app.fetch_content("http://192.168.1.20/phoneApp")
    TextInput:
        readonly: True
        size_hint: (5,None)
        height: 450
        text: app.result_text
    Button:
        text: 'QUIT'
        background_normal: ''
        background_color: 1,0,0,1
        on_press: app.stop()

'''


class UrlExample(App):
    status = NumericProperty()
    result_text = StringProperty()
    headers = DictProperty()
    mode = StringProperty()

    def build(self):
        return Builder.load_string(KV)

    def fetch_content(self, url):
        self.cleanup()
        UrlRequest(
            url,
            on_success=self.on_success,
            on_failure=self.on_failure,
            on_error=self.on_error
        )

    def cleanup(self):
        self.result_text = ''
        self.status = 0
        self.headers = {}

    def display_data(self, data):
        dstring = "\t\t\ttmp  -  wL  -  NH3  -  pH  -  status  -  charge\n\n  "
        for item in data:
            if item == "]":
                dstring += "\n"
            elif item == "[" or item == "'":
                continue
            elif item == ",":
                dstring += " "
            else:
                dstring += item
            
        dstring = dstring[:-2]
        return dstring

    def light_Mode(self, msg):
        if msg == "morning":
            return "Lights set to Morning Mode"
        elif msg == "midday":
            return "Lights set to Midday Mode"
        elif msg == "afternoon":
            return "Lights set to Afternoon Mode"
        elif msg == "off":
            return "Lights are off"
        else:
            return "Lights are set according to time of day"

    def on_success(self, req, result):
        self.cleanup()
        headers = req.resp_headers
        content_type = headers.get('content-type', headers.get('Content-Type'))
        self.result_text = self.display_data(result)
        self.status = req.resp_status
        self.headers = headers

    def on_failure(self, req, result):
        self.cleanup()
        self.result_text = result
        self.status = req.resp_status
        self.headers = req.resp_headers

    def on_error(self, req, result):
        self.cleanup()
        self.result_text = str(result)

    count = 1

    def send_message(self, message):
        self.mode = self.light_Mode(message)
        POST_data = self._prepare_data(message)
        self._send_message(POST_data)

    def _prepare_data(self, message):
        auth_data = {'message': message}
        auth_data = urllib.parse.urlencode(auth_data)
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        return {'auth_data': auth_data, 'headers': headers}

    def _send_message(self, POST_data):
        UrlRequest(
            url='http://192.168.1.20/phoneApp',
            req_body=POST_data['auth_data'],
            req_headers=POST_data['headers'],
        )


if __name__ == '__main__':
    UrlExample().run()
