import socket
import datetime
import sys
import os.path

def get_information():
    port_number = int(sys.argv[1])
    if port_number < 1024 or port_number > 64000:
        print("The port number should be between 1,024 and 64,000")
        sys.exit()
    else:
        #hostname = socket.gethostbyname(socket.gethostname())
        #print(hostname)
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind(('', port_number))
            print("socket successfully made and binding success")
        except socket.error:
            print("binding error")
            sys.exit()
            
        try:
            server_socket.listen(10) 
        except socket.error:
            print("The server call listen() error")
            server_socket.close()
            sys.exit()
    create_connection(server_socket, port_number)     
        
def create_connection(server_socket, port_number):
    current = datetime.datetime.today()
    current_time = current.time()
    found = False
    
    while not found:
        client_socket, address = server_socket.accept()
        print(("Connection from {} has been established!").format(address))
        string = ("Time {}, IP address: {}, Port number: {}").format(current_time, address, port_number)
        print(string)
        
        client_socket.settimeout(1)
        try:
            message = client_socket.recv(1029)      #5 bytes of header and 1,024 bytes of filename          
        except socket.error:
            print("Timeout! took more than one second to read the file")
            client_socket.close()
            create_connection(server_socket, port_number)
            #go back to the start of the loop
        
        
        
        
        byte_array = message
        magicNo = int(((byte_array[:2]).hex()), 16)
        file_type = byte_array[2]
        filenameLen = int((byte_array[3:5].hex()), 16)          
        if magicNo == 0x497E:
            pass
        if file_type == 1:
            pass
        if filenameLen >= 1 or filenameLen <= 1024:
            pass
        else:
            print("The file request is not valid")
            client_socket.close()
            create_connection(server_socket, port_number) 
        
        filename = (byte_array[5:])
        if filenameLen != len(filename):
            print("Inconsistency of data in the file request")
            client_socket.close()
            create_connection(server_socket, port_number)
        else:     
            if os.path.isfile(filename.decode('utf-8')) == True:
                try:
                    file = open(filename)
                    content = file.read()
                    success = True
                    
                    file.close()                    
                except IOError:
                    content = "Sorry the file cannot be opened"
                    success = False
                    file.close()
            else:
                content = "Sorry, the file you wishes to retrieve is not available"
                success = False
        fileResponse, bytes_transffered = create_file_response(success, content)
        client_socket.send(fileResponse) 
        client_socket.close()
        if success == True:
            print(("Successfully send the data to client, the length of the data is {} bytes").format(bytes_transffered))
        else:
            print("Successfully send the data to client")
        create_connection(server_socket, port_number)
        
    
        
        
def create_file_response(success, content):
    magicNo = 0x497E              
    file_type = 2
    file_data = content.encode("utf-8")
    
    if success:
        status_code = 1
    else:
        status_code = 0
    
    if status_code == 0:
        data_length = 0
    else:
        data_length = len(bytes(file_data))
    
    
    magic_result = magicNo << 48
    index1 = magic_result & 0x0000FFFFFFFFFFFF
    result1 = magic_result | index1
    
    type_result = file_type << 40
    index2 = type_result & 0x00FFFFFFFFFFFFFF
    result2 = type_result | index2 
    
    status_result = status_code << 32
    index3 = status_result & 0x00FFFFFFFFFFFFFF
    result3 = status_result | index3
    
    data_result1 = data_length & 0x00000000FFFFFFFF
    index_data1 = data_result1

    
    result = result1 + result2
    results3 = result + result3
    
    result4 = results3 + index_data1
    
    new_hex = hex(result4)[2:]
    array = bytearray.fromhex(new_hex) 
    array += bytearray(bytes(file_data))
    bytes_transffered = len(array)
    
    return array, bytes_transffered
    
    
def main():
    get_information()
    
main()