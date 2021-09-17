import socket
import ast
import threading


SIZE = 10

Name = input("Enter a name to be visible: ")
###############################################################################################################

class Network:
    def __init__(self):
        self.newMsg = True
        self.incoming = ""
        self.datatype = ""
        self.newdata = ""
        self.sendId = True
        self.begin_sending = False
        self.clientsList = {}
        self.sender = ""
        self.knowSender = True
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.join()

    def join(self):
        try:
            self.client.connect(('0.0.0.0', 8989))
            print("Connected")
            print(self.client.recv(100).decode("utf-8"))
            self.client.sendall(Name.encode("utf-8"))
            self.strThread()
        except:
            print("\n\n.....Disconnected from Server :(")

    def recv(self):
        while True:
            self.data = self.client.recv(SIZE + 7)
            if self.newMsg:
                self.datatype = str(self.data.decode("utf-8")[SIZE: SIZE + 1])
                self.msglen = int(self.data.decode("utf-8")[:SIZE])

                self.newMsg = False

            if self.datatype == "n":
                self.newdata += self.data.decode("utf-8")
                self.sliceValue = int(self.newdata.find("n")) + 1

                if len(self.newdata[self.sliceValue:]) == int(self.msglen):
                    self.clientsList = ast.literal_eval(self.newdata[SIZE + 1:])
                    print(self.clientsList)
                    self.newMsg = True
                    self.newdata = ""
                    self.datatype = ""

            elif self.datatype == "r":
                self.fndindex = self.data.decode("utf-8").find("r")
                self.incoming += self.data.decode("utf-8")
                if self.knowSender:
                    self.sender = int(str(self.data.decode("utf-8"))[self.fndindex+1: self.fndindex +2])
                    self.knowSender = False

                if len(self.incoming[int(self.incoming.index("r"))+2:]) == self.msglen:
                    print(self.clientsList[self.sender], ": ", self.incoming[SIZE + 2:])
                    self.sender = ""
                    self.newMsg = True
                    self.incoming = ""
                    self.datatype = ""
                    self.knowSender = True

    def send(self):
        while True:
            self.user_text = input("")
            if self.user_text:
                if self.user_text[:1].isnumeric():
                    self.clientsList_keys = list(self.clientsList.keys())
                    self.clientsList_values = list(self.clientsList.values())
                    msg = str(f"{self.user_text[:1]}{len(self.user_text) - 1:<{SIZE}}" + "r" + str(self.clientsList_keys[int(self.clientsList_values.index(Name))]) + self.user_text[1:])
                    self.client.send(msg.encode("utf-8"))
                    msg = ""

                elif self.user_text[:1] == "g":
                    self.clientsList_keys = list(self.clientsList.keys())
                    self.clientsList_values = list(self.clientsList.values())
                    msg1 = str(f"{str('~')}{len(self.user_text) - 1:<{SIZE}}" + "g" + str(self.clientsList_keys[int(self.clientsList_values.index(Name))]) + self.user_text[1:])
                    self.client.send(msg1.encode("utf-8"))
                    msg1 = ""
    def strThread(self):
        threading.Thread(target = self.recv).start()
        threading.Thread(target=self.send).start()


if __name__ == "__main__":
    Network()
