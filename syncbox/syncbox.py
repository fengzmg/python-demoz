import os
import shutil

def should_be_copied(source_file, dest_file):
	if '.lnk' in source_file:
		return False
	if os.path.exists(dest_file) and os.path.getmtime(dest_file) >= os.path.getmtime(source_file):
		return False
	else:
		return True

def backup(source_dir, dest_dir):
	if not os.path.exists(dest_dir):
		os.mkdir(dest_dir)
	filenames = os.listdir(source_dir)
	files_copied_count = 0
	for filename in filenames:
		file_to_copy = os.path.join(source_dir, filename)
		copy_to_file = os.path.join(dest_dir, filename)

		if os.path.isdir(file_to_copy):
			files_copied_count +=  backup(file_to_copy, copy_to_file)
		else:
			if should_be_copied(file_to_copy, copy_to_file):
				shutil.copy2(file_to_copy, copy_to_file)
				print 'copied %s => %s' % (file_to_copy, copy_to_file)
				files_copied_count += 1
	return files_copied_count

def clean_obseleted_files(source_dir, dest_dir):
	"""cleanup the obseleted files from dest_dir
	"""
	filenames = os.listdir(dest_dir)
	files_removed_count = 0

	for filename in filenames:
		file_at_dest = os.path.join(dest_dir, filename)
		file_at_source = os.path.join(source_dir, filename)

		if os.path.isdir(file_at_dest):
			if not os.path.exists(file_at_source):
				shutil.rmtree(file_at_dest)
				print 'removed dir %s' % file_at_dest
			else:	
				clean_obseleted_files(file_at_source, file_at_dest)
		else:
			if not os.path.exists(file_at_source):
				os.remove(file_at_dest)
				print 'removed file %s' % file_at_dest

def sync_and_backup(source_dir, dest_dir):
	files_copied_count = backup(source_dir, dest_dir)
	print 'copied %d files' % files_copied_count
	clean_obseleted_files(source_dir, dest_dir)

if __name__ == '__main__':
	source_dir = r'C:\Drivers\network'
	dest_dir = r'C:\Users\Meng\Desktop\test'
	sync_and_backup(source_dir, dest_dir)
	
				
				


