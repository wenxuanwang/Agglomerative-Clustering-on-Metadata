import sys
from parse import parser
from collections import Counter,defaultdict
import numpy as np
def get_unique_items(file_dict,index):#{{{
  '''
  Returns a count of the number of occurences of each unique file in the
  trace
  '''
  counts = Counter()
  for f in file_dict:
    counts[file_dict[f][index]] += 1

  for f in counts:
    if counts[f] > 1:
      print f,':',counts[f],' ',
  return counts#}}}

def get_directory_groups(file_dict,level=-1,print_sizes=True):
  '''
  Returns groups of fids based on the specified directory level.  For directory
  0/1/2/3/4/5/6 , a level 0f -1 corresponds to 6, and a level of <= -7
  corresponds to 0
  '''
  directory_dict = defaultdict(list)
  print 'Level: ',level
  for f in file_dict:
    path = file_dict[f]['path_to_file'].strip()
    d = path.split('/')[1:] # The paths start with a leading '/'
    if len(d)<abs(level):
      level = 0
    directory_dict[d[level]].append(f)

  if print_sizes:
    ones = 0
    counts = defaultdict(list)
    for element in directory_dict:
      l = len(directory_dict[element])
      if l != 1:
        counts[l].append(element)
      else:
        ones += 1
    #for l in counts:
    #  print l,':',counts[l]
    print 'x:y  y directories at the specified level each contained x of our files'
    if ones != 0: 
      print '1:',ones,' ',
    for l in counts:
      print l,':',len(counts[l]),' ',
  return directory_dict

def discretize(file_dict):
  out = []
  for entry in file_dict.keys():
    parentdir=entry['path_to_file'].split('/')[-1]
    l = [entry['modification_time'],entry['user_id'],entry['file_id'],entry['block_size_in_bytes'],entry['group_id'],entry['creation_time']]
    # throwing away path and permissions
  out.append(l)
  return np.array(out)
    

if __name__ == '__main__':
  #arg parsing
  fn = ''#{{{
  exp = ''
  for i,arg in enumerate(sys.argv):
    if arg == '-f':
      fn = sys.argv[i+1]
    elif arg == '-exp':
      exp = sys.argv[i+1]

  if fn == '':
    print 'Please specify a data file'
    sys.exit(1)
  if exp == '':
    print "You're very dull"
    sys.exit(1)#}}}
 
  file_dict=parser(fn)
  '''
  
  Format: 
  {file_id:{'modification_time': 1231285728.0, 'user_id': 0, 'file_id': 5030,
  'block_size_in_bytes': 524288, 'path_to_file': ' /0/1/2/3/4/5/6/7/8/9',
  'size_in_bytes': 1000, 'group_id': 0, 'creation_time': 1231285728.0,
  'permissions': '-rwxrwxr--'}...}

  '''
  
  if exp == 'unique-fid':
    get_unique_items(file_dict,'file_id')
  elif exp == 'unique-uid':
    get_unique_items(file_dict,'user_id')
  elif exp == 'unique-gid':
    get_unique_items(file_dict,'group_id')
  elif exp.startswith('dir-'):
    get_directory_groups(file_dict,-int(exp.split('-')[1]))

