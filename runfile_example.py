# -*- coding: utf-8 -*-
"""
@author: Florian Mahiddini - EIGSI - mahiddini@eigsi.fr
@date: July 2024
@version: 0.4 

Runfile example

Licensed under the GNU General Public License v3.0
"""
import lychrel_tools as lt
import csv
import os

##**********************************************************************************
result_path = './results/'
isExist = os.path.exists(result_path)
if not isExist:
    os.makedirs(result_path)

##**********************************************************************************
## Lists all Lychrel candidates for the first 10000 integers in base systems 10
## and 16. The number is considered a Lychrel candidate when no palindrome is
## found in the sequence of reverse-and-add operations after the stopping 
## criterion has been reached (here set with 'iter_depth' variable)
## The outcomes are stored in a list nested in a dictionary.
## lychrel_candidates['10'] will return the list of Lychrel candidates found in
## the base system 10   

lychrel_candidates = {}
#for base in range(10,17):
for base in [10,16]:
    print('** PROCESSING BASE {}\n'.format(base))
    seeds = lt.init_seeds('1', base, nb_iter = 10000)
    lychrel_candidates[str(base)] = lt.search_lychrel(seeds, iter_depth = 500)

# print outcomes
print('\n***Lychrel candidates in base 10 ****\n', lychrel_candidates['10'])
print('\n***Lychrel candidates in base 16 ****\n', lychrel_candidates['16'])
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
print('\n*** Generated thread for 196 in base 16')
for thread in lt.thread_lychrel(base16_number2):
      print(thread)
# --
print('\n*** Generated thread for 196 in base 10')
for thread in lt.thread_lychrel(base10_number, iter_depth=40):
      print(thread)

##**********************************************************************************
## Save sequence in ASCII and export thread as a Graph in GRAPHML format
# Example 1:
# Save threads in ASCII and .graphml for the first 1000 natural numbers 
# expressed in base systems 2 to 10
for base in range(2,11):
    print('\n** PROCESSING BASE {}\n'.format(base))
    seeds = lt.init_seeds('1', base, nb_iter = 10000)
    filename_seq = result_path + 'seq_10000_base_{}.txt'.format(base)
    lt.save_sequence_ascii(filename_seq, seeds, iter_depth = 300)
    graph_filename = result_path + 'seq_10000_base_{}.graphml'.format(base)
    lt.export_graph(filename_seq, graph_filename)

# Example 2:
# Save thread for natural number 196 expressed in base sytem 10.
# 196 is known as a serious Lychrel candidate
# Maximum iterations: 5000
for base in range(10,11):
    print('\n** PROCESSING BASE {}\n'.format(base))
    seed = lt.init_seeds('196', base=10, nb_iter = 0) # selecting a unique seed (196 in base 10)
    max_iter = 5000
    filename_seq = result_path + 'seq_196_{}iterations_base_{}.txt'.format(max_iter, base)
    lt.save_sequence_ascii(filename_seq, seed, iter_depth = max_iter)
    graph_filename = result_path + 'seq_196_{}iterations_base_{}.graphml'.format(max_iter, base)
    lt.export_graph(filename_seq, graph_filename)

#**********************************************************************************
## Lists all Lychrel candidates for the first natural numbers of 5 digits in
# specified bases. Save list of Lychrel candidates in ASCII file
# Create csv file with Lychrel candidates density vs base systems 
lychrel_candidates = {}
lychrel_density = []
for base in range(2,11):
    print('** PROCESSING BASE {}\n'.format(base))
    seeds = lt.init_seeds('1', base, limit_digits = 6)
    lychrel_candidates[str(base)] = lt.search_lychrel(seeds, iter_depth = 500)
    filename= result_path + 'lychrel_candidates_1_digits_max_integers_base2_10_iterdepth500.txt'
    lt.print_list_in_ASCII(filename, {str(base): lychrel_candidates[str(base)]}, mode='a')
    lychrel_density.append((base,len(lychrel_candidates[str(base)])))

csv_filename = result_path + 'density_5digits_base_2_10.csv'
with open(csv_filename,'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['Base','Number of Lychrel candidates'])
    csv_out.writerows(lychrel_density)
##**********************************************************************************

