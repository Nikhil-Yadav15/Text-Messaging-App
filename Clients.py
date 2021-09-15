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
            self.client.connect(('192.168.1.5', 9229))
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
                if self.sendId:
                    ############################
                    self.listValue = list(self.clientsList.values())
                    self.listKeys = list(self.clientsList.keys())
                    self.client.send(str(f"{str('r'):<{SIZE}}{self.listKeys[int(self.listValue.index(Name))]}").encode("utf-8"))
                    self.sendId = False
                    self.begin_sending = True
                    #############################
                if self.begin_sending:
                    if self.user_text[:1].isnumeric():
                        msg = str(f"{self.user_text[:1]}{len(self.user_text) - 1:<{SIZE}}" + "r" + self.user_text[1:])
                        self.client.send(msg.encode("utf-8"))
                        print("sending id")
                        self.sendId = True
                        self.begin_sending = False
                        msg = ""
                    elif self.user_text[:1] == "g":
                        msg = str(f"~{len(self.user_text) - 1:<{SIZE}}" + "g" + self.user_text[1:])
                        self.client.send(msg.encode("utf-8"))
                        print("sending id")
                        self.sendId = True
                        self.begin_sending = False
                        msg = ""


    def strThread(self):
        threading.Thread(target = self.recv).start()
        threading.Thread(target=self.send).start()


if __name__ == "__main__":
    Network()
