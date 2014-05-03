import os
import datetime
from subprocess import Popen, PIPE, call
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto

# config
AWS_KEY 	= "YOU-AMAZON-AWS-KEY"
AWS_SECRET 	= "YOU-AMAZON-AWS-SECRET"
BUCKET = 'you-bucket'
DATABASES 	= [('database1', 'user_database1', 'password_database1'), 
			   ('database2', 'user_database2', 'password_database2')]

def divisor():
	print ''
	print '- - - - - - - - - - - - - - - - - - - - - - - - - - - - '
	print ''


# get current time
time = datetime.datetime.utcnow().isoformat()+ "Z"
time = str(time).replace(':', '.')	

# folder
dt = datetime.date.today()
tf = str(dt.year)+'-'+str(dt.month)
path_base = os.path.join(os.getcwd(), 'dumps', tf)

#create dir to storage dumps
call(['mkdir', '-p', path_base])

for i in DATABASES:
	database = i[0]
	user = i[1]
	password =  i[2]
	dump_name = database+'-'+time+'.sql.gz'
	file_name = os.path.join(path_base, dump_name)
	
	divisor()

	print 'Dump from: '+database
	
	
	#  mysqldump
	f = open(file_name, 'w+')
	
	p1_args = ['mysqldump', '-h', 'localhost', '-u', user, '-p'+password, database]
	pipe1 = Popen(p1_args, stdout=PIPE)
	
	p2_args = ['gzip', '-9']
	pipe2 = Popen(p2_args, stdin=pipe1.stdout, stdout=f)

	pipe2.wait()
	pipe1.wait()
	


	print '\t - Create: '+file_name



	# Send to amazon s3
	print '\t- Send to AmazonS3 - Bucket:'+BUCKET
	s3Connection = S3Connection(AWS_KEY, AWS_SECRET)
	s3Bucket = s3Connection.get_bucket(BUCKET)
	s3BucketObject = s3Bucket.new_key(s3Bucket)
	s3BucketObject.name = dump_name
	s3BucketObject.set_contents_from_filename('kohana-3.3.2.zip')
	s3Connection.close()






	
