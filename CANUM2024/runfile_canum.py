# -*- coding: utf-8 -*-
"""
@author: Florian Mahiddini - EIGSI - mahiddini@eigsi.fr
@date: May 2024

Numerical Experiments - CANUM 2024 @ Ile de Ré

Licensed under the GNU General Public License v3.0
"""
import lychrel_tools as lt
import csv

##*******************************************************************************
## ADDITIONAL FUNCTIONS - To be implemented in lychrel_tools
##*******************************************************************************
def print_list_in_ASCII(filename, lychrel_candidates, mode ='w+'):
    """
    Saves list of Lychrel candidates in ASCII file

    Parameters
    ----------
    filename : STRING
        Name of the file where the results will be stored
    
    lychrel_candidates : DICT of LIST
        
    mode : STRING
        

    Returns
    -------
    None.

    """
    with open(filename, mode) as file:
        for base, seed_candidates in lychrel_candidates.items():
            file.write("*** Lychrel candidates in base: {}\n".format(base))
            file.write("*** Number of candidates: {}\n".format(len(seed_candidates)))
            file.write(",".join(str(seeds) for seeds in seed_candidates)+"\n")
            file.write("\n")

def new_init_seeds(start, base, **kwargs):
    """
    Create a list of unit-incremented Number instances in a specified base

    Parameters
    ----------
    start : String
        list of digits representing the number to increment
    nb_iter : Int
        Number of succesive increment from the first seed
    base : int
        base of numbers

    Returns
    -------
    seeds : List of Number instances
        
        
    Example
    -------
    init_seed('1',100,16) will return a list of 100 numbers, unit-incremented in
    base 16, eg. ['1','2', ... ,'5F','60','61','62','63','64','65']
        

    """
    seeds = [lt.Number(start, base)]
    if 'nb_iter' in kwargs.keys():
        for idx in range(1,kwargs['nb_iter']+1):
            seeds.append(lt.increment(seeds[idx-1]))
    
    
    if 'limit_digits' in kwargs.keys():
        idx = 1
        while len(seeds[idx-1].digits) < kwargs['limit_digits']:
            seeds.append(lt.increment(seeds[idx-1]))
            idx += 1
            
    if 'limit' in kwargs.keys():
        idx = 1
        while seeds[idx-1].digits != kwargs['limits']:
            seeds.append(lt.increment(seeds[idx-1]))
            idx += 1
    
    return seeds



#**********************************************************************************
# Lists all Lychrel candidates for the first 100000 integers from base systems
# 2 to 60.
lychrel_candidates = {}
lychrel_density_1 = []
for base in range(2,61):
    print('** PROCESSING BASE {}\n'.format(base))
    seeds = lt.init_seeds('1', 100000, base)
    lychrel_candidates[str(base)] = lt.search_lychrel(seeds, iter_depth = 500)
    filename='./results_canum/lychrel_candidates_100000_integers_base2_60_iterdepth500.txt'
    print_list_in_ASCII(filename, {str(base): lychrel_candidates[str(base)]}, mode='a')
    lychrel_density_1.append((base,len(lychrel_candidates[str(base)])))

with open('density_1_base_2_60.csv','w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['Base','Nuber of Lychrel candidates'])
    csv_out.writerows(lychrel_density_1)

##    You can also do csv_out.writerows(data) instead of the for loop

#print outcomes
print('\n***Lychrel candidates in base 10 ****\n', lychrel_candidates['10'])
print('\n***Lychrel candidates in base 16 ****\n', lychrel_candidates['16'])


## Lists all Lychrel candidates for the first natural numbers of 5 digits
# generate seeds with the same number of digits
lychrel_candidates = {}
lychrel_density_2 = []
for base in range(2,21):
    print('** PROCESSING BASE {}\n'.format(base))
    seeds = new_init_seeds('1', base, limit_digits = 6)
    lychrel_candidates[str(base)] = lt.search_lychrel(seeds, iter_depth = 500)
    filename='./results_canum/lychrel_candidates_1_digits_max_integers_base2_20_iterdepth500.txt'
    print_list_in_ASCII(filename, {str(base): lychrel_candidates[str(base)]}, mode='a')
    lychrel_density_2.append((base,len(lychrel_candidates[str(base)])))

with open('density_5digits_base_2_20.csv','w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['Base','Number of Lychrel candidates'])
    csv_out.writerows(lychrel_density_2)
##**********************************************************************************

