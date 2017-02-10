import numpy as np
import logging

# FIXME : Finish the re-write of this, and clean up some of the structured
# matlab-isms.  As it is, this currently DOES NOT WORK. DO NOT USE.
# TODO : add in support for more varied input

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
####################################################################################
# This is an implementation of the iClust algorithm from Slonim et al.
# 
# 
# Inputs 
# ---
# sim_mat      : similarity matrix over input space.  Self-similarity = 1.
# T            : Tradeoff parameter.  Smaller T values lead to more deterministic
#                clusterings
# num_clusters : Default is floor(sqrt(data_size))
# num_maxima   : # of local maxima to extract before selecting best
# 

def is_similarity_good(sim_mat):
  # Check that the similarity matrix makes sense.
  if np.any(sim_mat<0):
    # You probably don't want negative values
    logging.info('Negative elements in input matrix are undefined')
    return False
  elif not np.all(sim_mat == sim_mat.T):
    logging.info('Input matrix is not symmetric')
    return False
  # TODO: Maybe check for maximal diagnols?
  return True

def calculate_ici(init_mat,cols,priors,size,num_clusters):
  # TODO: I have no idea what this is
  ici = 0
  for i in range(int(size)):
    for j in range(num_clusters):
      if init_mat(i,j) > 0:
        ici = ici + priors(i)*init_mat(i,j)*np.log2(init_mat(i,j)/cols(j))

  return ici 

def avg_similarity(sim_mat,num_clusters,cols,init_mat,priors):
  avg_sim = 0
  for i in range(len(sim_mat)):
    for c in range(num_clusters):
      for j in range(len(sim_mat)):
        if cols(c) > 0:
          avg_sim += priors(i)*init_mat(j,c)*priors(j)*sim_mat(i,j)/cols(c)
  return avg_sim



def initialize_iclust(size,num_clusters,init_type='hard'):
  # Init type values are 'hard' and 'soft'
  init_mat = np.zeros([size,num_clusters])
  cols = np.zeros([1,num_clusters])
  
  if init_type == 'hard':
    permute = np.random.permutation(range(int(size)))
    avg_cluster_size = np.ceil(size/num_clusters)
    for i in range(num_clusters):
      r = i-1*avg_cluster_size+1
      c = min(i*avg_cluster_size,num_clusters)
      indices = permute[r:c]
      init_mat[indices,i] = 1
      cols = length(indices)/size
  
  elif init_type == 'soft':
    init_mat = np.random(size,num_clusters)
    for i in range(size):
      init_mat[i,:] = init_mat[i,:]/sum(init_mat[i,:])
    cols = sum(init_mat)/float(size)
  
  return init_mat,cols

def update_matrices(sim_mat,size,T,init_mat,cols,converge,epsilon):
  col_inv = np.linalg.inv(cols)
  old_init = init_mat #TODO deepcopy
  for i in range(int(size)):
    e1 = (2/size) * col_inv * (sim_mat[i,:] * init_mat) 
    e2 = (1/(size*size)) * col_inv * col_inv * np.linalg.diag(init_mat.T *
        (sim_mat * init_mat)).T
    e = 1/T * (e1-e2)

    init_mat[i,:] = cols * np.exp(e)
    #Now, normalize
    init_mat[i,:] = init_mat[i,:]/sum(init_mat[i,:])

    cols = sum(init_mat)/size
    col_inv = np.linalg.inv(cols)
 
 deltas.append(max(max(abs(init_mat-old_init))))
 if deltas[-2] < epsilon:
   converge = True

 return init_mat,cols,converge



def iClust_single_iteration(sim_mat,iter_count,converge... )
  while not converge:
    iter_count += 1
    if iter_count % 100 == 0:
      break
    sim_mat = update_matrices(sim_mat,



def iClust(sim_mat,num_clusters,prior_type='uniform',T = 1/30.0,num_maxima = 10):
  size = float(len(sim_mat))

  # Default to uniform priors
  priors = np.ones([1,size])/size

  epsilon = 1e-10
  
  init_mat,cols = initialize_iclust(size,num_clusters) # Default to hard
                                                       # initialization

  
  

def main():
  logging.basicConfig(level=logging.DEBUG,
                      format='%(levelname)s: %(asctime)s -- %(message)s',
                      stream=sys.stdout)
  T = 1/30
  if num_clusters == 0:  
    num_clusters = np.floor(np.sqrt(len(sim_mat)))

