import os
import yaml
import boto3

class FSBackup(object):

	def __init__(self, config_path):
		self.config = yaml.safe_load(open('config.yaml', 'r'))

	def get_s3_client(self):
		session = boto3.Session(profile_name=self.config['aws']['profile'])
		s3 = session.client('s3')
		return s3

	def create_bucket(self):
		s3 = self.get_s3_client()
		s3.create_bucket(
			Bucket=self.config['aws']['bucket'],
			)

	def push(self, source, destination):
		s3 = self.get_s3_client()
		bucket = self.config['aws']['bucket']
		source = os.path.expanduser(source)
		if os.path.isfile(source):
			file_path_s3 = destination
			print(f"Uploading {source} to s3://{bucket}/{file_path_s3}")
			# s3.put_object(
			# 	Bucket=bucket,
			# 	Body=open(source, 'rb').read(),
			# 	Key=file_path_s3,
			# 	)
		else:
			for root, dirs, files in os.walk(source):
				for file in files:
					file_path = os.path.expanduser(
						os.path.join(
							root, file))
					file_path_s3 = os.path.join(
						destination, file)
					print(f"Uploading {file_path} to s3://{bucket}/{file_path_s3}")
					s3.put_object(
						Bucket=bucket,
						Body=open(file_path, 'rb').read(),
						Key=file_path_s3,
						)

	def sync(self, from_localtion, to_location):
		if from_localtion == 'local':
			for entry in self.config['backups'][to_location]:
				print(f"Sync files from {from_localtion} to {to_location}")
				for entry in self.config['backups'][to_location]:
					self.push(
						entry['source'], 
						os.path.join(to_location, entry['destination']),
						)

if __name__ == '__main__':
	fsbackup = FSBackup('config.yaml')
	fsbackup.create_bucket()
	fsbackup.sync('local', 'fedora')