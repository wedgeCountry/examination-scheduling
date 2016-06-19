#!/usr/bin/env python
# -*- coding: utf-8 -*-



from __future__ import division

import sys
import os
PATHS = os.getcwd().split('/')
PROJECT_PATH = ''
for p in PATHS:
    PROJECT_PATH += '%s/' % p
    if p == 'examination-scheduling':
        break
sys.path.append(PROJECT_PATH)

from time import time
import random 

from GurobiModel.GurobiLinear_v_1 import build_model as build_linear_model_1
from GurobiModel.GurobiLinear_v_2_Q import build_model as build_linear_model_2
from GurobiModel.GurobiLinear_v_3 import build_model as build_linear_model_3
from GurobiModel.GurobiLinear_v_4_Cliques import build_model as build_linear_model_4
from GurobiModel.GurobiLinear_v_5_changed_obj import build_model as build_linear_model_5
from GurobiModel.GurobiLinear_v_6_removed_c6 import build_model as build_linear_model_6
from GurobiModel.GurobiLinear_v_8_removed_obj import build_model as build_linear_model_8
from GurobiModel.GurobiLinear_v_10_location import build_model as build_linear_model_10
from GurobiModel.GurobiLinear_v_11_model_speed import build_model as build_linear_model_11
from GurobiModel.GurobiLinear_v_12_smaller_M import build_model as build_linear_model_12
from GurobiModel.GurobiLinear_v_13_cover_inequalities import build_model as build_linear_model_13

from GurobiModel.GurobiLinear_v_14_cuts1 import build_model as build_linear_model_14c1
from GurobiModel.GurobiLinear_v_14_cuts2 import build_model as build_linear_model_14c2
from GurobiModel.GurobiLinear_v_14_cuts3 import build_model as build_linear_model_14c3
from GurobiModel.GurobiLinear_v_14_cuts4 import build_model as build_linear_model_14c4
from GurobiModel.GurobiLinear_v_14_cuts5 import build_model as build_linear_model_14c5
from GurobiModel.GurobiLinear_v_14_cuts6 import build_model as build_linear_model_14c6
from GurobiModel.GurobiLinear_v_14_cuts7 import build_model as build_linear_model_14c7
from GurobiModel.GurobiLinear_v_14_cuts8 import build_model as build_linear_model_14c8
from GurobiModel.GurobiLinear_v_14_cuts9 import build_model as build_linear_model_14c9
from GurobiModel.GurobiLinear_v_14_cuts10 import build_model as build_linear_model_14c10
from GurobiModel.GurobiLinear_v_14_cuts11 import build_model as build_linear_model_14c11
from GurobiModel.GurobiLinear_v_14_cuts12 import build_model as build_linear_model_14c12

from GurobiModel.GurobiLinear_v_15_more_covers import build_model as build_linear_model_15
from GurobiModel.GurobiLinear_v_16_symmetry import build_model as build_linear_model_16
from GurobiModel.GurobiLinear_v_17_pertubate import build_model as build_linear_model_17
from GurobiModel.GurobiLinear_v_18_lexicographic import build_model as build_linear_model_18





from model.instance import build_smart_random
from model.instance import build_real_data
from model.instance import build_real_data_sample




def compare(data):
    """ we compare for some problems how many time we need to solve each problem
    """
    # Select models to compare
    problems = {
    #    'Linear Lexicographic': build_linear_model_18,
    #    'Linear Pertubate': build_linear_model_17,
    #    'Linear symmetrie': build_linear_model_16,
       'Linear more covers': build_linear_model_15,
    #    'Linear Cover inequalities': build_linear_model_13,
    #    'Linear smaller M': build_linear_model_12,
    #    'Linear model speed': build_linear_model_11,
    #    'Linear Location': build_linear_model_10,
    #   'Linear Advanced removed obj': build_linear_model_8,
    #   'Linear Advanced removed c6': build_linear_model_6,
    #   'Linear Advanced changed obj': build_linear_model_5,
    #   'Linear Advanced': build_linear_model_3,
    #   'Linear Advanced Cliques': build_linear_model_4,    
    #   'GurobiQ_neu': build_nonlinear_model
    }

    times = dict()

    objectives = dict()

    for prob_name in problems:
        print(prob_name)
        # Build selected model
        random.seed(42)

        problem = problems[prob_name](data)
        # Optimize selected model
        t = time()
        problem.optimize()
        times[prob_name] = time() - t

        for i in range(data['n']):
            for k in range(data['r']):
                for l in range(data['p']):
                    v = problem.getVarByName('x_%s_%s_%s' % (i,k,l))
                    if not v is None and v.x == 1:
                        print('%s %g' % (v.varName, v.x))

        # Save objective value
        try:
            objectives[prob_name] = problem.objVal
        except:

            objectives[prob_name] = 0

    return times, objectives


def test_compare():
    n = 200 
    r = 20
    p = 20
    tseed = 5656

    #data = build_smart_random(n=n,r=r,p=p,tseed=tseed)
    #data = build_real_data(tseed=tseed)
    data = build_real_data_sample(n=n,r=r,p=p,tseed=tseed)
    print data['c']
    print data['s']
    time, objectives = compare(data)

    print("")
    print("n: %s" % (n))
    print("r: %s" % (r))
    print("p: %s" % (p))
    print("seed: %s" % (tseed))
    print("Percentage conflicts: %s" % (sum( sum(data['conflicts'][i]) for i in range(n))/(2*n*(n-1))))
    print("")
    for key in time:
        print key
        print("time:")
        print(time[key])
        print("value:")
        print(objectives[key])
        print("")


if __name__ == '__main__':
    test_compare()
