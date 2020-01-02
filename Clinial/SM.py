#!/usr/bin/env python
# -*- coding:utf-8 -*-


import sys,os
import argparse
import commands
import time
import glob
from qywx_monitor import machineaddress
from qywx_monitor import sendqiyeweixin

machineaddress = machineaddress
def sendweixin(message,addresslist):
        weixin_path = '/GPFS01/softwares/WeixinBot/wxbot_project_py2.7/tmp_data/'
        cmd = 'wxext.py {0}/Pickle/GroupList.pkl'.format(weixin_path)
        os.system(cmd)
        #obtain uuid
        uuid_lis = []
        print(addresslist)
        for i in open('%s/Pickle/GroupList.csv'%weixin_path):
                j = i.rstrip().split(',')
                print(j[5])
                if j[5] in addresslist:
                        uuid_lis.append(j[0])
        print(uuid_lis)
        #obtain Log File
        N_lis = []
        for f in glob.glob('%s/Logs/*'):
                if 'log' in f:
                        f = i.split('/')[-1].split('.')[-1]
                        N_lis.append(f)
                else:
                        pass
        if N_lis:
                N_sort_lis = sorted(list(map(int,N_lis)),reverse=False)
                N = N_sort_lis[-1]+1
        else:
                N = 1
        print(N)
        if len(uuid_lis) ==1:
                cmd2 = "wget 'http://127.0.0.1:8080/send_msg/%s/%s' -O %s/Logs/log.%s"%(uuid_lis[0],message,weixin_path,N)
                os.system(cmd2)
        else:
                for u in uuid_lis:
                        N = N+1
                        cmd2 = "wget 'http://127.0.0.1:8080/send_msg/%s/%s' -O %s/Logs/log.%s"%(u,message,weixin_path,N)
                        os.system(cmd2)

def logwrite(folder, foldername, machineid, cycle_min, cycle_max, stop_file, complete=True):
    if complete:
        sys.stderr.write("{} cycles sync complete!\nDate:{}\n\n".format(cycle_max, time.strftime("%Y-%m-%d %H:%M:%S")))
        try:
            os.remove("{}/Filesync_Not_Complete_new.txt".format(folder))
        except:
            pass
        try:
            open("{}/Filesync_Complete_new.txt".format(folder), 'w').write("Process:{0}\n{1} cycle files sync complete!\nDate:{2}\n".format(os.getpid(), cycle_min, time.strftime("%Y-%m-%d %H:%M:%S")))
        except:
            pass
    else:
        sys.stderr.write("File sync cycles: \nmix: {0}\tmax:{1}.\n{2}\nFile not exists.\nDate:{3}\n\n".format(cycle_min, cycle_max, stop_file, time.strftime("%Y-%m-%d %H:%M:%S")))
        try:
            os.remove("{}/Filesync_Complete_new.txt".format(folder))
        except:
            pass
        try:
            open("{}/Filesync_Not_Complete_new.txt".format(folder),'w').write("Process: {0}\nFile sync cycles:\nmin: {1}\tmax: {2}.\n{3} \nfile not exists.\nDate:{4}\n".format(os.getpid(), cycle_min, cycle_max, stop_file, time.strftime("%Y-%m-%d %H:%M:%S")))
        except:
            pass

def runinfo_parser(runinfofile):
	machinedict = {"E00516":"X1","E00515":"X2","E00514":"X3","E00517":"X4","E00499":"X5",
	               "K00141":"4k1","K00422":"4k2","K00167":"4k3",
	               "E00572":"YZ1","E00591":"YZ2", "ST-E00578":"YZ3","ST-E00575":"YZ4",
	               "M02274":"miseq1","M03014":"miseq2","M05093":"miseq3","M05081":"miseq4",
	               "C70117":"miseq_dx1","C70114":"miseq_dx2","C70116":"miseq_dx3","C70141":"miseq_dx5","C70140":"miseq_dx6","C70159":"miseq_dx7","C70182":"miseq_dx8","C70193":"miseq_dx9","C70186":"miseq_dx10","C70187":"miseq_dx11","C70283":"miseq_dx12","C70280":"miseq_dx13",
		       "NDX550219":"nexseq1"
	               }
	try:
		import xml.etree.cElementTree as ET
	except ImportError:
		import xml.etree.ElementTree as ET
	tree = ET.ElementTree(file=runinfofile)
	root = tree.getroot()
	run = root.getchildren()[0]
	runid = run.attrib["Id"]
	flowcell = runid.split('_')[-1][0]
	Date,machineid = runid.split('_')[:2]
	machine = machinedict[machineid]
	reads_len=[]
	for read in run.find("Reads"):
		reads_len.append(int(read.attrib['NumCycles']))
	return runid,machine,flowcell,Date,reads_len

def bcl_check(start,end,read_len):
	total_cycle = sum(read_len)
	cycle_num = commands.getoutput('ls Data/Intensities/BaseCalls/L001/C*.1| grep : | cut -f 1 -d :').rstrip().split('\n')
	cycle_len = [None]*total_cycle
	for num,cycle in enumerate(cycle_num):
		cycle_file_num = commands.getoutput('ls {} | wc -l'.format(cycle)).rstrip().split('\n')
		cycle_len[num]=cycle_file_num[0]
	return cycle_len
