from fltk import *
import sys,socket

class TicTacToe(Fl_Window):
	def __init__(self,x,y,w,h,label):
	    	Fl_Window.__init__(self,x,y,w,h,label)
	    	self.begin()
	    	self.but = []
	    	self.used = []
	    	if sys.argv[1] == "server":
	        	self.symbol = "X"
	    	else:
	        	self.symbol = "O"
	    	self.out = Fl_Output(143,38,125,40,"status: ")
	    	self.out.value("Your turn")
	    	for i in range(3):
	        	for j in range(3):
	            		self.but.append(Fl_Button(85+80*j,85+80*i,80,80))
	            		self.but[-1].callback(self.but_cb)
	    	self.end()
	   	 
	    	self.host = sys.argv[2]
	    	self.port = int(sys.argv[3])
	    	self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	    	if sys.argv[1] == "server":
	        	for i in self.but:
		            	i.deactivate()
		        	self.out.value("Opponent's turn")
		        	self.s.bind((self.host,self.port))
	   	 
	    	fd = self.s.fileno()
	    	Fl.add_fd(fd,self.receive_data)
	    
	def but_cb(self,widget):
	    	index = self.but.index(widget)
	    	if index not in self.used:
	        	if sys.argv[1] == "server":
	            		self.but[index].label("X")
	        	else:
	            		self.but[index].label("O")
	       	 
	        	self.used.append(index)
	        	self.send_cb(index)
	    
	def check(self,index):
	    	self.leng = 3
	    	if len(self.used) == self.leng**2:
	        	return "Tie!"
	   	 
	    	h = int(index / 3)
	    	v = index % 3
	    	le = [0,4,8]
	    	ri = [2,4,6]
	    	h_count = 0
	    	v_count = 0
	    	le_count = 0
	    	ri_count = 0
	    	for i in range(3):
	        	if self.but[h+i].label() == self.symbol:
	            		h_count+=1
	        	if self.but[v+i*self.leng].label() == self.symbol:
	            		v_count+=1
	        	if self.but[le[i]].label() == self.symbol:
	            		le_count+=1
	        	if self.but[ri[i]].label() == self.symbol:
	            		ri_count+=1
	           	 
	    	if h_count == 3 or v_count == 3 or le_count == 3 or ri_count == 3:
	        	return "win"
	    	else:
	        	return "keep going"
	
	def send_cb(self,index):
		for i in self.but:
			i.deactivate()
		 
		message = self.check(index)
		if  message == "win":
			text = "You lost!"
			self.out.value("You win!")
		 
			if sys.argv[1] == "server":
				self.s.sendto(text.encode(),self.addr)
			else:
				self.s.sendto(text.encode(),(self.host,self.port))
		 
		elif message == "tie":
			text = "Tie!"
			self.out.value(text)
		 
			if sys.argv[1] == "server":
				self.s.sendto(text.encode(),self.addr)
			else:
				self.s.sendto(text.encode(),(self.host,self.port))
		else:
			self.out.value("Opponent's turn")
		 
			if sys.argv[1] == "server":
				text = self.symbol+str(index)
				self.s.sendto(text.encode(),self.addr)
			else:
				text = self.symbol+str(index)
				self.s.sendto(text.encode(),(self.host,self.port))
	 
	def receive_data(self,fd):
		(text,self.addr) = self.s.recvfrom(1024)
		text = text.decode()
	 
	if text == "You lost!" or text == "Tie!":
		self.out.value(text)
	 
	else:
		self.out.value("Your turn")
		for i in self.but:
			i.activate()
		if int(text[1]) not in self.used:
			self.but[int(text[1])].label(text[0])
			self.used.append(int(text[1]))
	 
a = TicTacToe(55,55,400,400,"sockets_"+sys.argv[1])
a.show()
Fl.run()
