from pathlib import Path
import json

class data_handle:
	def __init__(self,fileName,debugMode=False):
		self.fileName = fileName
		self.debugMode = debugMode


	def printdb(self,strOut):
		#Used in debug mode to print comments if debug is enabled.
		if self.debugMode == True:
			print(strOut)

	def checkExist(self):
		#Checks existence of fileName.
		filePath = Path(self.fileName)
		if filePath.is_file():
			self.printdb("The file "+self.fileName+" does exist.")
			return True
		else:
			self.printdb("The file "+self.fileName+" does not exist.")
			return False
	
	def fopen(self,mode="r"):
		#Open fileName for read (r) by default
		self.fileOpened = open(self.fileName,mode)
		self.printdb("File "+self.fileName+" opened.")

	def fwrite(self,textOut):
		#Write textOut to fileName
		self.fileOpened.write(textOut)
		self.printdb("File "+self.fileName+" wrote to file.")

	def fclose(self):
		#Close fileName
		self.fileOpened.close()
		self.printdb("File "+self.fileName+" closed")

	def qwrite(self,textOut,mode='w'):
		#Quick write to open and close a file for writing quickly
		self.fopen(mode)
		self.fileOpened.write(textOut)
		self.fclose()
		self.printdb("File "+self.fileName+" wrote to quickly.")

	def dictRead(self):
		self.fopen('r')
		fileText = self.fileOpened.read()
		fileDict = json.loads(fileText)
		self.fclose()
		return fileDict

	def dictWrite(self,dictForDump):
		self.fopen('w')
		self.fileOpened.write(json.dumps(dictForDump))
		self.fclose()