#main.py>

#Imports
import sys
import requests
import json
import os
import shutil
import time
import schedule
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
from gui import GUIObject

#TODO - DONT DOWNLOAD ALL THE FILES, JUST TAKE WHAT I NEED AND SAVE IN A LIST.

#StartUp class that deals with the main loop implementation.
####################Start#########################
class StartUp:
	def __init__(self):
		scriptDir = os.path.dirname(os.path.realpath(__file__))
		self.done = False
		self.count = 0
		self.consumer_key = "INSERT KEY HERE"
		self.base_url = 'https://api.tdameritrade.com/v1/marketdata/chains'
		self.quote_url = 'https://api.tdameritrade.com/v1/marketdata/quotes'
		self.file = ''
		self.ticker = ''
		self.quoteprice = 0.0
		self.percentdone = 0
		self.datelistput = []
		self.putlist = []
		self.calllist = []
		self.putdatalist = []
		self.calldatalist = []
		self.calljsonobjlist = []
		self.putjsonobjlist = []
		self.calljsonobjlistfinal = []
		self.putjsonobjlistfinal = []
		self.quotepricelist = []
		self.logfilename = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

	def main_loop(self):
		self.count = 0
		while (self.count < len(tickerlist)) and not self.done:
		#while (self.count < 1) and not self.done:
				self.ticker = final_tickerlist[self.count]
				print("Entering while loop for: {}".format(self.ticker))
				self.file = self.ticker
				self.quoteprice = self.quotepricelist[self.count]
				self.parse_json_data()
				self.count += 1

		self.write_to_logs("intro")
		self.analysis()

	def make_requests(self):
	    #Delay the requests by 1 second each.
		self.count = 0
		#for tick in range(1):
		for ticker in range(len(tickerlist)):
			#time.sleep(1)

			self.ticker = final_tickerlist[self.count]
			self.file = self.ticker
			self.count += 1

			#Caclulate and print completion percentage
			self.percentdone = self.count / len(tickerlist) * 100
			#self.percentdone = self.count / 1 * 100
			if self.count >= 1:
				if self.percentdone % 10 <= 2:
					print("The requests are {:.2f}%  complete!".format(self.percentdone))

			try:
				time.sleep(1.5)
				self.page = requests.get(url = self.base_url, params = {'apikey' : self.consumer_key,'symbol' : self.ticker,'contractType' : 'ALL'})

			except:
				time.sleep(10)
				self.count = self.count - 1
				self.write_to_logs("optionrequesterror")

			#Get current price from market.
			try:
				time.sleep(1.5)
				self.quote = requests.get(url = self.quote_url, params = {'apikey' : self.consumer_key, 'symbol' : self.ticker})
			except:
				time.sleep(10)
				self.count = self.count - 1
				self.write_to_logs("quoterequesterror")

			#Parse the returned JSON.
			#Load the JSON and prepare to print the infromation.
			self.content = json.loads(self.page.content)
			self.quote_content = json.loads(self.quote.content)
			print(self.ticker + "\n\n\n")
			print(self.quote_content)

			try:
				self.quotepricelist.append(self.quote_content[self.ticker]["closePrice"])
				self.quoteprice = self.quotepricelist[ticker]

			except KeyError:
				self.write_to_logs("ValueError")
				self.quoteprice = 0.0

			#Get a list of dates call and put dates will be the same.		
			for i in self.content["callExpDateMap"]:
				for j in self.content["callExpDateMap"][i]:				
					for k in self.content["callExpDateMap"][i][j]:
						self.calljsonobjlist.append(JSONObject(self.content['symbol'], k['putCall'], k['description'], k['symbol'], k['mark'], 
										k['closePrice'], k['volatility'], k['delta'], k['gamma'], k['theta'], 
										k['vega'], k['rho'], k['strikePrice'], k['daysToExpiration'], 
										k['percentChange'], k['inTheMoney'], k['last'], self.quoteprice))
					
			for i in self.content["putExpDateMap"]:
				for j in self.content["putExpDateMap"][i]:			
					for k in self.content["putExpDateMap"][i][j]:
						self.putjsonobjlist.append(JSONObject(self.content['symbol'], k['putCall'], k['description'], k['symbol'], k['mark'], 
										k['closePrice'], k['volatility'], k['delta'], k['gamma'], k['theta'], 
										k['vega'], k['rho'], k['strikePrice'], k['daysToExpiration'], 
										k['percentChange'], k['inTheMoney'], k['last'], self.quoteprice))

	def write_to_logs(self, msgtype):
		with open(scriptDir + os.path.sep + 'logs/' + self.logfilename +'.txt', 'a') as self.json_file:
				if msgtype == "intro":
					self.json_file.write("##########################\n")
					self.json_file.write(self.logfilename)
					self.json_file.write("\nProgram was succesfull...\n")

				if msgtype == "keyerror":
					self.json_file.write("\nKey Error: {}\n".format(self.ticker))

				if msgtype == "oor":
				    self.json_file.write("\nRange Error: List for {} could not print. Out of range.\n".format(self.ticker))

				if msgtype == "optionrequesterror":
					self.json_file.write("Option Chain Request Failed: {}\n".format(self.ticker))

				if msgtype == "quoterequesterror":
					self.json_file.write("Quote Request Failed: {}\n".format(self.ticker))

				if msgtype == "ValueError":
					self.json_file.write("ValueError with ticker: {}".format(self.ticker))

				if msgtype == "NoFileError":
					self.json_file.write("No file exists for: {}".format(self.ticker))

	def parse_json_data(self):
		#Parsing JSON.
		print("Entering parse_json_data for: {}".format(self.ticker))

		#CALLS
		#Save and get the last close price.
		for m in range(len(self.calljsonobjlist)):
			try:
				self.calljsonobjlist[m].get_last_close()
			except ValueError:
				self.write_to_logs("ValueError")
				print("ValueError with: {}".format(self.ticker))

		#PUTS
		#Save and get the last close price.
		for m in range(len(self.putjsonobjlist)):
			try:
				self.putjsonobjlist[m].get_last_close()
			except ValueError:
				self.write_to_logs("ValueError")
				print("ValueError with: {}".format(self.ticker))

		#Filter undesirable options out.  
		self.calljsonobjlist = list(filter(lambda x: (x.daystoexp > 6), self.calljsonobjlist))
		self.calljsonobjlist = list(filter(lambda x: (x.closeprice > 0.15), self.calljsonobjlist))

		for p in range(len(self.calljsonobjlist)):
			self.calljsonobjlist[p].calculate_strike_diff()

			if (self.calljsonobjlist[p].strikepercentagediff <= self.calljsonobjlist[p].quotepercenttooptionstrikepos) and (self.calljsonobjlist[p].strikepercentagediff >= self.calljsonobjlist[p].quotepercenttooptionstrikeneg):
				self.calljsonobjlistfinal.append(self.calljsonobjlist[p])

		self.putjsonobjlist = list(filter(lambda x: (x.daystoexp > 6), self.putjsonobjlist))
		self.putjsonobjlist = list(filter(lambda x: (x.closeprice > 0.15), self.putjsonobjlist))

		for p in range(len(self.putjsonobjlist)):
			self.putjsonobjlist[p].calculate_strike_diff()

			if (self.putjsonobjlist[p].strikepercentagediff <= self.putjsonobjlist[p].quotepercenttooptionstrikepos) and (self.putjsonobjlist[p].strikepercentagediff >= self.putjsonobjlist[p].quotepercenttooptionstrikeneg):
				self.putjsonobjlistfinal.append(self.putjsonobjlist[p])

		self.calculate_percentage()
				
		self.calljsonobjlistfinal.sort(key=lambda x: x.percentchangefinal, reverse=True)
		self.putjsonobjlistfinal.sort(key=lambda x: x.percentchangefinal, reverse=True)

	def calculate_percentage(self): 
		for x in range(len(self.calljsonobjlistfinal)):
			print("CLOSE PRICE: " + str(self.calljsonobjlistfinal[x].closeprice))
			print("LAST CLOSE: " + str(self.calljsonobjlistfinal[x].lastclose))
			#Gain.
			if (self.calljsonobjlistfinal[x].lastclose < self.calljsonobjlistfinal[x].closeprice) and (self.calljsonobjlistfinal[x].lastclose != 0.0):
				self.calljsonobjlistfinal[x].percentchangefinal = ((float(self.calljsonobjlistfinal[x].closeprice) / float(self.calljsonobjlistfinal[x].lastclose)) * 100.0) - 100.0
		    #Loss.
			if (self.calljsonobjlistfinal[x].lastclose > self.calljsonobjlistfinal[x].closeprice) and (self.calljsonobjlistfinal[x].lastclose != 0.0):
				self.calljsonobjlistfinal[x].percentchangefinal = ((float(self.calljsonobjlistfinal[x].closeprice) / float(self.calljsonobjlistfinal[x].lastclose)) * 100.0) * -1.0

			#Same.
			if self.calljsonobjlistfinal[x].lastclose == self.calljsonobjlistfinal[x].closeprice:
				self.calljsonobjlistfinal[x].percentchangefinal = 0.0

		for x in range(len(self.putjsonobjlistfinal)):
			print("CLOSE PRICE: " + str(self.putjsonobjlistfinal[x].closeprice))
			print("LAST CLOSE: " + str(self.putjsonobjlistfinal[x].lastclose))
			#Gain.
			if (self.putjsonobjlistfinal[x].lastclose < self.putjsonobjlistfinal[x].closeprice) and (self.putjsonobjlistfinal[x].lastclose != 0.0):
				self.putjsonobjlistfinal[x].percentchangefinal = ((float(self.putjsonobjlistfinal[x].closeprice) / float(self.putjsonobjlistfinal[x].lastclose)) * 100.0) - 100.0

			#Loss.
			if (self.putjsonobjlistfinal[x].lastclose > self.putjsonobjlistfinal[x].closeprice) and (self.putjsonobjlistfinal[x].lastclose != 0.0):
				self.putjsonobjlistfinal[x].percentchangefinal = ((float(self.putjsonobjlistfinal[x].closeprice) / float(self.putjsonobjlistfinal[x].lastclose)) * 100.0) * -1.0

			#Same.
			if (self.putjsonobjlistfinal[x].lastclose == self.putjsonobjlistfinal[x].closeprice) or (self.putjsonobjlistfinal[x].lastclose == 0.0):
				self.putjsonobjlistfinal[x].percentchangefinal = 0.0

	def analysis(self):
		print("Len of put = {}".format(len(self.putjsonobjlist)))
		print("Len of call = {}".format(len(self.calljsonobjlist)))

		print("Len of put = {}".format(len(self.putjsonobjlistfinal)))
		print("Len of call = {}".format(len(self.calljsonobjlistfinal)))

		print("\n\nANALYSIS RESULTS: TOP 10 CHANGERS")
		print("CALLS:")

		#Print top 10 changers.
		try:
			with open(scriptDir + os.path.sep + 'data/analysisData/' + self.logfilename + '.txt', 'a') as self.json_file:
				self.json_file.write("ANALYSIS RESULTS: TOP 10 CHANGERS\n")
				self.json_file.write("CALLS:\n")

			for i in range(10):
				print("######################################")
				print("Type: {}".format(self.calljsonobjlistfinal[i].putCall)) 
				print("Description: {}".format(self.calljsonobjlistfinal[i].description))
				print("Yday Close Price: {}".format(self.calljsonobjlistfinal[i].lastclose))
				print("Today Close price: {}".format(self.calljsonobjlistfinal[i].closeprice))
				print("Strike Price: {}".format(self.calljsonobjlistfinal[i].strikeprice))
				print("Days To Expiry: {}".format(self.calljsonobjlistfinal[i].daystoexp))
				print("% Change: {:.2f}".format(self.calljsonobjlistfinal[i].percentchangefinal))
				print("In The Money?: {}".format(self.calljsonobjlistfinal[i].inTheMoney))
				print("Quote Price: {}".format(self.calljsonobjlistfinal[i].quoteprice))
				print("Strike % Diff: {:.2f}".format(self.calljsonobjlistfinal[i].strikepercentagediff))
				print("######################################")

			with open(scriptDir + os.path.sep + 'data/analysisData/' + self.logfilename + '.txt', 'a') as self.json_file:
				self.json_file.write("######################################\n")
				self.json_file.write("Type: {}\n".format(self.calljsonobjlistfinal[i].putCall)) 
				self.json_file.write("Description: {}\n".format(self.calljsonobjlistfinal[i].description))
				self.json_file.write("Yday Close Price: {}\n".format(self.calljsonobjlistfinal[i].lastclose))
				self.json_file.write("Today Close price: {}\n".format(self.calljsonobjlistfinal[i].closeprice))
				self.json_file.write("Strike Price: {}\n".format(self.calljsonobjlistfinal[i].strikeprice))
				self.json_file.write("Days To Expiry: {}\n".format(self.calljsonobjlistfinal[i].daystoexp))
				self.json_file.write("% Change: {:.2f}\n".format(self.calljsonobjlistfinal[i].percentchangefinal))
				self.json_file.write("In The Money?: {}\n".format(self.calljsonobjlistfinal[i].inTheMoney))
				self.json_file.write("Quote Price: {}\n".format(self.calljsonobjlistfinal[i].quoteprice))
				self.json_file.write("Strike % Diff: {:.2f}\n".format(self.calljsonobjlistfinal[i].strikepercentagediff))
				self.json_file.write("######################################\n")		
		except:
				print("ERROR: printing Call list. List out of range.")
				self.write_to_logs("oof")

		print("\n\n\n\nPUTS:")
		try:
			with open(scriptDir + os.path.sep + 'data/analysisData/' + self.logfilename +'.txt', 'a') as self.json_file:
				self.json_file.write("\n\n\n\nPUTS:\n")

			for i in range(10):
				print("######################################")
				print("Type: {}".format(self.putjsonobjlistfinal[i].putCall)) 
				print("Description: {}".format(self.putjsonobjlistfinal[i].description))
				print("Yday Close Price: {}".format(self.putjsonobjlistfinal[i].lastclose))
				print("Today Close Price: {}".format(self.putjsonobjlistfinal[i].closeprice))
				print("Strike Price: {}".format(self.putjsonobjlistfinal[i].strikeprice))
				print("Days To Expiry: {}".format(self.putjsonobjlistfinal[i].daystoexp))
				print("% Change: {:.2f}".format(self.putjsonobjlistfinal[i].percentchangefinal))
				print("In The Money?: {}".format(self.putjsonobjlistfinal[i].inTheMoney))
				print("Quote Price: {}".format(self.putjsonobjlistfinal[i].quoteprice))
				print("Strike % Diff: {:.2f}".format(self.putjsonobjlistfinal[i].strikepercentagediff))
				print("######################################")

			with open(scriptDir + os.path.sep + 'data/analysisData/' + self.logfilename + '.txt', 'a') as self.json_file:
				self.json_file.write("######################################\n")
				self.json_file.write("Type: {}\n".format(self.putjsonobjlistfinal[i].putCall)) 
				self.json_file.write("Description: {}\n".format(self.putjsonobjlistfinal[i].description))
				self.json_file.write("Yday Close Price: {}\n".format(self.putjsonobjlistfinal[i].lastclose))
				self.json_file.write("Today Close Price: {}\n".format(self.putjsonobjlistfinal[i].closeprice))
				self.json_file.write("Strike Price: {}\n".format(self.putjsonobjlistfinal[i].strikeprice))
				self.json_file.write("Days To Expiry: {}\n".format(self.putjsonobjlistfinal[i].daystoexp))
				self.json_file.write("% Change: {:.2f}\n".format(self.putjsonobjlistfinal[i].percentchangefinal))
				self.json_file.write("In The Money?: {}\n".format(self.putjsonobjlistfinal[i].inTheMoney))
				self.json_file.write("Quote Price: {}\n".format(self.putjsonobjlistfinal[i].quoteprice))
				self.json_file.write("Strike % Diff: {:.2f}\n".format(self.putjsonobjlistfinal[i].strikepercentagediff))
				self.json_file.write("######################################\n")        
		except:
			print("ERROR: printing Put list. List out of range.")
			self.write_to_logs("oof")

        #Save the close prices for the next day.
		for m in range(len(self.calljsonobjlist)):
			try:
				self.calljsonobjlist[m].save_last_close()
			except ValueError:
				self.write_to_logs("ValueError")
				print("ValueError with: {}".format(self.ticker))

		for m in range(len(self.putjsonobjlist)):
			try:
				self.putjsonobjlist[m].save_last_close()
			except ValueError:
				self.write_to_logs("ValueError")
				print("ValueError with: {}".format(self.ticker))

