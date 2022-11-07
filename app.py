from flask import Flask,request,render_template
import os
import time
import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import PyPDF2
import re



app = Flask(__name__)

@app.route('/')
@app.route('/main')
def main():
	return render_template("index.html")


@app.route('/webscrap',methods=['POST'])
def webscrap():
	
    
    
    
    
    
    

	int_features =[x for x in request.form.values()]
	website = int_features[0]
	pdf_fold = int_features[1]
	excel_fold = int_features[2]
	x = int_features[3]
	df  = pd.read_csv(x)
	chromeOptions = webdriver.ChromeOptions()
	prefs = {"plugins.always_open_pdf_externally":True,"download.default_directory":pdf_fold}
	chromeOptions.add_experimental_option("prefs",prefs)
	chromeOptions.add_argument("--disable-notifications")
	# chromeOptions.headless = True
	chromedriver = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
	browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)
	for i in range(len(df)):
		browser.get(website)
		record1 = df.iloc[i]
		A1 = record1[0]
		A2 = record1[1]
		A3 = int(record1[2])
		A4 = record1[3]
		A5 = int(record1[4])
		A6 = record1[5]
		A7 = int(record1[6])
		A8 = record1[7]
		A9 = record1[8]
		time.sleep(2)
		Name = browser.find_element(By.ID,'name')
		Name.send_keys(A1)
		time.sleep(2)
		Sex = browser.find_element(By.ID,'sex')
		Sex.send_keys(A2)
		time.sleep(2)
		Day = browser.find_element(By.ID,'day')
		Day.send_keys(A3)
		time.sleep(2)
		Month = browser.find_element(By.ID,'month')
		Month.send_keys(A4)
		time.sleep(2)
		Year = browser.find_element(By.ID,'year')
		Year.clear()
		Year.send_keys(A5)
		time.sleep(2)
		Hour = browser.find_element(By.ID,'hour')
		Hour.send_keys(A6)
		time.sleep(2)
		Minute = browser.find_element(By.ID,'minute')
		Minute.send_keys(A7)
		Country = browser.find_element(By.ID,'country')
		Country.send_keys(A8)
		time.sleep(2)
		City = browser.find_element(By.ID,'city')
		City.clear()
		City.send_keys(A9)
		time.sleep(5)
		ci=browser.find_elements(By.ID,'livesearch')
		ci[0].click()
		time.sleep(5)
		Sub = browser.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[1]/form/div/div/table/tbody/tr[15]/td/input[4]")
		Sub.click()
		time.sleep(5)
		Pd = browser.find_element(By.ID,'btn')
		Pd.click()
		time.sleep(10)
		PDF = browser.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/a[1]')
		PDF.click()
		try:
			time.sleep(10)
			T1=browser.find_element(By.XPATH,'/html/ins')
			T2=T1.find_element(By.XPATH,'//*[@id="aswift_5"]')
			browser.switch_to.frame(T2)
			T3=browser.find_element(By.XPATH,'//*[@id="ad_iframe"]')
			browser.switch_to.frame(T3)
			fin = browser.find_element(By.XPATH,'//*[@id="dismiss-button"]')
			fin.click()
			time.sleep(30)
		except:
			pass
	os.chdir(pdf_fold)
	l=["Name","Gender","DOB","Location"]
	columns=["Name","Gender","DOB","Time","Location"]
	values=[]
	for i in os.listdir():
		Obj = open(i, 'rb')
		pdfReader = PyPDF2.PdfFileReader(Obj)
		pageObj = pdfReader.getPage(0)
		data = pageObj.extractText()
		Eng_Data=re.sub("[^A-Za-z0-9 ]"," ",data)
		Eng_Data=Eng_Data.strip(" ")
		l = [i for i in Eng_Data.split(" ") if i.isalnum()]
		r1 = ['Vedic','Horoscope','Birth','Details','Name','Gender','Date','of','Time','Place','District','Latitude','Longitude','Timezone','W','S']
		data1=[i for i in l if i not in r1]
		name=data1[0]
		gender =data1[1]
		dob=data1[2]+"-"+data1[3]+"-"+data1[4]
		time=data1[5]+"."+data1[6]
		location=data1[7]+"-"+data1[8]+"-"+data1[9]+"-"+data1[10]+"-"+data1[11]+"-"+data1[12]+"-"+data1[13]
		values.append([name,gender,dob,time,location])
	df=pd.DataFrame(values,columns=columns)
	os.chdir(excel_fold)
	df.to_csv("File1.csv",index=False)

	return render_template('index.html',text ="Successfully")

if __name__ == "__main__":
	app.run(debug=True)