__author__ = 'Meng Feng'
import logging
import os
import datetime
import re
import sys
import time
import shutil

logger = logging.getLogger('housekeeper')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s'))
logger.addHandler(console_handler)

def print_usage():
    print """
    python housekeeper.py <args>
        housekeeping
        restore
        """


def perform_housekeeping(directories=[], age_in_secs=14*24*60*60, backup_enabled = False, backup_folder = None):
    for directory in directories:
        directory = os.path.normpath(directory)
        logger.info('housekeeping directory: %s ' % directory)
        for item in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, item)):
                perform_housekeeping([os.path.join(directory, item)], age_in_secs, backup_enabled, backup_folder)
            else:
                if os.path.getmtime(os.path.join(directory, item)) < time.time() - age_in_secs:
                    if backup_enabled:
                        dest_backup_folder = os.path.join(backup_folder, directory.split(os.path.commonprefix([directory, backup_folder]), 1)[1])
                        if not os.path.exists(dest_backup_folder):
                            os.makedirs(dest_backup_folder)
                        shutil.copy2(os.path.join(directory, item), os.path.join(dest_backup_folder, item))
                        logger.info('backed up %s => %s' % (os.path.join(directory, item), os.path.join(dest_backup_folder, item)))
                    os.remove(os.path.join(directory, item))
                    logger.info('removed %s' % os.path.join(directory, item))

def restore_from_backup(folder_to_restore = None, age_in_secs = 7*24*60*60):

    def restore_from_backup(folder_to_restore = None, age_in_secs = 7*24*60*60, base_backup_folder = None):
        if os.path.exists(folder_to_restore):
            folder_to_restore = os.path.normpath(folder_to_restore)
            logger.info('restoring directory: %s ' % folder_to_restore)
            for item in os.listdir(folder_to_restore):
                if os.path.isdir(os.path.join(folder_to_restore, item)):
                    restore_from_backup(os.path.join(folder_to_restore, item), age_in_secs, base_backup_folder)
                else:
                    if os.path.getmtime(os.path.join(folder_to_restore, item)) > time.time() - age_in_secs:
                        dest_folder = os.path.splitdrive(base_backup_folder)[0] + folder_to_restore.split(base_backup_folder, 1)[1]
                        try:
                            shutil.copy2(os.path.join(folder_to_restore, item), os.path.join(dest_folder, item))
                            os.remove(os.path.join(folder_to_restore, item))
                            logger.info('restored %s => %s' % (os.path.join(folder_to_restore, item), os.path.join(dest_folder, item)))
                        except:
                            logger.warn(e)

    restore_from_backup(folder_to_restore, age_in_secs, folder_to_restore)

if __name__ == '__main__':

    action = None
    if len(sys.argv) > 1:
        action = sys.argv[1]

        if action == 'housekeeping':
            # directories = ['/tmp/meng/scripts/input_files']
            directories = [r'C:\Temp', r'C:\tmp']
            age = 5 # in days
            backup_folder = r'C:\tmp\backup'
            #backup_folder = '/tmp/meng/backup'
            backup_enabled = False
            perform_housekeeping(directories=directories, age_in_secs=age*24*60*60, backup_enabled = backup_enabled, backup_folder = os.path.normpath(backup_folder))

        elif action == 'restore':
            age = 2 # in days
            backup_folder = r'C:\tmp\backup'
            # backup_folder = '/tmp/meng/backup'
            restore_from_backup(folder_to_restore= backup_folder, age_in_secs= age*24*60*60)

        elif action == 'help':
            print_usage()

        else:
            print "'%s' action is not supported" % action
            print_usage()
    else:
        print_usage()