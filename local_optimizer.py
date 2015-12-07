import re

class compiler:
	def __init__ (self, c_file):
		self.file_name = c_file

		rfile = open(self.file_name, "r")
		self.code_orig = rfile.read()
		rfile.close()
		self.code_array = self.code_orig.split("\n")
		print self.code_array
		self.write()
		self.constant_fold()
	
	def constant_fold (self):
		for l in self.code_array:
		 	if ( l.contains("=") and not l.contains("==")):
				print (re.split("[.?!,]+", "Hi, my. name is! Shane. boom"))



	def write(self):
		wfile = open(  "%s_optimized.c" % ( self.file_name.split(".")[0]), "w")
		for l in self.code_array:
			wfile.write(l)
			wfile.write("\n")
		wfile.close()

c = compiler("hello.c")
# c.compile