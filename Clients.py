import socket
import ast
import threading


SIZE = 10

Name = input("Enter a name to be visible: ")


# class Recv():
#     def __init__(self, clnt, clientListR):
#         self.clientListR = clientListR
#         self.newMsg1 = True
#         self.incoming = ""
#         self.newdata = ""
#         self.datatype = ""
#
#         while True:
#             self.data = clnt.recv(SIZE + 4)
#
#             if self.newMsg1:
#                 print("In if newMsg....")
#                 print("unpo: ", self.data[:SIZE])
#                 self.msglen = int(self.data.decode("utf-8")[:SIZE])
#                 print("unpo N/r :", self.data[SIZE: SIZE + 1])
#                 self.datatype = str(self.data.decode("utf-8")[SIZE: SIZE + 1])
#                 self.newMsg1 = False
#
#             if self.datatype == "n":
#                 self.newdata += self.data.decode("utf-8")
#                 print("newdata: ", self.newdata)
#                 print("fjds: ", len(self.newdata) - (SIZE + 1))
#
#                 if len(self.newdata) - (SIZE + 1) == self.msglen:
#                     print("msglen: ", self.msglen)
#                     print("NEw.... ", self.newdata[SIZE + 1:])
#                     print("json: ", ast.literal_eval(self.newdata[SIZE + 1:]))
#                     self.clientListR = ast.literal_eval(self.newdata[SIZE + 1:])
#                     self.newMsg1 = True
#                     self.newdata = ""
#                     self.datatype = ""
#
#             elif self.datatype == "r":
#                 print("else....")
#                 self.incoming += self.data.decode("utf-8")
#                 print("incoming: ", self.incoming)
#
#                 if len(self.incoming) - (SIZE + 1) == self.msglen:
#                     print("msglen: ", self.msglen)
#                     print("Server: ", self.incoming[SIZE + 1:])
#                     self.newMsg1 = True
#                     self.incoming = ""
#                     self.datatype = ""

###############################################################################################################

class Network:
    def __init__(self):
        self.newMsg = True
        self.incoming = ""
        self.datatype = ""
        self.newdata = ""
        self.clientsList = {}
        self.sender = ""
        self.knowSender = True
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.join()

    def join(self):
        self.client.connect(('192.168.1.5', 9229))
        print("Connected")
        print(self.client.recv(100).decode("utf-8"))
        self.client.sendall(Name.encode("utf-8"))
        self.strThread()

    def recv(self):
        while True:
            self.data = self.client.recv(SIZE + 7)
            if self.newMsg:
                print("unpo N/r :", self.data[SIZE: SIZE + 1])
                self.datatype = str(self.data.decode("utf-8")[SIZE: SIZE + 1])
                print("datatype>>> ", self.datatype)
                self.msglen = int(self.data.decode("utf-8")[:SIZE])

                self.newMsg = False

            if self.datatype == "n":
                self.newdata += self.data.decode("utf-8")
                self.sliceValue = int(self.newdata.find("n")) + 1
                print("msglen: ", self.msglen)

                if len(self.newdata[self.sliceValue:]) == int(self.msglen):
                    print("Final: ", ast.literal_eval(self.newdata[SIZE + 1:]))
                    self.clientsList = ast.literal_eval(self.newdata[SIZE + 1:])
                    print("list: ", self.clientsList)
                    self.newMsg = True
                    self.newdata = ""
                    self.datatype = ""

            elif self.datatype == "r":
                print("else....")
                self.fndindex = self.data.decode("utf-8").find("r")
                self.incoming += self.data.decode("utf-8")
                print("Whole: ", self.data.decode("utf-8"))
                if self.knowSender:
                    self.sender = int(str(self.data.decode("utf-8"))[self.fndindex+1: self.fndindex +2])
                    self.knowSender = False
                print("sender>>> ", self.sender)
                print("incoming: ", self.incoming)

                if len(self.incoming[int(self.incoming.index("r"))+2:]) == self.msglen:
                    print(self.clientsList[self.sender], ": ", self.incoming[SIZE + 2:])
                    self.sender = ""
                    self.newMsg = True
                    self.incoming = ""
                    self.datatype = ""
                    self.knowSender = True

    def send(self):
        while True:
            self.user_text = input("Enter your text: ")
            msg = str(f"{self.user_text[:1]}{len(self.user_text) - 1:<{SIZE}}" + "r" + self.user_text[1:])
            if self.user_text is None or self.user_text == "":
                pass
            else:
                print(msg)
                self.client.send(msg.encode("utf-8"))

    def strThread(self):
        threading.Thread(target = self.recv).start()
        threading.Thread(target=self.send).start()


if __name__ == "__main__":
    Network()
