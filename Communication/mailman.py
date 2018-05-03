import struct
import Common.variables as variables
import Common.functions as functions
from Common.variables import Headers


class Mailman:
    def __init__(self, socket, msg, header_type):
        if functions.is_string(msg):
            self.msg = msg
        else:
            self.msg = str(msg)
        self.socket = socket
        self.header_type = header_type

    def send(self):
        encoded_message = self.msg.encode("utf-8")
        header = struct.pack(variables.HEADER_DATA, self.header_type, len(encoded_message))  # add header
        message = header + encoded_message
        self.socket.sendall(message)


class Request(Mailman):
    def __init__(self, socket, msg, header_type):
        super().__init__(socket, msg, header_type)

    def send_request(self):
        super().send()


class Response(Mailman):
    def __init__(self, socket, msg, header_type):
        super().__init__(socket, msg, header_type)

    def send_response(self):
        super().send()


class ClickRequest(Request):
    def __init__(self, socket, field_id):
        super().__init__(socket, field_id, Headers.Request_click.value)


class ClickResponse(Response):
    def __init__(self, socket, field_id):
        super().__init__(socket, field_id, Headers.Response_click.value)


class JoinRequest(Request):
    def __init__(self, socket, name):
        super().__init__(socket, name, Headers.Request_join.value)


class JoinResponse(Response):
    def __init__(self, socket, respond):
        super().__init__(socket, respond, Headers.Response_join.value)


class LeaveRequest(Request):
    def __init__(self, socket, name):
        super().__init__(socket, name, Headers.Request_leave.value)


class LeaveResponse(Response):
    def __init__(self, socket, name):
        super().__init__(socket, name, Headers.Response_leave.value)


class ChangeShapeRequest(Request):
    def __init__(self, socket, name):
        super().__init__(socket, name, Headers.Request_change_shapes.value)


class ChangeShapeResponse(Response):
    def __init__(self, socket, name):
        super().__init__(socket, name, Headers.Response_change_shapes.value)


class ChangeFieldSizeRequest(Request):
    def __init__(self, socket, new_size):
        super().__init__(socket, new_size, Headers.Request_change_size.value)


class ChangeFieldSizeResponse(Response):
    def __init__(self, socket, new_size):
        super().__init__(socket, new_size, Headers.Response_change_size.value)


class Unpacker:
    @staticmethod
    def _receive_fixed_length_msg(sock, msg_len):
        message = b''
        while len(message) < msg_len:
            try:
                chunk = sock.recv(msg_len - len(message))  # read few bytes
                if chunk == b'':
                    raise RuntimeError("socket connection broken")
                message = message + chunk
            except ConnectionResetError:  # someone has disconnected
                break
        return message

    @staticmethod
    def unpack(sock):
        header = Unpacker._receive_fixed_length_msg(sock, variables.HEADER_LENGTH)
        if len(header) == 0:  # player has disconnected
            return None
        message_data = struct.unpack(variables.HEADER_DATA, header)  # length of the message
        message_length = message_data[1]
        message_type = message_data[0]
        message = None
        if message_length > 0:  # if everything is OK
            message = Unpacker._receive_fixed_length_msg(sock, message_length)  # read message
            message = message.decode("utf-8")
        return [message_type, message]
