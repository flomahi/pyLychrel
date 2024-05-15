# -*- coding: utf-8 -*-
"""
@author: Florian Mahiddini - EIGSI - mahiddini@eigsi.fr
@date: Nov. 2023
@version: 0.4 

Release notes: 
** Major code revision:
- new Number class
- perform the reverse-add operation with numbers from arbitrary bases
- export results in ASCII format or in a readable format with Cytoscape

Licensed under the GNU General Public License v3.0
"""

# **** PACKAGES
import networkx as nx

# **** GLOBAL VARIABLES
"""
This definition based on ASCII characters limits the pratical representation of
numbers
"""
global CHARACTERS_SET
CHARACTERS_SET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
# store the set of charcters with their respective index
global CHARACTERS_SET_DICT 
CHARACTERS_SET_DICT = dict([(value,index) for index,value 
                            in enumerate(CHARACTERS_SET)])
global MAX_BASE
MAX_BASE = len(CHARACTERS_SET)

# **** CLASS DEFINITION
class Number():
    """
    A Number object is an natural number ordered in the form of an array of  
    unique characters specified for a given base (ie from '0' to 'F' in base 16)
    
    Usage:
        n = Number('1A65',16)
        --> n.digits returns a string of digits '1A65'
        --> n.base returns the numbers base.
    """
    def __init__(self, digits, base=10):
        """
        Initializes an instance of a Number object
        
        Parameters
        ----------
        digits : STRING 
            List of digits representing the number
        base : INT 
            Base of the number system (default is 10).
        
        Returns
        ----------
        Number's instance
        
        Notes
        ----------
        - The base should be less than the predefined MAX_BASE.
        """
        
        self.digits = digits
        if base < MAX_BASE:
            self.base = base
        
    def __str__(self):
        """
        Return the digits of a Number's instance
        """
        return self.digits
    
    def is_palindrome(self):
        """
        Test whether a Number's instance is a palindrome
        
        Parameters
        ----------
        Number object
        
        Returns
        -------
        Logical Test : BOOLEAN
            True (Number's instance is a palindrome)
            False (Number's instance is not a palindrome)
        """
        # speeding up the process by checking the first and last digits
        if self.digits[0] != self.digits[-1]:
            return False
        else:
            return self.digits == self.digits[::-1]

# **** GENERIC FUNCTIONS DEFINITION

def add_single_digit(*digits):
    """
    Single digit addition (intermediate step of the reverse-and-add operation)
    The function takes an arbitrary numbers of digits and returns the sum of
    their respective positions within the CHARACTERS_SET string used to 
    represent numbers

    Parameters
    ----------
    *digits : List of characters
        digits to add

    Returns
    -------
    add_at_idx : INT
        algebric sum of digits (in base 10)
        
    Example
    -------
    add_single_digit('1','F','6') will return 1+15+6 = 22 since:
    '1' is at index 1 in CHARACTERS_SET
    'F' is at index 15 in CHARACTERS_SET
    '6' is at index 6 in CHARACTERS_SET
    
    """
    add_at_idx = 0
    for element in digits:
        add_at_idx += CHARACTERS_SET_DICT[element]
    
    return add_at_idx


def increment(number):
    """
    The function adds 1 to a Number instance in its specified base

    Parameters
    ----------
    number : Number's instance'
    
    Returns
    -------
    result : Number's instance
        unit-incremented number

    """
    # initialize new number
    numlength = len(number.digits)
    carry = '0'
    result = ['0']*(numlength + 1)
    
    # Compute the addition at the least significant digit
    add_at_zero = add_single_digit(number.digits[-1], '1')
    
    # Initialize the first addition hold
    if add_at_zero >= number.base:
        carry = '1'
        
        # Iterate through each digit of the number
        for index, value in enumerate(number.digits):
            i_index = (numlength - 1) - index # inverse index
            
            # Calculate the addition at the current index
            add_at_index = add_single_digit(number.digits[i_index],result[i_index], carry)
            
            # Adjust the result and carry if necessary
            if add_at_index >= number.base:
                result[i_index+1] = CHARACTERS_SET[add_at_index % number.base]
                result[i_index] = CHARACTERS_SET[CHARACTERS_SET_DICT[result[i_index]] + 1]
            else:
                result[i_index+1] = CHARACTERS_SET[add_at_index]
                carry = '0'
        
        # Remove leading zero if present
        if result[0] == '0':
            result.pop(0)
    else:
        # If no carry is needed, simply copy the digits and replace the last digit
        result = list(number.digits)
        result[-1] = CHARACTERS_SET[add_at_zero]
    
    # Return the result as a new Number object
    return Number(''.join(result),number.base)
    

def init_seeds(start, nb_iter, base):
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
    seeds = [Number(start, base)]
    for idx in range(1,nb_iter+1):
        seeds.append(increment(seeds[idx-1]))
    
    return seeds        


