import socket
import threading
import pickle
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
        self.beginRecv = False
        #
        self.newMsg = True
        self.toSend = ""
        self.msgtype = ""
        self.incomingMsg = ""
        self.nameInc = 0
        try:
            self.sock.bind(('192.168.1.5',9229))
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
                print("Name: ", self.name)
                self.conn_dict[self.conn] = self.nameInc
                self.name_dict[self.nameInc]  = self.name
                print("keys: ", self.conn_dict.keys())

                ######################################################
                self.updateUser = str(self.name_dict)
                self.sendingNewClient(self.updateUser, self.conn_dict.keys())

                self.nameInc += 1

            if self.addr not in self.addr_list:
                self.addr_list.append(self.addr)
                print("Connected to: ", self.conn_dict.items())

            # self.sending(self.conn_dict.keys())
            threading.Thread(target=self.recv).start()


    def sendingNewClient(self, user, clients):
        print("self.updateUser: ", user)

        for i in clients:
            print("user len: ", len(user))
            print(str(f"{len(user):<{SIZE}}" + "n" + user))
            i.send(str(f"{len(user):<{SIZE}}" + "n"+user).encode("utf-8"))

    def recv(self):
        while True:
            if self.knowSender:
                print("Know is true....")
                if self.onceRecv:
                    print("Once recv is true.....")
                    print("Conn....", self.conn)
                    self.onceData = self.conn.recv(SIZE+2)
                    print("onceData: ", self.onceData)
                    self.onceRecv = False
                    print("Value of OnceREcv: ", self.onceRecv)
                print("OnceData: ", self.onceData)
                print("Value of OnceREcv After if state: ", self.onceRecv)
                self.senderConnNo = self.onceData.decode("utf-8")[SIZE:]
                print("SenderNo: ", self.senderConnNo)
                self.key_list1 = list(self.conn_dict.keys())
                self.value_list1 = list(self.conn_dict.values())
                self.senderConn = self.key_list1[self.value_list1.index(int(self.senderConnNo))]
                print("SenderConn:....", self.senderConn)
                self.onceData = ""
                self.knowSender = False
                self.beginRecv = True





            if self.beginRecv:
                print("begin recv is true.....")
                self.data = self.senderConn.recv(SIZE + 7)
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
                    if len(self.incomingMsg[int(self.incomingMsg.index("r")) + 1:])  == self.msglen:
                        print(f"Sender: {self.name_dict[self.conn_dict[self.senderConn]]} ........ {self.incomingMsg[SIZE+2:]}")
                        #################################
                        self.key_list = list(self.conn_dict.keys())
                        self.value_list = list(self.conn_dict.values())
                        #################################
                        self.toSend = self.key_list[self.value_list.index(int(self.incomingMsg[:1]))]
                        print("Sending To:....", self.toSend)
                        self.sending(self.toSend, self.incomingMsg[SIZE+2:], self.senderConnNo)
                        print("above connNo: ", self.senderConnNo)
                        self.senderConn = ""
                        self.incomingMsg = ""
                        self.data = ""
                        self.msgtype = ""
                        self.toSend = ""
                        self.beginRecv = False
                        self.knowSender = True
                        self.onceRecv = True
                        print("near end....")
                        self.newMsg = True

                if self.msgtype == "g":
                    self.incomingMsg += self.data.decode("utf-8")
                    print("incoming...: ", self.incomingMsg)
                    print("len...group...: ", self.msglen)
                    ############################################################
                    if len(self.incomingMsg[int(self.incomingMsg.index("g")) + 1:])  == self.msglen:
                        print(f"Sender...grp: {self.name_dict[self.conn_dict[self.senderConn]]} ........ {self.incomingMsg[SIZE+2:]}")
                        #################################
                        #################################

                        self.sendingGrp(self.incomingMsg[SIZE+2:], self.senderConnNo)
                        print("above connNo: ", self.senderConnNo)
                        self.senderConn = ""
                        self.incomingMsg = ""
                        self.data = ""
                        self.msgtype = ""
                        self.toSend = ""
                        self.beginRecv = False
                        self.knowSender = True
                        self.onceRecv = True
                        print("Near end grp.....")
                        self.newMsg = True
                    ############################################################

    def sending(self, sendingTo, dataToSend, Sender):
        print("Sender: ", Sender)
        print("Datatosend: ", dataToSend)
        print("Sending this: ", str(f"{len(dataToSend):<{SIZE}}r{str(Sender)}{dataToSend}"))
        sendingTo.send(str(f"{len(dataToSend):<{SIZE}}r{str(Sender)}{dataToSend}").encode("utf-8"))

    def sendingGrp(self, sendingData, sender):
        print("Sendergrp....: ", sender)
        print("Datatosendgrp....: ", sendingData)
        for i in self.conn_dict.keys():
            if self.conn_dict[i] != int(sender):
                i.send(str(f"{len(sendingData):<{SIZE}}r{str(sender)}{sendingData}").encode("utf-8"))
            else:
                print("In else")




if __name__ == "__main__":
    Network()
