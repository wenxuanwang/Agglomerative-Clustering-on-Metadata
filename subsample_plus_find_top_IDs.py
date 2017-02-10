"""
Used to produce histogram plots of popularity distributoins
"""
import sys
import parse
#import matplotlib.pyplot as plt
#from matplotlib import cm
from lanl_stats import get_unique_items

def top_id(file_dict,t,num):
  counts = get_unique_items(file_dict,t)
  # Make a list of the thingies that are popular enough to matter
  return [x[0] for x in sorted(counts.items(),key=lambda i: i[1])[-num:]]

def make_scatter(x_list,y_list,t_list,x_field,y_field,t_field,num):
  xLabelVis=True
  yLabelVis=True
  titleVis=True
  automaticXLimit=True
  automaticYLimit=True
  legendVis=False
  title = 'Top '+str(num)+' instances of '+str(t_field)+' w.r.t. '+str(x_field)+' and '+str(y_field)
  
  #Marker size-Must be float
  marker_size=8.0

  fig = plt.figure()
  ax = fig.add_subplot(111)
  
  colMark = 'mo'
  ax.scatter(x_list,y_list,colMark,c=t_list,cmap=cm.PuRd)
  
  ax.get_xaxis().set_ticks([])
  ax.get_yaxis().set_ticks([])
  if xLabelVis==True:
    ax.set_ylabel(yLabel)

  if yLabelVis==True:
    ax.set_xlabel(xLabel)
  #set title here
  if titleVis==True:
    ax.set_title(title)
  if legendVis==True:
    ax.legend()
  
  plt.show()
  print 'should be showing plot'
  raw_input()
 
  
def scatter_lanl_by_top_id(x_field, y_field, t_field, file_dict, num,gnuplot=True):
  tops = top_id(file_dict,t_field,num)
  print tops
  x_list=[]
  y_list=[]
  t_list=[]
  t_dict={'Other':num+1}
  c=1
  tot = 0
  other = 0
  out = open('gnuplot_output','w')
  for f in file_dict:
    f1 = file_dict[f][x_field]
    f2 = file_dict[f][y_field]
    x_list.append(f1)
    y_list.append(f2)
    t = file_dict[f][t_field]
    tot += 1
    if t not in tops:
      t = "Other"
      other += 1
    t_list.append(t)
    if gnuplot:
      if t in t_dict.keys():
        t = t_dict[t]
      else:
        t_dict[t] = c
        t = t_dict[t]
        c += 1
      out.write(' '.join(map(str,[f1,f2,t]))+'\n')
  print t_dict
  if not gnuplot:
    make_scatter(x_list,y_list,t_list,x_field,y_field,t_field,num)
  print other,':',tot

if __name__ == '__main__':
  # Usage:
  # Returns a csv data file with the selected field reduced to the top num
  # attributes plus an "Other" catagory.
  # Specify the --hist option to 
  # ./subsample_plus_find_top_IDs.py LANL_data_file field_to_aggregate 
  # --plot (optional: makes a colormap plot) -n number_to_select (optional: default = 30)
  #
  # Fields are: 
  #{file_id:{'modification_time': 1231285728.0, 'user_id': 0, 'file_id': 5030,
  #'block_size_in_bytes': 524288, 'path_to_file': ' /0/1/2/3/4/5/6/7/8/9',
  #'size_in_bytes': 1000, 'group_id': 0, 'creation_time': 1231285728.0,
  #'permissions': '-rwxrwxr--'}...}
  
  num = 30
  plot = False
  t=sys.argv[2]
  fd = parse.parser(sys.argv[1])
  if len(sys.argv) > 3:
    # We have optional args
    if '--plot' in sys.argv:
      plot = True
      x_field = sys.argv[sys.argv.index('--plot')+1]
      y_field = sys.argv[sys.argv.index('--plot')+2]
    if '-n' in sys.argv:
      num = int(sys.argv[sys.argv.index('-n')+1])
  print num
  if plot:
    scatter_lanl_by_top_id(x_field,y_field,t,fd,num)
  else:
    top_id(fd,t,num)


