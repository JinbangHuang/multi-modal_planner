#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import yaml
import pickle
sys.path.append('/home/jinbang/pddlstream')
from pddlstream.algorithms.meta import create_parser, solve
from pddlstream.language.generator import from_gen_fn, from_test
from pddlstream.language.stream import StreamInfo
from pddlstream.utils import read, user_input, str_from_object, INF, Profiler
from pddlstream.language.constants import PDDLProblem, print_solution, And, Minimize, Equal
from pddlstream.algorithms.constraints import PlanConstraints


from pddlstream.algorithms.meta import solve, create_parser
from pddlstream.algorithms.search import solve_from_pddl
from pddlstream.utils import read
from pddlstream.language.constants import print_solution, PDDLProblem


def read_pddl(filename):
    directory = os.path.dirname(os.path.abspath(__file__))
    return read(os.path.join(directory, filename))

##################################################

def solve_pddl():
    domain_pddl = read_pddl('domain.pddl')
    problem_pddl = read_pddl('test.yaml')

    plan, cost = solve_from_pddl(domain_pddl, problem_pddl)
    print('Plan:', plan)
    print('Cost:', cost)

##################################################

def get_problem(name):


    with open(name) as f:
        problem_info = yaml.safe_load(f)
    my_objects = problem_info['objects']

    init = [('gripper', 'gripper0'),
            ('free', 'gripper0'), 
            Equal(('total-cost',), 0),       
            Equal(('UnstackCost',), 0),
            Equal(('StackCost',), 10),
            Equal(('PickCost',), 0), 
            Equal(('PlaceCost',), 0),]
            # Minimize('total-cost')]
    
    object_list = problem_info['objects']
    for object in object_list.items():
        name = object[0]
        init += [('box', name)]
        if 'on-table' in object[1]:
            init += [('on_table', name)]
        if 'is-on' in object[1]:
            lower_b = object[1]['is-on'][0]
            init += [('on', name, lower_b)]
        if 'clear' in object[1]:
            init += [('top', name)]

    
    goal_list=[]
    for subtask in problem_info['goal'].items():
        subgoal = subtask[1]
        if 'is-on' in subgoal:
            goal_list.append(('on',subgoal['is-on']['upper'], subgoal['is-on']['lower']))
        if 'on-table' in subgoal:
            goal_list.append(('on_table',subgoal['on-table'][0]))
    print(goal_list)
    goal = And(*goal_list)



    domain_pddl = read_pddl('domain.pddl')
    constant_map = {}
    stream_pddl = None
    stream_map = {}


    return PDDLProblem(domain_pddl, constant_map, stream_pddl, stream_map, init, goal)

def solve_pddlstream(name,id, debug=False):
    parser = create_parser()
    args = parser.parse_args()
    # print('Arguments:', args)

    problem = get_problem(name)
    planner = 'dijkstra' # cerberus
    # planner  = 'lmcut-astar'
    plan,_,_ = solve(problem, algorithm='adaptive', unit_costs=args.unit, search_sample_ratio=100,reorder = False, planner=planner, debug=debug)

    with open("task_plan_mm_{}.pkl".format(id) ,"wb") as f:
        pickle.dump(plan, f)

##################################################

def main():
    # solve_pddl()
    for i in range(1,101):
        name = 'Problem_mm_' + str(i) +'.yaml'
        # name = 'problem_test.yaml'
        solve_pddlstream(name,i)


if __name__ == '__main__':
    main()