#################END CLASS###########################

################JSON OBJECT##########################

class JSONObject:
	def __init__(self, ticker, putCall, description, symbol, mark, closeprice, volatility, delta, gamma, theta, vega, rho, strikeprice, daystoexp, percentchange, inTheMoney, last, quoteprice):
		self.ticker = ticker
		self.putCall = putCall
		self.description = description
		self.symbol = symbol
		self.mark = mark
		self.closeprice = closeprice
		self.percentchange = percentchange
		self.volatility = volatility
		self.delta = delta
		self.gamma = gamma
		self.theta = theta
		self.vega = vega
		self.rho = rho
		self.strikeprice = strikeprice
		self.daystoexp = daystoexp
		self.inTheMoney = inTheMoney
		self.percentchangefinal = 0
		self.last = last
		self.strikepercentagediff = 0
		self.quoteprice = quoteprice
		self.quotepercenttooptionstrikepos = 0
		self.quotepercenttooptionstrikeneg = 0
		self.lastclose = 0.0

	def calculate_strike_diff(self):
		self.strikepercentagediff = (self.strikeprice / self.quoteprice) * 100

		if self.quoteprice <= 50:
			self.quotepercenttooptionstrikepos = 120
			self.quotepercenttooptionstrikeneg = 80

		elif (self.quoteprice > 50) and (self.quoteprice <= 100):
			self.quotepercenttooptionstrikepos = 115
			self.quotepercenttooptionstrikeneg = 85
				
		elif (self.quoteprice > 100) and (self.quoteprice <= 200):
			self.quotepercenttooptionstrikepos = 112
			self.quotepercenttooptionstrikeneg = 87

		elif self.quoteprice > 200:
			self.quotepercenttooptionstrikepos = 105
			self.quotepercenttooptionstrikeneg = 95

	def save_last_close(self):
		with open(scriptDir + os.path.sep + 'data/closeInfo/yesterday/' + self.symbol + '.json', 'w') as self.json_file:
			self.json_file.write(str(self.closeprice))

	def get_last_close(self):
		try:
			with open(scriptDir + os.path.sep + 'data/closeInfo/yesterday/' + self.symbol + '.json', 'r') as self.json_file:
				closeval = self.json_file.read()
            
				self.lastclose = float(closeval)
		except:
			with open(scriptDir + os.path.sep + 'data/closeInfo/yesterday/' + self.symbol + '.json', 'w') as self.json_file:
				self.json_file.write(str(self.closeprice))		

