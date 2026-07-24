# =============================================================================
## @file   run-lowq2-mobo.py
#  @author Derek Anderson
#  @date   07.23.2026
# -----------------------------------------------------------------------------
## @brief Main executable and wrapper script for
#    running the LowQ2-MOBO problem.
# =============================================================================

def RunObjectives(tag = None, **kwargs):
    """RunObjectives

    Runs trial (simulation, reconstruction,
    and all analyses) for provided set of
    updated parameters.

    Args:
      tag:    tag associated with trial
      kwargs: any keyword arguments (e.g. parameterization)
    Returns:
      dictionary of objectives and their values
    """
    # NB use lazy importing to make sure
    # dependencies get picked up
    import json
    import os
    from BICLowQ2 import AID2ETools as at
    from BICLowQ2 import EICTools as et

    # grab paths to config files
    run_path, exp_path, par_path, obj_path = at.GetConfigPaths()

    # create trial manager
    trial = et.TrialManager(run_path, par_path, obj_path, tag)

    # create and run script
    oFiles = trial.DoTrial(kwargs)

    # extract relevant objectives
    #   --> (should be in associated
    #       json files)
    objectives = dict()
    for obj, file in oFiles.items():
        oJson = file.replace(".root", ".json")
        oVal  = None
        if os.path.isfile(oJson):
            with open(oJson, 'r') as out:
                oDat = json.load(out)
                oVal = oDat[obj]
            objectives[obj] = oVal

    # return dictionary of objectives
    return objectives

def main(*args, **kwargs):
    """main

    Wrapper to run BIC-MOBO. Can be run in
    3 modes, set with the -b or -w options:

     default -- with Ax and in a single monitoring job
       >>> python new-run.py

     waves -- with Ax over a sequence of monitoring jobs
       >>> python new-run.py -w

    In the default mode, user can specify which runner
    to use with the -r option:

      joblib -- use joblib runner (default)
      slurm  -- use slurm runner
      panda  -- use panda runner (TODO)

    User can also specify an Ax experiment
    to load with the -x option, or override
    which configuration files to use with the
    -u, -e, -p, -o, -s, -t options as detailed
    below.

    Args:
      -w: run in waves
      -r: specify runner
      -x: specify experiment to load
      -u: specify a run config to use
      -e: specify an experiment/problem config to use
      -p: specify a parameter config to use
      -o: specify an objective config to use
      -s: specify an environment script to source
      -t: specify a SLURM template to use
    """
    from BICLowQ2 import AID2ETools as at

    options = at.ParseArguments()
    client  = at.BICLowQ2Client(options, RunObjectives)
    if options.waves:
        client.Waves(__file__)
    else:
        client.Run()

if __name__ == "__main__":
    main()

# end ========================================================================
