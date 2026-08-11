import msgpack
import sys
import yaml
import base64
import json
from Crypto.Cipher import AES
import hmac
import hashlib
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import binascii
#put raw server app datatype response here (from wireshark data description)
packedRaw = b"\x92\x85\xa6\x72\x65\x73\x75\x6c\x74\x00\xa4\x64\x61\x74\x65\xb3\x32\x30\x32\x36\x2f\x30\x33\x2f\x33\x30\x20\x31\x33\x3a\x31\x33\x3a\x30\x30\xa7\x76\x65\x72\x73\x69\x6f\x6e\xa5\x30\x39\x2e\x30\x31\xa4\x66\x6c\x61\x67\xa1\x30\xa7\x73\x65\x73\x73\x69\x6f\x6e\xad\x36\x39\x63\x61\x37\x36\x64\x63\x62\x63\x37\x31\x39\x93\x00\x91\x93\xce\x00\x02\x05\xa8\x14\x01\xce\x00\x04\xb2\x98"
#ADD b prefix when bytes!

#Python to JSON
toBeJson = [0, [[1, 'localhosttesting_20260326154312', 'breadbreakr test 1', '2026-01-23 17:46:11', '2050-02-22 17:46:11', 1, 3], [2, 'localhosttesting_20260327133850', 'breadbreakr test 2', '2026-01-23 17:46:11', '2069-02-22 17:46:11', 0, 2]]]


#put YAML binary data here
yamlData = "AAAAA/6+3u8AAAB0AAE3W5rvrNpHDrTAc00q9T0fAAAAMeGPSWM/lVkeUhjGy97CzR9FRpCuzUjHJ0H8quMP+rYxe3d+wQwTzoaGZKTZ+F+P10iZCqmTQKiJ9NYQ5yg/NwzXBtPl8KLyctFRWuVGLVux9GCVy+XTs6kKCA5N7m420A=="

#udp decryption

encryptedUDP = bytes.fromhex("08de39187857f593df6434570269fc85257177feb734d70af47dcd5bee8f9a6332f0b1f9de7a343d7ae50bb1a957123805bde17e7700a26920445481a91dfe0e")

udpIV = bytes.fromhex("185af50497054644bf89f96ff2f798b2") #375b9aefacda470eb4c0734d2af53d1f - workslol #778d0e05fc2341ac9dfd4d85e7e841fc - lobby2 #185af50497054644bf89f96ff2f798b2 - patched

udpKey = bytes.fromhex("3710c0f30922423a8fd8befcc1f83b3d") #fa83f3c959a34b22af8077bca022a012 - workslol #25917d4f165141feaa19bcbcff7c5d19 - lobby2 #3710c0f30922423a8fd8befcc1f83b3d - patched

sid = bytes.fromhex("c2498a5532f947808e8684812b022b95") #40cb64adeaa648389f3f3c2e091128ad - workslol #e6a2a4727c144356a9b63a3cb5ae5498 - lobby2 #c2498a5532f947808e8684812b022b95 - patched
hashKey = bytes.fromhex("61a174c3f20a4b75bb4d2f17e183f25e") #21af7e438c7f40f4a5d9242f03fc5a66 - workslol #58b3b5f72b0b41969fa7ab535e4fb199 - lobby2 #61a174c3f20a4b75bb4d2f17e183f25e - patched

#udp decryption 2
udpIV2 = bytes.fromhex("778d0e05fc2341ac9dfd4d85e7e841fc")

udpKey2 = bytes.fromhex("25917d4f165141feaa19bcbcff7c5d19")

sid2 = bytes.fromhex("e6a2a4727c144356a9b63a3cb5ae5498")
hashKey2 = bytes.fromhex("58b3b5f72b0b41969fa7ab535e4fb199")


#functions
def nullPadding(data, block_size):
    padLength = block_size - (len(data) % block_size)
    return data + b'\x00' * padLength

