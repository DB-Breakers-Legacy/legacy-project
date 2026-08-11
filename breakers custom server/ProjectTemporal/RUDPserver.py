import base64
import os
import hashlib
import hmac
import http.client

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

IV_KEY = bytes.fromhex("185af50497054644bf89f96ff2f798b2")

AES_KEY = bytes.fromhex("3710c0f30922423a8fd8befcc1f83b3d")

HASH_KEY = bytes.fromhex("61a174c3f20a4b75bb4d2f17e183f25e")

SID_KEY = bytes.fromhex("c2498a5532f947808e8684812b022b95")

def nullPadding(data, block_size):
    padLength = block_size - (len(data) % block_size)
    return data + b'\x00' * padLength

def encryptData(data, isnull=False):
    print("Encrypting Data...")
    print(data.encode())
    print(data.encode().hex())
    if isnull == True:
        paddedData = data.encode()
    else:
        paddedData = nullPadding(data.encode(), AES.block_size)
        print("Padded Data...")
        print(paddedData)
        
    iv = get_random_bytes(16)
    #use cipher obj stored in user dict later
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    cipherText = cipher.encrypt(paddedData)
    
    
    #hash + iv + ciphertext
    hashGen = iv + cipherText
    
    macHash = hmac.new(HASH_KEY, hashGen, hashlib.sha256).digest()
    
    encryptedData = macHash + iv + cipherText
    
    return encryptedData
    
def decryptData(data):
    print("Decrypting Data...")
    iv = data[32:48] #32 hex char
    #print(f"Payload assumed IV is {iv.hex()}")
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    decryptedData = cipher.decrypt(data)
    

    incomingHash = data[:32] #64 hex char
    #print(f"Payload assumed Hash is {incomingHash.hex()}")
    cipherText = data[48:] #96+ hex char
    #print(f"Ciphertext is {cipherText.hex()}")
    
    hashGen = iv + cipherText
    
    macHash = hmac.new(HASH_KEY, hashGen, hashlib.sha256).digest()
    
    if hmac.compare_digest(macHash, incomingHash):
        print("Valid hash")
    else:
        print("Mismatched hash")
        #debug, probably return error in real environment
    
    return decryptedData

def getPublicIp():
    host = "ipv4.icanhazip.com"
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", "/")
    response = conn.getresponse()
    text = response.read()
    return text

class UnexpectedPacketType(Exception):
    pass

