#this module clusters on timestamps using my DBSCAN module
#and then takes counts of various stats within the identified clusters

import dbscan
import basic_counts
import parse
import sys

#gets basic counts of users, files and groups in the snapshot
def get_counts(file_dict):
  
  num_users=basic_counts.count_unique_users(file_dict)
  num_groups=basic_counts.count_unique_groups(file_dict)
  num_files=basic_counts.count_total_files(file_dict)

  
  return num_users,num_groups,num_files

def cluster(file_dict):
  pass

if __name__ == "__main__":
  # Usage:
  # python cluster_and_count.py <LANL_snapshot_file> DBSCAN_epsilon_value DBSCAN_n_value
  #

  if len(sys.argv) == 1:
    path_to_snapshots="/Users/ian/Desktop/datasets/lanl_fs/anon-all-fs/"
    snapshot_file_path=path_to_snapshots+"anon-lnfs-fs4.txt"
    eps=10
    n=100
  else:
    snapshot_file_path=sys.argv[1]
    eps=sys.argv[2]
    n=sys.argv[3]
  
  
  #parse the snapshot into a file dictionary
  file_dict=parse.parser(snapshot_file_path)
  
  #get overall counts
  users,groups,files=get_counts(file_dict)
  
  print "--Counts--"
  print "Users:",users
  print "Groups:",groups
  print "Files:",files
  
  #cluster
  
  #pull out the mtimes from the file_dict 
  #NOTE WE ARE TRUNCATING AT 2000 files initially
  
  keys=file_dict.iterkeys()
  
  data_list=[]
  count=0
  
  for key in keys:
  
    if count==2000:
      break
  
    metadata=file_dict[key]
    mtime=metadata["modification_time"]
    
    mytuple=(mtime,key)
    
    data_list.append(mytuple)
    
    count+=1
    
  cluster_list=dbscan.dim_1_dbscan(data_list,eps,n)
  
  running_total=0
  
  
  for cluster in cluster_list:
    running_total+=len(cluster)
    
  
  noise_files=files-running_total
    
  print "Cluster Information"
  print "Number of Clusters:",len(cluster_list)
  print "Number of Files Clustered:",running_total
  print "Number of Noise Files:",noise_files
  
  for cluster in cluster_list:
    users=set([])
    groups=set([])
    
    for entry in cluster:
      file_id=entry[1]
      file_metadata=file_dict[file_id]
      
      users.add(file_metadata["user_id"])
      groups.add(file_metadata["group_id"])
        
    print "Cluster Stats"
    print "Size:",len(cluster)
    print "Number of Users:",len(users)
    print "Number of Groups:",len(groups)
