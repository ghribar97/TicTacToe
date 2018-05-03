from Communication.server import Server

if __name__ == "__main__":
    serv = Server()
    serv.start_listening()
    serv.sock.close()
