from pathlib import Path

class data_handle:
	def __init__(self,fileName,debugMode=False):
		self.fileName = fileName
		self.debugMode = debugMode

	def printdb(self,strOut):
		if self.debugMode == True:
			print(strOut)

	def checkExist(self):
		filePath = Path(self.fileName)
		if filePath.is_file():
			self.printdb("The file "+self.fileName+" does exist.")
			return True
		else:
			self.printdb("The file "+self.fileName+" does not exist.")
			return False
	
	def fopen(self,mode="r"):
		self.fileOpened = open(self.fileName,mode)
		self.printdb("File "+self.fileName+" opened.")

	def fwrite(self,textOut):
		self.fileOpened.write(textOut)
		self.printdb("File "+self.fileName+" wrote to file.")

	def fclose(self):
		self.fileOpened.close()
		self.printdb("File "+self.fileName+" closed")

	def qwrite(self,textOut,mode='w'):
		self.fopen(mode)
		self.fileOpened.write(textOut)
		self.fileOpened.close()
		self.printdb("File "+self.fileName+" wrote to quickly.")
