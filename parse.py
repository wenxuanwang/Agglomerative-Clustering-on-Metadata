#Expected input format
#unique ID | Permissions | UID | GID | File_size_in_bytes | Creation_time | Modification_time | Block_size_in_bytes | /path/to/file
#0             1            2     3              4             5                6                    7                      8

'''
avani@edmond:~/ian_cluster/hotstor13-cluster_analysis/src$ head
data/anon-gnfs-fs1.txt
12212963|-rw-r--r--|0|0|11676|2007-12-15 10:43:53.000000|2011-04-07 03:13:44.000000|262144| /0/1/2/3/4/5/6/7/8/9 
'''

import datetime
from collections import namedtuple
def parser(path, t=''):
  #open up the snapshot file
  FILE=open(path,'r')
  file_dict={}
  for line in FILE:
    #skip empty lines
    if line=="":
      continue
    bad_lines = 0
    line_split=line.strip().split("|")
    if len(line_split) != 9:
      print '*',
      bad_lines += 1
      continue
    #extract the filepath/name
    name=int(line_split[0])
    #load up the medata data dictionary
    metadata_dict={}
    metadata_dict["file_id"]=int(line_split[0])
    metadata_dict["permissions"]=line_split[1]
    metadata_dict["user_id"]=int(line_split[2])
    metadata_dict["group_id"]=int(line_split[3])
    metadata_dict["size_in_bytes"]=int(line_split[4])

    epoch_create_time=convert_to_epoch_time(line_split[5])
    epoch_mod_time=convert_to_epoch_time(line_split[6])

    metadata_dict["creation_time"]=epoch_create_time
    metadata_dict["modification_time"]=epoch_mod_time
    metadata_dict["block_size_in_bytes"]=int(line_split[7])
    metadata_dict["path_to_file"]=line_split[8].rstrip()
    if t!= '':
      # t is a namedtuple
      file_dict[name]=t(modification_time=epoch_mod_time,user_id=metadata_dict['user_id'],file_id=metadata_dict['file_id'],block_size_in_bytes=metadata_dict['block_size_in_bytes'],path_to_file=metadata_dict['path_to_file'],size_in_bytes=metadata_dict['size_in_bytes'],group_id=metadata_dict['group_id'],creation_time=metadata_dict['creation_time'],permissions=metadata_dict['permissions'])
     # LANL=namedtuple('LANL','modification_time user_id file_id block_size_in_bytes path_to_file size_in_bytes group_id creation_time permissions')
    else:
      #put the dictionary in, indexed by the unique ID
      file_dict[name]=metadata_dict
  return file_dict

def convert_to_epoch_time(time_string):#{{{

  #break into constituent elements
  time_string_split=time_string.split(" ")

  year_element_string=time_string_split[0]
  time_of_day_string=time_string_split[1]

  year_date_split=year_element_string.split("-")
  time_of_day_split=time_of_day_string.split(":")

  year=int(year_date_split[0])
  month=int(year_date_split[1])
  day=int(year_date_split[2])
  hour=int(time_of_day_split[0])
  minute=int(time_of_day_split[1])
  second_subsplit=time_of_day_split[1].split(".")
  second=int(second_subsplit[0])

  #datetime for calculating time since unix epoch
  initial_datetime=datetime.datetime(year,month,day,hour,minute,second)
  epoch_start=datetime.datetime(1970,1,1)

  #create the delta and return it as seconds
  epoch=(initial_datetime-epoch_start).total_seconds()

  return epoch#}}}

if __name__ == "__main__":
  snapshot_path="anon-lnfs-fs6.txt"
  file_dict=parser(snapshot_path)