class RUDPConnect(DatagramProtocol):
    def __init__(self):
        self.sequenceCounter = 0  #TODO: make these work with multiple connections, dictionary keyed with addr
        #move ALL of these to a dict
        self.dnsCounter = 0
        self.connectionActive = False
        self.awaitingConnectionACK = False
        self.connectionEstablished = False
        self.dnsComplete = False

    # Main entrypoint method for the class
    def datagramReceived(self, data, addr):
        print(f"Received data from {addr}") #repr(data).hex()
        packetHeader = data[3] #write documentation
        print(f"Connection Type == {packetHeader}\n")

        if self.isInitConnectRequest(data):
            self.onInitConnectRequest(data, addr)

        elif self.isHeartbeat(data):
            self.onHeartbeat(data, addr)

        elif self.isInitConnectData(data):
            self.onInitConnectData(data, addr)

        elif self.isInitConnectDataContinued(data):
            self.onInitConnectDataContinued(data, addr)

        elif self.isDnsStuff(data):
            self.onDnsStuff(data, addr)

        else:
            # TODO QUESTION: should we raise here? We didn't pre-refactor, we
            # just silently exited. I'm not raising for pre-factor
            # compatibility, but there's an argument for raising.
            #
            # raise UnexpectedPacketType

            # TODO: replace with logger?
            print("could not recognize packet type")
            # TODO: probably want to log the bad packet too somehow

    # Methods to recognize packet types 
    def isInitConnectRequest(self, data):
        return len(data) == 20 and self.connectionActive == False

    def isHeartbeat(self, data):
        return len(data) == 82

    def isInitConnectData(self, data):
        return len(data) == 130

    def isInitConnectDataContinued(self, data):
        return len(data) == 20 and self.awaitingConnectionACK == True

    def isDnsStuff(self, data):
        return len(data) == 26

    # Methods to respond to specific packet types 
    def onInitConnectRequest(self, data, addr):
        print("Getting initial connection request...")
        ivKey = data[4:20] #IV key, store in dict
        print(f"IV key == {ivKey}")
        print("Sending ACK...\n")
        response = b'\x00\x00\x00\x04'
        self.connectionActive = True
        self.transport.write(response, addr) 

    def onHeartbeat(self, data, addr):
        print("Getting heartbeat...")
        self.sequenceCounter += 1
        cCount = self.sequenceCounter
        ackHeader = b'\x00\x00\x04'
        response = cCount.to_bytes(1, 'big') + ackHeader #TODO: check if sequence header actually is just one byte, probably not.
        print("Sending ACK with sequence...")
        print(response)
        self.transport.write(response, addr) 
        #initial connection data continued
        if self.connectionEstablished == False: #TODO: terrible race condition, maybe better if in a addr dict?
            print("Sending Connection ACK...")
            response = b'\x00\x00\x00\x04'
            self.transport.write(response, addr) 
            #send server connection data
            #TODO: make this less awful
            initDataHeader = bytes.fromhex("00000003febedeef000000440001010000001b")
            responseAddr = self.bamco_truncated_public_ip
            responsePort = addr[1]
            self.clientPort = addr[1]
            responseData = responseAddr + str(responsePort)
            print(f"Response == {responseData}")
            response = initDataHeader + encryptData(responseData)
            print("Sending connection data 1...")
            self.transport.write(response, addr) 
            self.connectionEstablished = True
            self.awaitingConnectionACK = True
            
        if self.sequenceCounter == 3: #TODO: also probably not good
            initDataHeader = bytes.fromhex("03000003febedeef01000054012fff0000002d")
            responseData = '127.0.0.1:7100' #bc.googleusercontent.com:7100
            response = initDataHeader + encryptData(responseData)
            print("Sending connection data 4...")
            self.transport.write(response, addr)
                
        if self.sequenceCounter == 4:
            initDataHeader = bytes.fromhex("04000003febedeef0100003401310100000001")
            responseData = '' #NULL
            response = initDataHeader + encryptData(responseData, True)
            print("Sending final connection data...")
            self.transport.write(response, addr)
                
                
        if self.sequenceCounter > 4: #start sending heartbeats back after 5
            print("Sending server heartbeat request back...")
            initDataHeader = bytes.fromhex("000003febedeef000000440001010000001b")
            responseHeader = cCount.to_bytes(1, 'big') + initDataHeader
            responseAddr = self.bamco_truncated_public_ip
            responsePort = addr[1]
            responseData = responseAddr + str(responsePort)
            response = responseHeader + encryptData(responseData)
            self.transport.write(response, addr)
            #check for response?
    
    def onInitConnectData(self, data, addr):
        print("Getting connection data...")
    
    def onInitConnectDataContinued(self, data, addr):
        self.awaitingConnectionACK = False
        print("Continuing connection data...")
        initDataHeader = bytes.fromhex("01000003febedeef01000054012fff0000002f")
        responseData = '6.127.0.0.1:7099' #6.bc.googleusercontent.com:7099
        response = initDataHeader + encryptData(responseData)
        print("Sending connection data 2...")
        self.transport.write(response, addr)
        
        initDataHeader = bytes.fromhex("02000003febedeef01000054012fff0000002d")
        responseData = '127.0.0.1:7099' #bc.googleusercontent.com:7099
        response = initDataHeader + encryptData(responseData)
        print("Sending connection data 3...")
        self.transport.write(response, addr)
    
    def onDnsStuff(self, data, addr):
        self.dnsCounter += 1
        print("Sending DNS stuff...")
        initDataHeader = bytes.fromhex("0f0f0c0c00000001002b") #2b can be 2c, investigate
        responseData = '144.85.112.136.bc.googleusercontent.com:7100'
        response = initDataHeader + encryptData(responseData)
        self.transport.write(response, addr)
        #TODO check if need to wait
        if self.dnsCounter == 5:
            initDataHeader = bytes.fromhex("00000c0c00000001002b")
            response = initDataHeader + encryptData(responseData)
            for x in range(5):
                self.transport.write(response, addr)
                if x == 4:
                    self.dnsComplete = True

    @property
    def public_ip(self):
        if not hasattr(self, '_public_ip'):
            ip = getPublicIp()
            self._public_ip = ip.decode('utf8')
        return self._public_ip

    @property
    def truncated_public_ip(self):
        bits = self.public_ip.split('.')
        return '.'.join(bits[:2])

    @property
    def bamco_truncated_public_ip(self):
        return self.truncated_public_ip + ':'

if __name__ == '__main__':
    listen_port = int(os.environ.get("RUDP_SERVER_PORT", 7100))
    reactor.listenUDP(listen_port, RUDPConnect())
    print(f"RUDP server started on port {listen_port}")
    reactor.run()
