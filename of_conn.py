import socket
from struct import *

#create an INET, STREAMing socket
s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

# OF Controller port is 6633
s.connect(("192.168.56.102", 6633))

# OF Header (HELLO)

ofp_version = 0x01 # 1 byte
ofp_type = 0 # for HELLO initiation, 1 byte
ofp_length = 8 # 2 bytes
ofp_transid = 9 # 4 bytes
ofp_header = pack('!BBHI', ofp_version, ofp_type, ofp_length, ofp_transid)
s.send(ofp_header)

while (True) :
	data = s.recv(8)
	print data
	print len(data)
	recv_ofp_header = unpack('!BBHI', data)
	print recv_ofp_header
	recv_ofp_type = recv_ofp_header[1]
	if recv_ofp_type == 5 :
		ofp_type = 0x06 # 1 byte
		ofp_length =  80 # 2 bytes
		ofp_transid =  0 # 4 bytes
		of_packet = ''
		# datapath id = datapath_id_p1 + datapath_id_p2
		datapath_id_p1 = 0x0000 # 4 bytes
		datapath_id_p2 = 0x0001 # 4 bytes
		max_pkt_buff = 256 # 4 bytes
		num_tables = 255 # 1 byte
		reserved = '0' # 3 bytes
		capability_flags = 0x00000077  # 4 byte having all capability flags
		action_flags = 0x00000fff # 4 bytes of actions flag list
		port_num_1 = 0xfffe # 2 bytes
		# MAC Address into two parts mac_add_p1 (4 b) + mac_add_p2 (2 b) = (6 b)
		mac_add_p1 = 0x1a98f198 # 4 bytes
		mac_add_p2 = 0xb84d # 2 bytes
		port_name_1 = 0x7331 # 2 bytes
		port_name_2 = 0x0000 # 4 bytes x 3 times we will send
		port_cnf_flag_1 = 0x0001 # 4 bytes
		port_state_flag_1 = 0x0001 # 4 bytes
		port_curnt_flag_1 = 0x0000 # 4 bytes
		port_adv_flag_1 = 0x0000 # 4 bytes
		port_sub_flag = 0x0000 # 4 bytes
		port_peer_flag = 0x0000 # 4 bytes
		port_d = pack('!HIHHIIIHIIIIII', port_num_1, mac_add_p1, mac_add_p2, port_name_1, port_name_2, port_name_2, port_name_2, port_name_2, port_cnf_flag_1, port_state_flag_1, port_curnt_flag_1, port_adv_flag_1, port_sub_flag, port_peer_flag)
		feature_reply = pack('!IIIB3sII', datapath_id_p1, datapath_id_p2, max_pkt_buff, num_tables, reserved, capability_flags, action_flags)
		ofp_header = pack('!BBHI', ofp_version, ofp_type, ofp_length, ofp_transid)
		of_packet = ofp_header + feature_reply + port_d
		s.send(of_packet)
		print 'OF_CONN: WE SENT FEATURE REPLY'
	elif recv_ofp_type == 9 :
		 x = s.recv(4)
	elif recv_ofp_type == 7:
		of_packet = ''
		ofp_type = 0x08
		ofp_length = 12 # 12 bytes
		handle_ipfrag = 0x0000 # 2 bytes
		max_byte_flow = 0xffff # 2 bytes
		ofp_header = pack('!BBHI', ofp_version, ofp_type, ofp_length, ofp_transid)
		getfeature_reply = pack('!HH', handle_ipfrag, max_byte_flow)
		of_packet = ofp_header + getfeature_reply
		s.send(of_packet)


		 
