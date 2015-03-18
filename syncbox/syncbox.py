import os
import shutil

def should_be_copied(source_file, dest_file):
	if '.lnk' in source_file:
		return False
	if os.path.exists(dest_file) and os.path.getmtime(dest_file) >= os.path.getmtime(source_file):
		return False
	else:
		return True


def sync_and_backup(source_dir, dest_dir):

	if not os.path.exists(dest_dir):
		os.mkdir(dest_dir)

	filenames = os.listdir(source_dir)
	files_copied_count = 0
	for filename in filenames:
		file_to_copy = os.path.join(source_dir, filename)
		copy_to_file = os.path.join(dest_dir, filename)

		if os.path.isdir(file_to_copy):
			files_copied_count +=  sync_and_backup(file_to_copy, copy_to_file)
		else:
			if should_be_copied(file_to_copy, copy_to_file):
				shutil.copy2(file_to_copy, copy_to_file)
				print 'copied %s => %s' % (file_to_copy, copy_to_file)
				files_copied_count += 1
	return files_copied_count

if __name__ == '__main__':
	source_dir = r'C:\Drivers'
	dest_dir = r'C:\Users\Meng\Desktop\test'
	files_copied_count = sync_and_backup(source_dir, dest_dir)
	print 'copied %d files' % files_copied_count
				
				