################END CLASS############################
#Entry point.
if __name__ == '__main__':
	#Get the ticker list set up.
	tickerfile = open('ticker.txt', 'r')
	tickerlist = []
	ticker_count = 0
	stripped_tickerlist = []
	final_tickerlist = []

	scriptDir = os.path.dirname(os.path.realpath(__file__))

	while True:
		ticker_count +=1

		#Get the next line.
		line = tickerfile.readline()
			
		tickerlist.append(line)

		#If the line is empty close the file.
		if not line:
			break

	##########Data Clensing##########################

	#Remove the newlines in the list.
	for element in tickerlist:
		stripped_tickerlist.append(element.strip())

	#Make list upper case.
	for element in stripped_tickerlist:
		final_tickerlist.append(element.upper())

	#################################################
	#File cleanup.
	tickerfile.close()

	#Calculate time to complete one request rotation.
	time_len = ((ticker_count * 4.9) / 60) / 60

	#Program Info.
	print("Welcome to OptionsReader.");
	print("This program is in early development stages.");
	print("Amount of tickers counted in file: {}".format(ticker_count))
	print("It will take on average {:.2f} hours to process all {} tickers\n\n".format(time_len, ticker_count))

	#Create needed directories if they do not already exist.
	if not os.path.exists("data/closeInfo/today/"):
	    os.makedirs(scriptDir + os.path.sep + "data/closeInfo/today/")

	if not os.path.exists("data/closeInfo/yesterday/"):
	    os.makedirs(scriptDir + os.path.sep + "data/closeInfo/yesterday/")

	dataprocesser = StartUp()

	#Start the loop.
	dataprocesser.make_requests()
	dataprocesser.main_loop()


