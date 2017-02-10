#this module takes in a list of metadata dictionaries from the parser
# and produces a data for a CDF showing the temporal distances between the specified timestamps
import math
import sys
from parse import parser

#timestamps_to_extract should be a list
#of strings that represent what timestamps we should pull out.
#must have at least one entry
#file list is a list of file metadata dictionaries
#returns a list of epoch time integers representing the timestamps
def get_timelist(timestamps_to_extract,file_list,truncate_at):
  
  time_list=[]
  
  keys=file_list.iterkeys()
  
  count=0
  for key in keys:
    
    print key
    
    if count==truncate_at:
      break
    
    count+=1
  
    metadata=file_list[key]
    
    for stamp in timestamps_to_extract:
  
      current_timestamp=metadata[stamp]
      time_list.append(current_timestamp)
      

  return time_list

def get_files(path):
  file_dict=parser(path)
  
  return file_dict

#takes the list of epoch time stamps and creates a list
#of the distance of any one stamp to all the others.
def create_inter_distance_list(time_list):
  
  inter_time_list=[]
  time_list.sort()

  for start_point in time_list:
    
    for end_point in time_list:
      
      time_diff=math.fabs(end_point-start_point)
      inter_time_list.append(time_diff)
      
  return inter_time_list
      
      
def create_cdf(inter_time_list):

  total_items=len(inter_time_list)
  inter_time_list.sort()
  
  x_list=[]
  y_list=[]
  
  cur_y_perc=0.0
  incrementer=1.0/(total_items*1.0)
  
  for inter_time in inter_time_list:  
    
    x_list.append(inter_time)
    y_list.append(cur_y_perc)
    
    cur_y_perc+=incrementer
    
    
    
    
  return x_list,y_list

    
def output_cdf(x_list,y_list,path):

  
  FILE=open(path,'w')
  
  for index in range(len(x_list)):
    
    x_pos=x_list[index]
    y_pos=y_list[index]
    
    outstring=str(x_pos)+"\t"+str(y_pos)+"\n"
    
    FILE.write(outstring)
    
  FILE.close()
  
  
if __name__ == "__main__":      
  snapshot_file_path = sys.argv[1]
  timestamps_to_get=["modification_time"]
  file_dict=get_files(snapshot_file_path)
  time_list=get_timelist(timestamps_to_get,file_dict,2000)  
  inter_time_list=create_inter_distance_list(time_list)
  x_list,y_list=create_cdf(inter_time_list)
  output_cdf(x_list,y_list,"test_out.dat")