print("Enter 1 to turn value data string from Wireshark to byte format\n\nEnter 2 to unpack it.\n\nEnter 3 to decode yaml data\n\nEnter 4 to decrypt UDP packets\n\nEnter 5 to decrypt packet with alternative keys.\n\nEnter 6 to turn Python list into JSON.")
userInput = input()

if userInput == "1":
    
    packedBytes = ""
    for i in range(0, len(packedRaw), 2):
        packedBytes += packedRaw[i:i + 2] + r"\x"
        
    packedBytes = r"\x" + packedBytes[:-2]
    print("Put this result in packedRaw with b prefix and run 2.\n")
    print(packedBytes)
    
elif userInput == "2":
    

    unpacked = msgpack.unpackb(packedRaw)
    print(unpacked)
    
elif userInput == "3":
    
    decodedData = base64.b64decode(yamlData)
    print(decodedData)
    
elif userInput == "4":
    
    cipher = AES.new(udpKey, AES.MODE_CBC, udpIV)
    decryptedData = cipher.decrypt(encryptedUDP)
    
    iv = encryptedUDP[32:48] #32 hex char
    print(f"Payload assumed IV is {iv.hex()}")
    incomingHash = encryptedUDP[:32] #64 hex char
    print(f"Payload assumed Hash is {incomingHash.hex()}")
    cipherText = encryptedUDP[48:] #96+ hex char
    print(f"Ciphertext is {cipherText.hex()}")
    
    
    #cannot be udpIV from inital auth because is different result each time
    hashGen = iv + cipherText
    

    
    
    # Generate potential HMACs
    macHash = hmac.new(hashKey, hashGen, hashlib.sha256).digest()
    macHashHex = hmac.new(hashKey, hashGen, hashlib.sha256).hexdigest()
    
    
    

    print("Ciphertext Decrypted Hex Value")
    print(decryptedData[48:].hex())
    print("\n")
    
    print("Decrypted Bytes with Encoding")
    print(decryptedData[48:])
    print("\n")
    
    
    print("Payload hash")
    print(incomingHash.hex())
    print("\n")
    
    
    print("Comparing hash2")
    print(macHashHex)

    
    if hmac.compare_digest(macHash, incomingHash):
        print("Valid")
    else:
        print("Mismatch")
    
    
elif userInput == "5": #for testing with different key values when outputs need to be compared
    
    cipher = AES.new(udpKey2, AES.MODE_CBC, udpIV2)
    decryptedData = cipher.decrypt(encryptedUDP)
    
    iv = encryptedUDP[32:48] #32 hex char
    print(f"Payload assumed IV is {iv.hex()}")
    incomingHash = encryptedUDP[:32] #64 hex char
    print(f"Payload assumed Hash is {incomingHash.hex()}")
    cipherText = encryptedUDP[48:] #96+ hex char
    print(f"Ciphertext is {cipherText.hex()}")
    
    
    #cannot be udpIV from inital auth because is different result each time
    hashGen = iv + cipherText
    

    
    
    # Generate potential HMACs
    macHash = hmac.new(hashKey2, hashGen, hashlib.sha256).digest()
    macHashHex = hmac.new(hashKey2, hashGen, hashlib.sha256).hexdigest()
    
    
    

    print("Ciphertext Decrypted Hex Value")
    print(decryptedData[48:].hex())
    print("\n")
    
    print("Decrypted Bytes with Encoding")
    print(decryptedData[48:])
    print("\n")
    
    
    print("Payload hash")
    print(incomingHash.hex())
    print("\n")
    
    
    print("Comparing hash2")
    print(macHashHex)

    
    if hmac.compare_digest(macHash, incomingHash):
        print("Valid")
    else:
        print("Mismatch")

elif userInput == "6": #python to json
    
    jsonStr = json.dumps(toBeJson)
    print(jsonStr)

    
else:
    print("enter 1 or 2 or 3")

