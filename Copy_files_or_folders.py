import shutil, os
def copy_folders(src,dist):
	shutil.copytree(src,dist)
def copy_files(src,dist):
	shutil.copy2(src,dist)
print('This simple Script copies a list of files/folders seperated by commas from one directory to another')

files_folders = input("\nPlease specify if you'd like to copy files or folders (1/2):")
src_directory=input("\nPlease Enter Src Directory :")
dist_directory=input("\nPlease Enter Dist Directory :")
list_of_files_folders=list(input("\nPlease Enter the list of files/folders separated by commas :").split(','))
for i in list_of_files_folders:
	print (i)
	if files_folders=='1':
	   if not os.path.exists(dist_directory):
			   os.makedirs(dist_directory)
	   print('\n'+src_directory+'//'+i.lstrip().rstrip()+'\n')
	   copy_files(src_directory+'//'+i.lstrip().rstrip(), dist_directory)
	if files_folders=='2':
	   copy_folders(src_directory+'//'+i.lstrip().rstrip(), dist_directory+'//'+i.lstrip().rstrip())
	print('\ncopied')
