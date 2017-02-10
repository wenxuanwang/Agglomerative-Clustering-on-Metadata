'''
Blame: avani
Various entropy calculations given a list of LANL entries.

LANL entry format: 

  ['modification_time': 1231285728.0, 'user_id': 0, 'file_id': 5030,
  'block_size_in_bytes': 524288, 'path_to_file': ' /0/1/2/3/4/5/6/7/8/9',
  'size_in_bytes': 1000, 'group_id': 0, 'creation_time': 1231285728.0,
  'permissions': '-rwxrwxr--']...}

'''
import sys
import math
from collections import namedtuple

def cast_list_of_dict_to_namedtuple(list_of_dict):
# Makes everything a named tuple so that it's easier to think about and faster.
  LANL=namedtuple('LANL','modification_time user_id file_id block_size_in_bytes path_to_file size_in_bytes group_id creation_time permissions')

  return LANL(modification_time=list_of_dict['modification_time'],user_id=list_of_dict['user_id'],file_id=list_of_dict['file_id'],block_size_in_bytes=list_of_dict['block_size_in_bytes'],path_to_file=list_of_dict['path_to_file'],size_in_bytes=list_of_dict['size_in_bytes'],group_id=list_of_dict['group_id'],creation_time=list_of_dict['creation_time'],permissions=list_of_dict['permissions'])

def calculate_sample_field_entropy(list_of_ntuples,field,exclude=['total']):
  # Either calculates the total entropy (field = 'total') or 
  # calculates the sample entropy in one field

  if field == 'total':
    entropies = []
    for f in list_of_ntuples[0]._fields:
      if f not in exclude:
        entropies.append(calculate_sample_field_entropy(list_of_ntuples,f))
    return entropies
  
  bin = [getattr(l,field) for l in list_of_ntuples]
  # We have to assume uniform likelihood here. Not ideal, but as long as we
  # mention it it should be fine.
  return uniform_entropy(bin)


def uniform_entropy(bin):
  # Returns bits of uncertainty per element assuming that the probability of
  # choosing an element from the bin is uniform.
  seen = set([])
  l_bin = float(len(bin))
  entropy = 0
  for element in bin:
    if element in seen:
      continue
    c = bin.count(element)
    entropy += ((c/l_bin)*math.log((c/l_bin),2))
    seen.add(element)
  return entropy*(-1)

def test(thingie):
  a = {'modification_time': 1231285728.0, 'user_id': 0, 'file_id': 5030, 'block_size_in_bytes': 524288, 'path_to_file': ' /0/1/2/3/4/5/6/7/8/9', 'size_in_bytes': 1000, 'group_id': 0, 'creation_time': 1231285728.0, 'permissions': '-rwxrwxr--'}
  b = {'modification_time': 1234528.0, 'user_id': 34, 'file_id': 5030, 'block_size_in_bytes': 5288, 'path_to_file': ' /0/1/2/4/5/6/7/8/9', 'size_in_bytes': 1000, 'group_id': 0, 'creation_time': 1231285728.0, 'permissions': '-rwxrwxr--'}
  if thingie == 'naming':
    print cast_list_of_dict_to_namedtuple(a)
  elif thingie == 'uniform':
    bin = [2,2,2,3]
    #bin = [3,6,2,3,7,3,4,2,1,1,1,2,2,4,23,5,2,3,6,23,-2]
    print uniform_entropy(bin)
  elif thingie == 'total':
    ca = cast_list_of_dict_to_namedtuple(a)
    cb = cast_list_of_dict_to_namedtuple(b)
    print calculate_sample_field_entropy([ca,cb],'total')

if __name__ == '__main__':
  # Just a little tester.  I expect this to be called as a module.
  test(sys.argv[1])
