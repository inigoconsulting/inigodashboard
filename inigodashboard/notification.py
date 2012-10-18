import json

class Notification(object):

    def __init__(self, request):
        self.request = request

    def peek(self):
        return [
            json.loads(m) for m in self.request.session.peek_flash()
        ]

    def pop(self):
        return [
            json.loads(m) for m in self.request.session.pop_flash()
        ]

    def notify(self, message, type_='info'):
        self.request.session.flash(
            json.dumps({'type': type_, 'message': message})
        )
