import sys
import os
import jax.numpy as jnp
from jax import vmap
import datetime
import pandas as pd 
sys.path.insert(1, os.path.join(sys.path[0], ".."))
from function_creation.function import Function
import matplotlib.pyplot as plt
from main import bo
from utils import *
import uuid
from function_creation.create_problem import create_problem
import multiprocessing




def run_behaviour(data):
    behaviour_index,aq,f_index,d,f_keys = data
    f_key = f_keys[f_index]
    human_behaviours = ['expert','adversarial','trusting',0.25,0.5,0.75]
    # for this problem data
    problem_data = {}
    problem_data["sample_initial"] = 4
    problem_data["gp_ms"] = 8
    problem_data["alternatives"] = 3
    problem_data["NSGA_iters"] = 50
    problem_data["plotting"] = True
    problem_data['max_iterations'] = 75
    # problem_data['lengthscale'] = 0.4
    problem_data['lengthscale'] = 0.8
    problem_data['dim'] = d
    # at a given human behaviour
    problem_data['human_behaviour'] = human_behaviours[behaviour_index]
    problem_data['acquisition_function'] = aq

    aqs = {'EI':EI,'UCB':UCB}

    # for a given function...
    key = random.PRNGKey(f_key)
    f = Function(create_problem(key,problem_data['lengthscale'],problem_data['dim']))

    file = str(uuid.uuid4())
    path = "bo/results/" + file + "/"
    os.mkdir(path)

    problem_data['time_created'] = str(datetime.datetime.now())
    problem_data['file_name'] = path
    problem_data['function_key'] = str(f_key)


    bo(
        f,
        aqs[aq],
        problem_data,
        path=path
    )


# evaluate for each behaviour using a pool 
if __name__ == '__main__':
    f_keys = pd.read_csv('function_creation/f_keys.csv')['f_keys'].values
    problems = len(f_keys)

    try:
        b_index = int(sys.argv[1])
        aq = sys.argv[2]
        d = int(sys.argv[3])
    except:
        f_index = 0
        b_index = 0
        d = 1
        aq = 'UCB'

    pool = multiprocessing.Pool(processes=8)
    # pool.map(run_behaviour,range(6))
    pool.map(run_behaviour,[(b_index,aq,f_index,d,f_keys) for f_index in range(50)])
    pool.close()

