import Common.variables as variables
import Communication.mailman as mailman
import Common.functions as functions
from Common.variables import ResponseCode, Headers
import socket
import threading


class Server:
    def __init__(self):
        self.clients = {}  # key = socks, value = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
        server_address = (variables.SERVER_NAME, variables.PORT_NUMBER)  # # Bind the socket to the port
        print('starting up on {} port {}'.format(*server_address))
        self.sock.bind(server_address)
        self.sock.listen(1)

    def start_listening(self):
        while True:
            try:
                # wait for a new connection
                client_sock, client_addr = self.sock.accept()
                thread = threading.Thread(target=self._client_thread, args=(client_sock,))
                thread.daemon = True
                thread.start()

            except KeyboardInterrupt:
                break

    def _client_thread(self, client_sock):
        while True:
            msg_received = mailman.Unpacker.unpack(client_sock)
            if msg_received is None or not msg_received[1]:
                break
            self._process_message(client_sock, msg_received)
        print("Removed player " + self.clients[client_sock])
        self.clients = functions.remove_key(self.clients, client_sock)
        client_sock.close()

    def _process_message(self, client_sock, msg_rec):
        if functions.is_string(msg_rec[1]):
            header_type = int(msg_rec[0])
            if header_type == Headers.Request_join.value:
                self._process_join(client_sock, str(msg_rec[1]))
            elif header_type == Headers.Request_click.value:
                self._process_click(client_sock, msg_rec[1])
            elif header_type == Headers.Request_leave.value:
                self._process_leave(client_sock, msg_rec[1])
            elif header_type == Headers.Request_change_size.value:
                self._process_change_size(client_sock, msg_rec[1])
            else:
                print("I don't know this header: " + msg_rec)

    def _process_change_size(self, client_sock, msg_rec):
        if functions.is_string(msg_rec) and functions.is_number(int(msg_rec)):
            print("Trying to change field size")
            other_sock = self._get_other_sock(client_sock)
            if int(msg_rec) == ResponseCode.Ok.value:
                mailman.ChangeFieldSizeResponse(other_sock, str(ResponseCode.Ok.value)).send()
                mailman.ChangeFieldSizeResponse(client_sock, str(ResponseCode.Ok.value)).send()
            elif int(msg_rec) == ResponseCode.Not_Ok.value:
                mailman.ChangeFieldSizeResponse(other_sock, str(ResponseCode.Not_Ok.value)).send()
            else:
                mailman.ChangeFieldSizeResponse(other_sock, msg_rec).send()

    def _process_leave(self, client_sock, msg_rec):
        if functions.is_string(msg_rec):
            print(self.clients[client_sock], "is leaving")
            other_sock = self._get_other_sock(client_sock)
            mailman.LeaveResponse(other_sock, msg_rec).send()

    def _process_join(self, sock, msg):
        if functions.is_string(msg):
            print("Processing join...")
            if len(self.clients) < 2:  # only for two players
                print("Accepted player " + msg)
                self.clients[sock] = msg  # add player
                mailman.JoinResponse(sock, ResponseCode.Ok.value).send()
                if len(self.clients) == 2:  # initialize players
                    print("All players are ready to play")
                    players = list(self.clients.keys())
                    print(self.clients[players[1]], "start to play")
                    mailman.JoinResponse(players[0], str("True\\" + self.clients[players[1]])).send()  # first one start
                    mailman.JoinResponse(players[1], str("False\\" + self.clients[players[0]])).send()  # second wait
            else:
                print("Declined player " + msg)
                mailman.JoinResponse(sock, ResponseCode.Not_Ok.value).send()

    def _get_other_sock(self, sock):
        player_socks = list(self.clients.keys())
        if player_socks[0] == sock:
            return player_socks[1]
        return player_socks[0]

    def _process_click(self, sock, msg):
        if functions.is_number(int(msg)):
            print("player", self.clients[sock], "clicked cell with id", msg)
            mailman.ClickResponse(self._get_other_sock(sock), msg).send()


if __name__ == "__main__":
    server = Server()
    server.start_listening()
    server.sock.close()


