# -*- coding: utf-8 -*-
#
# This source file is part of the FabSim software toolkit, which is distributed under the BSD 3-Clause license.
# Please refer to LICENSE for detailed information regarding the licensing.
#
# This file contains FabSim definitions specific to FabDummy.

from base.fab import *
import ymmsl  # Required to process ymmsl files (comes with MUSCLE3).

# Add local script, blackbox and template path.
add_local_paths("FabMUSCLE")


@task
def install_muscle(config, **args):
    update_environment(args)
    with_config("install_muscle")
    execute(put_configs,config)
    job(dict(script='install_muscle', wall_time='0:15:0', memory='2G'))


@task
def muscle_unified(config, muscle_script="main.py", **args):
    update_environment(args)
    update_environment({"muscle_script":muscle_script})
    with_config(config)
    execute(put_configs,config)
    job(dict(script='muscle_unified', wall_time='0:15:0', memory='2G'),args)


@task
def make_muscle_ensemble(config, ymmsl_name, **args):
    """
    Creates a concurrently running MUSCLE ensemble application using a 
    variation of run_ensemble.
    """
    with_config(config)
    local("rm -rf {}/SWEEP".format(env.job_config_path_local))

    # Make MUSCLE Manager directory.
    local("mkdir -p {}/SWEEP/muscle_manager".format(env.job_config_path_local))
    local("cp {}/{} {}/SWEEP/muscle_manager/".format(env.job_config_path_local, ymmsl_name, env.job_config_path_local))

    with open("{}/{}".format(env.job_config_path_local, ymmsl_name), 'r') as f:
        config = ymmsl.load(f)

    # Make directories for MUSCLE submodel instances.
    for ce in config.model.compute_elements:

        print(ce.name, ce.implementation)
        local("mkdir {}/SWEEP/{}".format(env.job_config_path_local, ce.name))
        local("cp {}/{}.py {}/SWEEP/{}/model.py".format(env.job_config_path_local, ce.implementation, env.job_config_path_local, ce.name))


@task
def run_muscle_dist(config, ymmsl_name="main.ymmsl", **args):
    """
    Run a MUSCLE application as a FabSim ensemble.
    """
    make_muscle_ensemble(config, ymmsl_name, **args)

    path_to_config = find_config_file_path(config)
    sweep_dir = path_to_config + "/SWEEP"
    env.script = 'muscle_distributed'
    update_environment({"ymmsl_name":ymmsl_name, "muscle_model_script":"model.py", "exec_first":"muscle_manager"})

    run_ensemble(config, sweep_dir, **args)
   

@task
def run_muscle_dist_local(config, ymmsl_name="main.ymmsl", **args):

    scripts = ["muscle_manager {}".format(ymmsl_name)]

    with_config(config)

    with open("{}/{}".format(env.job_config_path_local, ymmsl_name), 'r') as f:
        config = ymmsl.load(f)

    for ce in config.model.compute_elements:
        print(ce.name, ce.implementation)

        print("python3 ./{}.py --muscle-instance={}".format(ce.implementation, ce.name))
        scripts.append("python3 ./{}.py --muscle-instance={}".format(ce.implementation, ce.name))

    exec_string = "cd {} ; ".format(env.job_config_path_local)
    for s in scripts:
        exec_string += "{} & ".format(s)
    exec_string += " wait"
    print(exec_string)
    local(exec_string)


### Old FabDummy code

@task
def dummy(config,**args):
    """Submit a Dummy job to the remote queue.
    The job results will be stored with a name pattern as defined in the environment,
    e.g. cylinder-abcd1234-legion-256
    config : config directory to use to define input files, e.g. config=cylinder
    Keyword arguments:
            cores : number of compute cores to request
            images : number of images to take
            steering : steering session i.d.
            wall_time : wall-time job limit
            memory : memory per node
    """
    update_environment(args)
    with_config(config)
    execute(put_configs,config)
    job(dict(script='dummy', wall_time='0:15:0', memory='2G'),args)

@task
def dummy_ensemble(config="dummy_test",**args):
    """
    Submits an ensemble of dummy jobs.
    One job is run for each file in <config_file_directory>/dummy_test/SWEEP.
    """
    
    path_to_config = find_config_file_path(config)
    print("local config file path at: %s" % path_to_config)
    sweep_dir = path_to_config + "/SWEEP"
    env.script = 'dummy'
    env.input_name_in_config = 'dummy.txt'

    run_ensemble(config, sweep_dir, **args)
    
@task
def lammps_dummy(config,**args):
    """Submit a LAMMPS job to the remote queue.
    The job results will be stored with a name pattern as defined in the environment,
    e.g. cylinder-abcd1234-legion-256
    config : config directory to use to define geometry, e.g. config=lamps_lj_liquid
    Keyword arguments:
            cores : number of compute cores to request
            images : number of images to take
            steering : steering session i.d.
            wall_time : wall-time job limit
            memory : memory per node
    """
    with_config(config)
    execute(put_configs,config)
    job(dict(script='lammps', wall_time = '0:15:0', lammps_input = "in.CG.lammps"),args)
