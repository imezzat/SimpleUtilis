import os
import re
import xlsxwriter
import itertools
import time
import traceback

print ('This simple Script searches for regex in the files contained within its directory (and subdirectories) and outputs the result in excel sheet \
(matches in each file as well as the unique matches in all of files) \n')

file_type = input("Please enter extensions for target files seperated by commas (Use empty string  if y'd like to search all file types) : ").split(',')
regex = input("\nPlease enter Regex or press Enter for default regex:")
if regex=='':
   regex='HKM_SwReq_[0-9]+|SwReq_Error_Handling[0-9]+'
print('Regex to be searched for '+ regex)

TG_ReqKeys= dict()
for root, dirs, files in os.walk(str(os.path.dirname(os.path.realpath(__file__)))):
   for file in files:
      path_file = os.path.join(root,file)
      if file_type and not file.endswith(tuple(file_type)):
             continue
      fo=open(path_file)
      print(file)
      try:
          trim = re.findall(regex, fo.read(), re.DOTALL)
          unique_list=list(set(trim))
          if unique_list:
              TG_ReqKeys[file]=unique_list
      except Exception:
         print(traceback.format_exc())
      fo.close()

print(TG_ReqKeys)
workbook = xlsxwriter.Workbook(str(os.path.dirname(os.path.realpath(__file__)))+'//TG_ReqKeys '+time.strftime("%Y_%m_%d")+'.xlsx')
worksheet = workbook.add_worksheet("Sheet_1")
text_format = workbook.add_format({'text_wrap': True})
worksheet.write(0, 0, 'TG')
worksheet.write(0, 1, 'ReqKeys')
worksheet.write(0, 2, 'NumberOfReqsinTG')
worksheet.write(0,3,'ALLReqsWithDuplicatesRemoved')
row=1
def init(worksheet,header_format):
    worksheet.freeze_panes(1, 1)
    worksheet.write(0,0,'TGs',header_format)
    worksheet.write(0,1,'ReqKeys',header_format)
    worksheet.write(0,2,'NoOfReqsInTG',header_format)
    worksheet.write(0, 3, 'UniqueReqIDs', header_format)
    worksheet.set_column(0, 0 ,50)
    worksheet.set_column(1, 1, 30)
    worksheet.set_column(2, 2, 30)
    worksheet.set_column(3, 3, 30)
    return
def merge_fill_TGs_count(worksheet, TGsColumn, ReqCountColumn, row, start, dictionary, merge_format):
    for item in dictionary:
        worksheet.write(row, TGsColumn, item,merge_format)
        if len(dictionary[item])>1:
           worksheet.merge_range(start, TGsColumn, start + len(dictionary[item]) - 1, TGsColumn, item, merge_format)
           worksheet.merge_range(start, ReqCountColumn, start + len(dictionary[item]) - 1, ReqCountColumn, item, merge_format)
        worksheet.write(row, ReqCountColumn, len(dictionary[item]), merge_format)
        start += len(dictionary[item])
        row += len(dictionary[item])
        #print(len(dictionary[item]))
    return
def fill_in_column(worksheet, Column, row, list, useLastElementFormat,last_elemnt_format):
        for x in list:
            worksheet.write(row, Column, x)
            if  useLastElementFormat:
                if x == list[-1]:
                    worksheet.write(row, Column, x, last_elemnt_format)
            row += 1
        return
merge_format = workbook.add_format({
    'align':    'center',
    'valign':   'vcenter',
    'bottom':6,
    'bottom_color':'#000000'
})
header_format = workbook.add_format({
   'align':    'center',
   'valign':   'vcenter',
   'fg_color':'#400f0d',
   'color':'white',
   'bottom':6,
   'bottom_color':'#400f0d'
})
last_elemnt_format = workbook.add_format({
    'bottom':6,
    'bottom_color':'#000000'
})
TGsColumn=0;ReqCountColumn=2;row=1;start=1
ReqKeys_in_TGs_Column=1;unique_ReqKeys_Column=3;accumulated_length=0

init(worksheet,header_format)

merge_fill_TGs_count(worksheet,TGsColumn,ReqCountColumn,row,start,TG_ReqKeys,merge_format)

for key in TG_ReqKeys:
    fill_in_column(worksheet,ReqKeys_in_TGs_Column,row+accumulated_length,TG_ReqKeys[key],True,last_elemnt_format)
    accumulated_length+=len(TG_ReqKeys[key])
ALLReqs=[]

for key in TG_ReqKeys:
    ALLReqs.append(TG_ReqKeys[key])
row=1
lst=list(itertools.chain.from_iterable(ALLReqs))
uniquelist=list(set(lst))
uniquelist.sort()
fill_in_column(worksheet,unique_ReqKeys_Column,row,uniquelist,False,last_elemnt_format)
workbook.close()
