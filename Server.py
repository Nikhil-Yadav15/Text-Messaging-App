import socket
import threading
SIZE = 10

# r: simple send message
# n: new client msg send
# s: single interaction
# g: grp interaction
# i: identity

class Network:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn_dict = {}
        self.addr_list = []
        self.name_dict = {}
        #
        self.onceRecv = True
        self.knowSender = True
        self.senderConnNo = ""
        self.senderConn = ""
        self.beginRecv = True
        #
        self.newMsg = True
        self.toSend = ""
        self.msgtype = ""
        self.incomingMsg = ""
        self.nameInc = 0
        try:
            self.sock.bind(('', 2))
            print("Ready...")
            self.sock.listen(5)
            self.acceptance()
        except socket.error as e:
            print(e)
            print("Disconnected....")
    def acceptance(self):
        while 1:
            self.conn, self.addr = self.sock.accept()
            self.conn.send(str("Welcome! {0}".format(self.addr)).encode("utf-8"))

            if self.conn not in self.conn_dict.keys():
                self.name = self.conn.recv(100).decode("utf-8")
                self.conn_dict[self.conn] = self.nameInc
                self.name_dict[self.nameInc]  = self.name

                ######################################################
                self.updateUser = str(self.name_dict)
                self.sendingNewClient(self.updateUser, self.conn_dict.keys())

                self.nameInc += 1

            if self.addr not in self.addr_list:
                self.addr_list.append(self.addr)
                print("Connected to: ", self.conn_dict.items())

            # self.sending(self.conn_dict.keys())
            threading.Thread(target=self.recv).start()
            # self.recv()

    def sendingNewClient(self, user, clients):
        print("self.updateUser: ", user)

        for i in clients:
            print("user len: ", len(user))
            print(str(f"{len(user):<{SIZE}}" + "n" + user))
            i.send(str(f"{len(user):<{SIZE}}" + "n"+user).encode("utf-8"))
        # self.knowSender = True

    def recv(self):
        while True:
            self.data = self.conn.recv(SIZE + 7)
            if not self.data:
                pass
            if self.data:
                print("begin recv is true.....")
                print("data: ", self.data)
                if self.knowSender:
                    self.senderConnNo = int(self.data.decode("utf-8")[SIZE+2:SIZE+3])
                    print("SenderNO: ", self.senderConnNo)
                    #######################################
                    self.key_list1 = list(self.conn_dict.keys())
                    self.value_list1 = list(self.conn_dict.values())
                    #######################################
                    self.senderConn = self.key_list1[int(self.value_list1.index(self.senderConnNo))]
                    self.knowSender = False
                    print("sender conn above>....: " , self.senderConn)
                print("Name: ", self.name_dict[int(self.conn_dict[self.senderConn])])
                if self.newMsg:
                    print("length...: ", self.data[1:SIZE])
                    self.msglen = int(self.data.decode("utf-8")[1:SIZE])
                    print("Name1: ", self.name_dict[int(self.conn_dict[self.senderConn])])
                    self.msgtype = str(self.data.decode("utf-8")[SIZE+1:SIZE+2])
                    self.newMsg = False

                if self.msgtype == "r":
                    self.incomingMsg += self.data.decode("utf-8")
                    print("incoming...: ", self.incomingMsg)
                    print("len...: ", self.msglen)
                    print("Index length: ", self.incomingMsg[int(self.incomingMsg.index("r")) + 2:])
                    self.conn = self.senderConn
                    if len(self.incomingMsg[int(self.incomingMsg.index("r")) + 2:])  == self.msglen:
                        print(f"Sender: {self.name_dict[self.conn_dict[self.senderConn]]} ........ {self.incomingMsg[SIZE+3:]}")
                        #################################
                        self.key_list = list(self.conn_dict.keys())
                        self.value_list = list(self.conn_dict.values())
                        #################################
                        self.toSend = self.key_list[self.value_list.index(int(self.incomingMsg[:1]))]
                        print("Sending To:....", self.toSend)
                        self.sending(self.toSend, self.incomingMsg[SIZE+3:], self.senderConnNo)
                        print("above connNo: ", self.senderConnNo)
                        self.senderConn = ""
                        self.senderConnNo = ""
                        self.incomingMsg = ""
                        self.data = ""
                        self.msgtype = ""
                        self.toSend = ""
                        self.knowSender = True
                        # self.onceRecv = True
                        print("near end....")
                        self.newMsg = True

                elif self.msgtype == "g":
                    self.incomingMsg += self.data.decode("utf-8")
                    print("incoming...: ", self.incomingMsg)
                    print("len...: ", self.msglen)
                    print("Index length: ", self.incomingMsg[int(self.incomingMsg.index("g")) + 1:])
                    self.conn = self.senderConn
                    if len(self.incomingMsg[int(self.incomingMsg.index("g")) + 2:]) == self.msglen:
                        print(f"Sender: {self.name_dict[self.conn_dict[self.senderConn]]} ........ {self.incomingMsg[SIZE + 3:]}")
                        self.groupSending(self.incomingMsg[SIZE+3:], self.senderConnNo)

                        self.senderConn = ""
                        self.senderConnNo = ""
                        self.incomingMsg = ""
                        self.data = ""
                        self.msgtype = ""
                        self.knowSender = True
                        print("near end grp....")
                        self.newMsg = True

                elif self.msgtype == "l":
                    print("reached...........")
                    self.incomingMsg += self.data.decode("utf-8")
                    self.conn = self.senderConn
                    print("Came: ", self.incomingMsg[SIZE + 3:])
                    self.send_Left(str(self.senderConnNo))
                    self.name_dict.pop(self.senderConnNo)
                    self.conn_dict.pop(self.senderConn)
                    self.senderConn = ""
                    self.senderConnNo = ""
                    self.incomingMsg = ""
                    self.data = ""
                    self.msgtype = ""
                    self.knowSender = True
                    print("near end leave....")
                    self.newMsg = True

                ##################################

    def sending(self, sendingTo, dataToSend, Sender):
        print("Sender: ", Sender)
        print("Datatosend: ", dataToSend)
        print("Sending this: ", str(f"{len(dataToSend):<{SIZE}}r{str(Sender)}{dataToSend}"))
        sendingTo.send(str(f"{len(dataToSend):<{SIZE}}r{str(Sender)}{dataToSend}").encode("utf-8"))

    def send_Left(self, leaving):
        for i in self.conn_dict.keys():
            if self.conn_dict[i] != int(leaving):
                i.send(str(f"{leaving:<{SIZE}}l").encode("utf-8"))

    def groupSending(self, DataToSend, sender):
        print("Sender Grp: ", sender)
        print("Datatosend Grp: ", DataToSend)
        for i in self.conn_dict.keys():
            if self.conn_dict[i] != sender:
                i.send(str(f"{len(DataToSend):<{SIZE}}g{str(sender)}{DataToSend}").encode("utf-8"))



if __name__ == "__main__":
    Network()
