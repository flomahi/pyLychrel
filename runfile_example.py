# -*- coding: utf-8 -*-
"""
@author: Florian Mahiddini - EIGSI - mahiddini@eigsi.fr
@date: Nov. 2023
@version: 0.4 

Runfile example

Licensed under the GNU General Public License v3.0
"""
import lychrel_tools as lt

##**********************************************************************************
## Lists all Lychrel candidates for the first 10000 integers from base systems
## 2 to 60. The number is considered a Lychrel candidate when no palindrome is
## found in the sequence of reverse-and-add operations after the stopping criterion
## has been reached (here set by 'iter_depth' variable)
## The outcome is stored in a list nested in a dictionary
## lychrel_candidates['4'] will return the list of Lychrel candidates found in
## the base system 4   

lychrel_candidates = {}
#for base in range(10,17):
for base in [10,16]:
    print('** PROCESSING BASE {}\n'.format(base))
    seeds = lt.init_seeds('1', 10000, base)
    lychrel_candidates[str(base)] = lt.search_lychrel(seeds, iter_depth = 500)

# print outcomes
print('\n***Lychrel candidates in base 10 ****\n', lychrel_candidates['10'])
print('\n***Lychrel candidates in base 16 ****\n', lychrel_candidates['16'])
        

##**********************************************************************************

##**********************************************************************************
## Compute threads for different versions of 196 in base systems 2, 10 and 16 

## 196 (base 10) = 11000100 (base 2)
base2_number = lt.Number('11000100',base = 2)
#--
print('\n*** Generated thread for 196 in base 2')
for thread in lt.thread_lychrel(base2_number):
      print(thread)
##

## 196 (base 10) = C4 (base 16) 
base16_number1 = lt.Number('C4', base = 16)
#--
print('\n*** Generated thread for C4 in base 16')
for thread in lt.thread_lychrel(base16_number1):
      print(thread)
##

##**** 196 expressed in base 10 and base 16
base16_number2 = lt.Number('196', base = 16)
base10_number = lt.Number('196', base = 10)
#--
print('\n*** Generated thread for 16 in base 16')
for thread in lt.thread_lychrel(base16_number2):
      print(thread)
# --
print('\n*** Generated thread for 16 in base 10')
for thread in lt.thread_lychrel(base10_number, iter_depth=40):
      print(thread)

##**********************************************************************************

##**********************************************************************************
## Save sequence in ASCII and export thread as a Graph in GRAPHML format
# Example 1: 
# Save threads in ASCII and .graphml for the first 1000 natural numbers 
# expressed in base systems 2 to 60
for base in range(2,61):
    print('\n** PROCESSING BASE {}\n'.format(base))
    seeds = lt.init_seeds('1', 10000, base)
    filename_seq = './results/seq_10000_base_{}.txt'.format(base)
    lt.save_sequence_ascii(filename_seq, seeds, iter_depth = 300)
    graph_filename = './results/seq_10000_base_{}.graphml'.format(base)
    lt.export_graph(filename_seq, graph_filename)

# Example 2: 
# Save thread for natural number 196 expressed in base sytem 10.
# 196 is known as a serious Lychrel candidate
# Maximum iterations: 5000
for base in range(10,11):
    print('\n** PROCESSING BASE {}\n'.format(base))
    seed = lt.init_seeds('196', 0, base=10) # selecting a unique seed (196 in base 10)
    max_iter = 5000
    filename_seq = './results/seq_196_{}iterations_base_{}.txt'.format(max_iter, base)
    lt.save_sequence_ascii(filename_seq, seed, iter_depth = max_iter)
    graph_filename = './results/seq_196_{}iterations_base_{}.graphml'.format(max_iter, base)
    lt.export_graph(filename_seq, graph_filename)
##**********************************************************************************