import Common.variables as variables
import Communication.mailman as mailman
from Common.variables import Headers, ResponseCode
import player
import Graphics.messenger as messenger
import Common.functions as functions
import threading
import clickManager
import socket
import math


class Client:
    def __init__(self, player):
        self.player = player
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
        # Connect the socket to the port where the server is listening
        server_address = (variables.SERVER_NAME, variables.PORT_NUMBER)
        print('connecting to {} port {}'.format(*server_address))
        try:
            self.sock.connect(server_address)
        except ConnectionRefusedError:
            messenger.SendToUser.error("Server is not online")
            self.player.back_to_menu()
        self._start_thread()
        self.new_field_size = variables.DEFAULT_FIELD_SIZE
        mailman.JoinRequest(self.sock, player.name).send_request()

    def _start_thread(self):
        thread = threading.Thread(target=self._message_receiver)
        thread.daemon = True
        thread.start()

    def _message_receiver(self):
        while True:
            msg_received = mailman.Unpacker.unpack(self.sock)
            if len(msg_received[1]) > 0:  # if message exists
                self._process_message(msg_received)

    def _process_message(self, msg):
        msg_type = int(msg[0])
        content = str(msg[1])
        if msg_type == Headers.Response_join.value:
            self._process_join(content)
        elif msg_type == Headers.Response_click.value:
            self._process_click(content)
        if msg_type == Headers.Response_leave.value:
            self._process_leave()
        if msg_type == Headers.Response_change_size.value:
            self._process_change_field(content)

    def send_clicked_cell(self, cell_id):
        if functions.is_number(cell_id):
            print("I clicked cell number", cell_id)
            mailman.ClickRequest(self.sock, str(cell_id)).send()

    def _process_click(self, msg):
        if functions.is_number(int(msg)):
            print("My opponent clicked cell with id", msg)
            cell_id = int(msg)
            self.player.opponent.click(cell_id)

    def send_leave_request(self):
        print("I am leaving")
        mailman.LeaveRequest(self.sock, self.player.name).send()

    def _process_leave(self):
        messenger.SendToUser.go_back("Notification from server", self.player.opponent.name + " has left the game!")
        self.player.back_to_menu()

    def _process_change_field(self, num):
        if functions.is_string(num) and functions.is_number(int(num)):
            opponent_name = self.player.opponent.name
            if int(num) == ResponseCode.Ok.value:  # opponent accept
                print("changed field size")
                self.player.board.gui.set_field_size(self.new_field_size)
                num = self.player.board.gui.playing_field.restart()
                self.player.board.playing_field.initialize_field(num)
            elif int(num) == ResponseCode.Not_Ok.value:  # opponent is not cool with a field change
                print("didn't change size")
                true_size = int(math.sqrt(self.player.board.playing_field.get_number_of_cells()))
                self.player.board.gui.set_field_size(true_size)
                messenger.SendToUser.show_info("Message", opponent_name +
                                        " declined your request for changing field size to " + str(self.new_field_size))
            elif 3 <= int(num) <= 5:  # field size can only be from 3 to 5
                agree = messenger.SendToUser.ask_for_field_change(
                        opponent_name + " want to change field size to " + str(num) + ".\nDo you agree?")
                if agree:
                    print("I agree to change size")
                    mailman.ChangeFieldSizeRequest(self.sock, ResponseCode.Ok.value).send()
                    self.new_field_size = int(num)
                else:
                    print("I disagree to change size")
                    mailman.ChangeFieldSizeRequest(self.sock, ResponseCode.Not_Ok.value).send()

    def send_change_field_request(self):
        num = self.player.board.gui.get_field_size()
        if functions.is_number(num):
            print("I want to change field size to " + str(num))
            self.new_field_size = num
            mailman.ChangeFieldSizeRequest(self.sock, str(num)).send()

    def _process_join(self, msg_txt):
        if functions.is_string(msg_txt):
            if msg_txt == str(ResponseCode.Ok.value):  # can play
                print("I,", self.player.name, ", have joined the game.")
            elif msg_txt == str(ResponseCode.Not_Ok.value):  # game is full
                messenger.SendToUser.error("There is already two players in the game!")
                exit(0)
            else:  # initialize who will start
                data = msg_txt.split("\\")
                start = False
                if data[0] == "True":
                    start = True
                self._configure_game(start, data[1])

    def _configure_game(self, start, name):
        # It doesn't matter what we set, because initialize function will set the right way
        opponent = player.MultiPlayerOpponent(name, "Circle", self.player.board, start)
        self.player.initialize(start, opponent)
        cm = clickManager.ClickManager(self.player.board, self.player, opponent)
        opponent.add_click_manager(cm)
