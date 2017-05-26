import os
import time
from subprocess import Popen
import schedule

source = ""
target_dir = ""
mysql_username=""
mysql_password=""
aeskey=""
remote_ssh_username=""
remote_ssh_ip=""
remote_target_dir=""

if not os.path.exists(target_dir):
	os.mkdir(target_dir)



def job():
	today = target_dir + os.sep + time.strftime('%Y%m%d')
	now = time.strftime('%H%M%S')
	target = today + os.sep + now + '.tar'
	
	if not os.path.exists(today):
		os.mkdir(today)
		print('Successfully created directory', today)

	zip_command = 'tar -cvf {0} -C  {1} .'.format(target,source)
#For live servers ( doesn't make the db read only during dump)
	#sql_dump = ("mysqldump -u {0} -p'{1}' --single-transaction --quick --lock-tables=false --all-databases > ").format(mysql_username,mysql_password)+"/tmp/"+now+"database.bak.sql"	
	sql_dump = ("mysqldump -u {0} -p'{1}' --all-databases > ").format(mysql_username,mysql_password)+"/tmp/"+now+"database.bak.sql"
	sql_zip = 'tar -r --file={0} -C {1}'.format(target,("/tmp/"+now+"database.bak.sql"),)
	encrypt = "openssl aes-128-cbc -salt -in {0} -out {1}.aes -k {2}".format(target,target,aeskey)
	ssh_command = "scp {0}.aes {1}@{2}:{3}".format(target,remote_ssh_username,remote_ssh_ip,remote_target_dir)




	print('Running:')
	if os.system(zip_command) == 0:
		print('Successfully backed files up to', target)
	if os.system(sql_dump) == 0:
		print('Successfully backed mysql')
	if os.system(sql_zip) == 0:
		print('Successfully added mysql backup to zip')
	if os.system(encrypt) == 0:
		print('encrypted backup')
	if os.system(ssh_command) == 0:
		print('file is out of here')


schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
