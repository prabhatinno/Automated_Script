import os,sys,glob
import re,csv,re
from datetime import date,timedelta
import calendar
import datetime
import pysftp
count=0
naming=[]
location=os.getcwd()+'/'+sys.argv[1]
if((sys.argv[1].split('/')[1].title()!='Clinical') and (sys.argv[1].split('/')[1].title()!='Financial')):
	print('Invalid Input')
	exit()	
list_of_folder = glob.glob(str(location)+'/*')
latest_file =max(list_of_folder, key=os.path.getctime)
# print latest_file
my_date = date.today()
if(calendar.day_name[my_date.weekday()]=='Monday'):s_file=(datetime.datetime.today() - timedelta(days=8)).strftime('%Y%m%d')
if(calendar.day_name[my_date.weekday()]=='Tuesday'):s_file=(datetime.datetime.today() - timedelta(days=9)).strftime('%Y%m%d')
if(calendar.day_name[my_date.weekday()]=='Wednesday'):s_file=(datetime.datetime.today() - timedelta(days=10)).strftime('%Y%m%d')
if(calendar.day_name[my_date.weekday()]=='Thursday'):s_file=(datetime.datetime.today() - timedelta(days=11)).strftime('%Y%m%d')
if(calendar.day_name[my_date.weekday()]=='Friday'):s_file=(datetime.datetime.today() - timedelta(days=12)).strftime('%Y%m%d')
if(calendar.day_name[my_date.weekday()]=='Saturday'):s_file=(datetime.datetime.today() - timedelta(days=13)).strftime('%Y%m%d')
if(calendar.day_name[my_date.weekday()]=='Sunday'):s_file=(datetime.datetime.today() - timedelta(days=14)).strftime('%Y%m%d')
# print s_file
l_file =datetime.datetime.today().strftime('%Y%m%d')
# print l_file
if(sys.argv[1].split('/')[1].title()=='Clinical'):
	reader = re.sub('\\n','',open('config.csv', 'r').readlines()[:3][0])
if(sys.argv[1].split('/')[1].title()=='Financial'):
	reader = re.sub('\\n','',open('config.csv', 'r').readlines()[:3][1])
optum_file_naming=reader.split(',')
#print optum_file_naming
for file_naming in optum_file_naming:
	naming.append(re.sub(r's_file',s_file,re.sub(r'l_file',l_file,file_naming)))
for root, dirs, files in os.walk(latest_file):
	for file in files:
		if(file.endswith('.txt')):
			print file
			for file1 in naming:
				if(file==file1):
					count=count+1
				if(file.endswith('_Visits.txt')):
					with open(latest_file+'/'+file,'r') as f1:
						col_data=(f1.readlines()[:2][1].split('|')[21])
				elif(file.endswith('_Encounters.txt')):
					with open(latest_file+'/'+file,'r') as f1:
						col_data=(f1.readlines()[:2][1].split('|')[26])		
if((count==17 and sys.argv[1].split('/')[1].title()=='Clinical') or (count==3 and sys.argv[1].split('/')[1].title()=='Financial')):
	print 'Everything Fine According To Optum,\nFile_count:'+str(count)
	s=str(col_data)
	osler_site_name=re.sub(r'\[|\]|\'|\\n|\"|\s|\.','',s)
	print 'Site_name:'+osler_site_name

	def yes_or_no(question):
		reply = str(raw_input(question+'[Y/N]: ')).lower().strip()
		if reply== 'y':
			def upload(path):
				s=pysftp.Connection('52.34.114.56',username='optum',password='Optum2017#')
				optum_file=s.listdir(path)
				for optum_site_name in optum_file:
					if(optum_site_name==osler_site_name):
						optum_path=path+optum_site_name+'/'+sys.argv[1].split('/')[1]
						# print Optum_Path
						for root, dirs, files in os.walk(latest_file):
							for file in files:
								if (file.endswith('.txt')):
									if len(s.listdir(optum_path))!=0:
										print "File Already there"
										exit()
									else:
										print 'pra'	
									#s.put(osler_site_name+'/'+file,optum_path+'/'+file)

						optum_uploaded_file=s.listdir(optum_path)
						print str(len(optum_uploaded_file))+' File Upload Successfully'

				s.close
			upload(open('config.csv','r').readlines()[:3][2])
		elif reply== 'n':
			exit()
		else:
	    	 print 'Invalid Input'
	yes_or_no('Do You Want To Upload on Optum')

else:
	print 'check it Again!!Not According To Optum\nFile_count:'+str(count)
