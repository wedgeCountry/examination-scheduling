#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from collections import defaultdict

from inputData import examination_data
from heuristics import tools

from evaluation.objectives import obj_time, obj_room

    
def get_moses_representation(data, gamma=1.0, verbose = False):
    
    n, r, p = data['n'], data['r'], data['p']
    if verbose: print n, r, p
    
    h = data['h']
    
    # load exam names
    exams = data['exam_names']
    # for each exam the time
    result_times = data['result_times']
    # for each exam the room
    result_rooms = data['result_rooms']
    # for each room index the name
    room_names = data['room_names']
    
    y = defaultdict(int)
    for i, exam in enumerate(exams):
        l = h.index(result_times[exam])
        y[i,l] = 1.0
    
    x = defaultdict(int)
    for i, exam in enumerate(exams):
        for room in result_rooms[exam]:
            k = room_names.index(room)
            x[i,k] = 1.0
          
    times = [result_times[exam] for exam in exams]
    
    v = obj_room(x) - gamma * obj_time(times, data, h_max = max(h))
    
    return x, times, v

    
if __name__ == '__main__':
    
    gamma = 1.0
    
    data = examination_data.read_data(threshold = 0)
    data['similar_periods'] = tools.get_similar_periods(data)
    
    x, y, v = get_moses_representation(data, gamma=gamma, verbose=True)
    print "ROOM_OBJ:", obj_room(x)
    print "TIME_OBJ:", obj_time(y, data, h_max = max(data['h']))
    print "VALUE:", v
    
    # get rooms for which we dont have data
    #if False:
        
        #print "Rooms of which we have data:"
        #print sorted(room_names)
        #print "Rooms in moses:"
        #r1 = set([ room for rooms in result_rooms.values() for room in rooms ])
        #print sorted(r1)
        #print "Rooms of which we don't have data:"
        #r2 = set(room_names)
        #print sorted([r for r in r1 if r not in r2])
        
    
    