def save_sequence_ascii(filename, seeds_list,  **kwargs):
    """
    Saves full sequence of Lychrel thread in an ASCII file

    Parameters
    ----------
    filename : STRING
        Name of the file under which the sequence of threads will be stored
    seeds_list : List of Number
        Seed to be tested
    **kwargs : DICT
        Additional argument
        iter_depth: INT - stopping criteria for a sequence of reverse-and-add 
        operation 

    Returns
    -------
    None.

    """
    # Save thread in file
    with open(filename,'w+') as file:
        # GENERATE HEADER
        file.write('# MAX_ITER_DEPTH = {}\n'.format(kwargs['iter_depth']))        
        # generate thread
        for number in seeds_list:
            #print(number)
            index_iter = 1
            file.write('[ THREAD ]\n')
            file.write(number.digits)
            file.write('\n')
            for thread in thread_lychrel(number, kwargs['iter_depth']):
                index_iter += 1
                #file.write('# ITERATION {}\n'.format(index_iter))
                file.write(thread.digits)
                #print(thread.digits)
                file.write('\n')
            if index_iter < kwargs['iter_depth']:
                file.write('# Lychrel = NO\n')
                file.write('# nb_iter = {}\n'.format(index_iter))
            else:
                file.write('# Lychrel = YES\n')
                file.write('# nb_iter = MAX_ITER\n')
            file.write('\n')


def export_graph(sequence_filename, graph_filename):
    """
    Converts an ASCII thread file to GRAPHML format
    The function needs networkX to operate

    Parameters
    ----------
    sequence_filename : STRING 
        ASCII filename
    graph_filename : STRING
        GRAPHML filename

    Returns
    -------
    None.

    """
    # intialize variable
    first_node = True
    # create empty network
    thread_graph = nx.DiGraph()
    # read file
    with open(sequence_filename, 'r') as file:
        for node in file:
            # Ignore comments or empty lines if any
            if node.startswith('#') or node == '\n':
                continue
            # Initiate thread
            if node.startswith('[') and node.endswith(']\n'):
                first_node = True
                temp_node = None
                #print(node)
                continue
            else:
                # Add nodes
                if node not in thread_graph:
                    #print(node)
                    thread_graph.add_node(node)
                # Add edges
                if first_node:
                    temp_node = node
                    first_node = False
                else:
                    thread_graph.add_edge(node, temp_node)
                    temp_node = node
        
    # # write graph
    nx.write_graphml(thread_graph,graph_filename)
    #return thread_graph

    

# **** LYCHREL CONJECTURE UTILITIES
def reverse_add(number):
    """
    Performs the reverse-add operation on the instance of a number object in an
    arbitrary base
    
    Parameters
    ----------
    number : NUMBER
        
    Returns
    -------
    result : STRING

    """
    numlength = len(number.digits)
    # sets an empty string filled with '0' of length n+1
    result = ['0']*(numlength+1)
    
    
    #
    for index, value in enumerate(number.digits):
        i_index = (numlength - 1) - index # inverse index
        
        add_at_index = add_single_digit(number.digits[i_index], number.digits[index], result[i_index+1])
        
        if add_at_index >= number.base:
            result[i_index+1] = CHARACTERS_SET[add_at_index % number.base]
            result[i_index] = CHARACTERS_SET[CHARACTERS_SET_DICT[result[i_index]] + 1]
            
        else:
            result[i_index+1] = CHARACTERS_SET[add_at_index]

    if result[0] == '0':
        result.pop(0)

    return ''.join(result)


def thread_lychrel(seed, iter_depth=1000):
    """
    Generator of Lychrel thread. The function takes a Number's instance (a seed)
    as argument and performs the reverse-add operation until a palindrome
    is found or the maximum number of iterations is reached.
    

    Parameters
    ----------
    seed : NUMBER object
        
    iter_depth : INT, optional
        Stop iteration criteria. The default is 1000.

    Yields
    ------
    next_seed : NUMBER object
    
    """
    
    # local variables definition and initialization
    test_lychrel = False
    index_iter = 0
    #print('******* INITIATE THREAD ********\nNumber : {} '.format(self.number))
    
    # Iterate over reverse-add sequence of a seed
    while test_lychrel is False and index_iter < iter_depth:
        next_seed = Number(reverse_add(seed),seed.base)
        index_iter += 1
        test_lychrel = next_seed.is_palindrome()
        seed = next_seed
        yield next_seed

def test_lychrel(seed, iter_depth=1000):
    """
    The function tests whether a Number's instance (a seed) is a Lychrel 
    candidate

    Parameters
    ----------
    seed : NUMBER object  
        
    iter_depth : TYPE, optional
        Stopping criteria for the reverse-and-add operation. The default is 1000.

    Returns
    -------
    test_lychrel : BOOLEAN
        True (the seed IS NOT a Lychrel candidate)        
        False (the seed IS a Lychrel candidate) --> the stopping criteria 
            has been reached BEFORE a palindrome is found in the thread

    """
    # local variables definition and initialization
    test_lychrel = False
    index_iter = 0
    #print('******* INITIATE THREAD ********\nNumber : {} '.format(self.number))
    
    # Iterate over reverse-add sequence of a seed
    while test_lychrel is False and index_iter < iter_depth:
        next_seed = Number(reverse_add(seed), seed.base)
        index_iter += 1
        test_lychrel = next_seed.is_palindrome()
        seed = next_seed
    
    return test_lychrel

def search_lychrel(seeds_list, iter_depth=500):
    """
    
    Parameters
    ----------
    seeds_list : LIST of Number's instance
        
    iter_depth : INT
        Stop criteria for the reverse-and-add operation

    Returns
    -------
    List of Lychrel candidates among the seeds list

    """
    
    return [x.digits for x in seeds_list if test_lychrel(x,iter_depth) is False]
       