################################################################################################################################
	#Create the app instance and gui instance.
	# app = QApplication([])

	# #app.setStyle("Fusion")

	# dark_palette = QPalette()

	# dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
	# dark_palette.setColor(QPalette.WindowText, Qt.white)
	# dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
	# dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
	# dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
	# dark_palette.setColor(QPalette.ToolTipText, Qt.white)
	# dark_palette.setColor(QPalette.Text, Qt.white)
	# dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
	# dark_palette.setColor(QPalette.ButtonText, Qt.black)
	# dark_palette.setColor(QPalette.BrightText, Qt.red)
	# dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
	# dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
	# dark_palette.setColor(QPalette.HighlightedText, Qt.black)

	# app.setPalette(dark_palette)

	# app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
	# #app.setWindowIcon(QIcon('logo.png'))

	# GUI = GUIObject()
	# GUI.startButton.clicked.connect(lambda: GUI.display(1))
	# GUI.doneButton.clicked.connect(lambda: GUI.display(0))

	# #Let QT handle the GUI
	# app.exec_()
	#sys.exit(app.exec_())
################################################################################################################################


	#Scheduled times.
	#schedule.every().day.at("06:40").do(app.main_loop())
	#schedule.every().day.at("08:45").do(app.main_loop())
	#schedule.every().day.at("10:45").do(app.main_loop())
	#schedule.every().day.at("13:15").do(app.main_loop())

	#while 1:
		#schedule.run_pending()
		#time.sleep(1)