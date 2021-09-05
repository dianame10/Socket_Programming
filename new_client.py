import socket
import sys
import os

def get_information():
    try:
        if len(sys.argv) < 4 or len(sys.argv) > 4:
            print("you should enter 3 parameters which are hostname or IP address, port number and filename you wishes to retrieve")
            sys.exit()
            
        hostname = str(sys.argv[1])
        port_number = int(sys.argv[2])
        filename = str(sys.argv[3])        
        if port_number < 1024 or port_number > 64000:
            print("The port number should be between 1,024 and 64,000")
            sys.exit()
        if os.path.isfile(filename) == True:
            print("File already exist")
            sys.exit() 
        else:  
            socket.getaddrinfo(hostname, port_number)          
    except socket.gaierror:
        print("The hostname does not exist or an IP address is not well-formed")
        sys.exit()   
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    except socket.error:
        print("Socket not successfuly created")
        sys.exit()
        
    try:
        client_socket.connect((hostname, port_number))
    except socket.error:
        client_socket.close()
        print("Connection fail")
        sys.exit()    
        
    magicNo = 0x497E                    #fixedHeader
    file_type = 1                       #fixedHeader, already 1 byte
    n = len(bytes((filename).encode())) #FilenameLen
    file_request = bytes((filename).encode("utf-8"))
    
    magic_result = magicNo << 24
    index1 = magic_result & 0x0000FFFFFF
    result1 = magic_result | index1
    
    type_result = file_type << 16
    index2 = type_result & 0x00FFFFFFFF
    result2 = type_result | index2
    
    index3 = n & 0x0000FFFFFF
    result3 = index3
    
    result = result1 + result2
    results = result + result3
    
    new_hex = hex(results)[2:]
    
    array = bytearray.fromhex(new_hex)
    
    fileRequest = array + bytearray(file_request)
    
    
    client_socket.sendall(fileRequest)
    
    receive_and_read_file(client_socket, filename)
    
    client_socket.close()    
    


def receive_and_read_file(client_socket, filename):
    
    client_socket.settimeout(1)
    try:
        message = client_socket.recv(4096)
    except socket.error:
        print("Timeout! there is a gap more than one second while reading the file response")
        client_socket.close()
        sys.exit()
        
    byte_array = b''
    new_msg = True
    
    if new_msg:
        new_msg = False
        decoded_message = message
        new_byte_array = decoded_message
        byte_array += new_byte_array
    magic_byte = (byte_array[:2]).hex()
    magicNo = int(magic_byte, 16)
    file_type = byte_array[2]
    status_code = byte_array[3]
    dataLength = int(byte_array[4:8].hex(), 16)
    if magicNo == 0x497E:
        pass
    if file_type == 2:
        pass
    if status_code == 1 or status_code == 0:
        pass
    else:
        print("The file response is not valid")
        client_socket.close()
        sys.exit()
        
    if status_code == 0:
        print("The file yor wishes to retrieve is an empty file or does not exist on server side")
        client_socket.close()
        sys.exit()
    else:
        content = byte_array[8:]
        bytes_received = len(content)
        if dataLength != bytes_received:    
            print("Inconsistency of data in the file response")
            client_socket.close()
            sys.exit()
        else:
            try:
                with open(filename, 'wb') as f:
                    f.write(content)
                
            except IOError:
                print("Error occurs! cannot create new file for writting")
                client_server.close()
                f.close()
                sys.exit()
        print(("Content of the file you wishes is successfuly transfer into your local file, now you can open it locally in your device. The number of bytes received is {} bytes").format(bytes_received))   
        file = open(filename)
        read = file.read()
        
        file.close()
        byte_array = b''
        new_msg = True
        client_socket.close()
        sys.exit()
        
    
    
    
def main():
    get_information()
    
main()