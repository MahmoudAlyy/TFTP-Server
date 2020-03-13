import socket
import struct

def read_func(filename, client_address):
    chunck = 512
    data_list = []
    index = -1
    f = open(filename, "rb")
    while 1:
        temp = f.read(chunck)
        if not temp:
            break
        index = index + 1
        data_list.append(temp)

    opcode = 3
    for i in range(index+1):
        block_number = i+1
        format_str = "!HH{}s".format(len(data_list[i]))
        packet = struct.pack(format_str, opcode, block_number, data_list[i])
        server_socket.sendto(packet, client_address)
        bytes,client_address_temp = server_socket.recvfrom(1024)
        receievd_block_number = struct.unpack("!H", bytes[2:4])
        if bytes[1] != 4  or receievd_block_number[0] != block_number :
            print ("ERROR: IN THE ACK")
    f.close()
    print("DOWNLOAD COMPLETED")
    main()
        

def write_func(filename, client_address):
    ### SEND ACK
    opcode = 4
    block_number = 0
    packet = struct.pack("!HH", opcode, block_number)
    server_socket.sendto(packet,client_address)

    ### Recieve stuff
    f = open(filename, "wb")

    while 1:
        bytes,client_address_temp = server_socket.recvfrom(516)
        f.write(bytes[4:])
        block_number = block_number + 1
        packet = struct.pack("!HH", opcode, block_number)
        server_socket.sendto(packet, client_address)
        if len(bytes) < 516:
            print("UPLOAD COMPLETED")
            break
    f.close()
    main()



def main():
    print("[SERVER] Waiting...")

    bytes, client_address = server_socket.recvfrom(1024)

    for zero_counter in range(2,len(bytes)):
        if bytes[zero_counter] == 0:
            break

    filename = bytes[2:zero_counter]

    if bytes[1] == 1:
        print("READ REQUEST")
        read_func(filename, client_address)
    elif bytes[1] == 2:
        print("WRITE REQUEST")
        write_func(filename, client_address)

    else :
        print("ERROR: DIDN'T RECEIVE A READ OR WRITE REQUEST")


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("127.0.0.1", 69)
    server_socket.bind(server_address)
    print("[SERVER] Socket info:", server_socket)
    main()