def image_check(start,end,read_len):
	total_cycle = sum(read_len)
	image_cycle_num = commands.getoutput('ls Thumbnail_Images/L001/C*.1| grep : | cut -f 1 -d :').rstrip().split('\n')
	image_cycle_len = [None] *total_cycle
	for num, image_cycle in enumerate(image_cycle_num):
		image_cycle_file_num = commands.getoutput('ls {} | wc -l '.format(image_cycle)).rstrip().split('\n')
		image_cycle_len[num]=image_cycle_file_num[0]
	return image_cycle_len

def infofile_check(read_len):
	infofiles = ["Basecalling_Netcopy_complete_Read{}.txt".format(x) for x in range(1,len(read_len)+1)]
	infofiles.extend(["ImageAnalysis_Netcopy_complete_Read{}.txt".format(y) for y in range(1,len(read_len)+1)])
	infofiles.extend(["InterOp/ControlMetricsOut.bin", 
#"InterOp/IndexMetricsOut.bin",
 				"InterOp/TileMetricsOut.bin", "InterOp/CorrectedIntMetricsOut.bin", "InterOp/ExtractionMetricsOut.bin", "InterOp/QMetricsOut.bin", "RTAComplete.txt", "RunInfo.xml", "runParameters.xml"])
	info_not_exist = None
	for n in infofiles:
		if not os.path.exists(n):
			print "{0} is not exists!".format(n)
			info_not_exist = n
	return info_not_exist

def filecheck(start,end,reads_len,checklist):
	sys.stderr.write("FileSync function Started!\nStart Cycle:{},End Cycle:{}\n".format(start,end))
	check_result = ["Done"] *3
	if checklist[0]:
		bcl_result = bcl_check(start,end,reads_len)
		if len(list(set(bcl_result))) == 1 and list(set(bcl_result)) != [None]:
			check_result[0] = True
	if checklist[1]:
		image_result = image_check(start,end,reads_len)
#		print image_result
		if len(list(set(image_result))) ==1 and list(set(image_result)) != [None]:
			check_result[1] = True
	if checklist[2]:
		infofile_result = infofile_check(reads_len)
		print infofile_result
		if infofile_result == None:
			check_result[2] = True
	return check_result
	
def folder_moniter(workfolder,check_image):
	bioinfo=["MonitorBioinformatics"]
	mailto=["MonitorBioinformatics","MonitorSequencing"]
	workfolder = os.path.abspath(workfolder)
	os.chdir(workfolder)
	runinfofile ="{0}/RunInfo.xml".format(workfolder)
	runid,machine,flowcell,Date,reads_len = runinfo_parser(runinfofile) # machine is like miseq1, miseq2
	folder_runid = ""
	print machine
	for n in workfolder.split('/'):
		if n.count('_')>=3:
			folder_runid=n
	if "miseq" in machine:
		address = machineaddress["miseq"]
	elif "nexseq" in machine:
		address = machineaddress["nextseq"]
	else:
		address = machineaddress["Other"]
	address_sequencing = machineaddress["Sequencer"]
	if runid not in folder_runid:
		message="Sync ERROR|Runinfo:{}|Folder:{}".format(runid,folder_runid)
		#sendweixin(message,bioinfo)
		sendqiyeweixin(message,address)
		sys.exit()
	total_cycle = sum(reads_len)

	mailmessage="SyncStart|{0}|{1}|{2}".format(machine,runid,os.getpid())
	#sendweixin(mailmessage,bioinfo)
	sendqiyeweixin(mailmessage, address)
	if check_image:
		checklist = [True,True,True]
	else:
		checklist = [True,False,True]
	sys.stderr.write(mailmessage+"\n"+"Check bcl:{0}, Check Image:{1}, Check inforfile:{2}\n".format(*checklist))
	start = 1
	end = total_cycle
	
	while True:
		check_result = filecheck(start, end, reads_len, checklist[:])
		if False not in check_result and "Done" not in check_result:
			message_com = "SyncComplete|{}|{}|{}".format(machine, runid, os.getpid())
			try:
				#sendweixin(message_com,mailto)
				sendqiyeweixin(message_com,address)
				sendqiyeweixin(message_com,address_sequencing)
			except:
				pass
			logwrite(workfolder, runid, machine, total_cycle, total_cycle, "", complete=True)
			break
		logwrite(workfolder, runid, machine, total_cycle, total_cycle, "", complete=False)
		time.sleep(10)
	SampleSheetName = os.path.basename(workfolder) + '.csv'
        os.system("cp /GPFS01/Tranfer/001Bioinfomatics/5-SampleSheet/{SampleSheetName} {workfolder}".format(SampleSheetName=SampleSheetName,workfolder=workfolder))
        os.system("cp /GPFS01/Tranfer/001Bioinfomatics/5-SampleSheet/{SampleSheetName} {workfolder}/SampleSheet_new.csv".format(SampleSheetName=SampleSheetName,workfolder=workfolder))

		
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Miseq_Sequence Folder Sync Complete Check")
	parser.add_argument("-f","--folder",type=str,default='.',help='Folder path,default current folder')
	parser.add_argument("-c","--check_image",default=True,help='Check image files,default Yes')
	args = parser.parse_args()
	folder_moniter(args.folder,args.check_image)
