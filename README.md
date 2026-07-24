# LowQ2-MOBO [Under construction]

An application of the AID2E framework to the ePIC Low-Q2 tagger. 

## Optimization strategy

Optimization will proceed in stages, gradually building up the number of
parameters and objectives. These tages are listed below.

### Steps:

- [ ] Set up repo for optimization of linear tracking weights
- [ ] Optimize linear tracking weights against local track resolution for
    - [ ] Tagger 1
    - [ ] Tagger 2
- [ ] Add parameter config for optimization of tracker disk `z` positions
- [ ] Optimize tagger 1, 2 tracker disk `z` positions against local track resolution simultaneously
- [ ] Add electron efficiency and NN-retraining to objectives, full tracker disk position parameters
- [ ] Optimize tagger 1, 2 disk `z` positions against global track resolution simultaneoulsy (incl. NN-retraining)
- [ ] Optimize tagger 1, 2 disk `(x,y,z)` positions against track resolution and efficiency

## Dependencies

- Python 3.11.5
- Matplotlib
- Numpy
- Conda or Mamba (eg. via [Miniforge](https://github.com/conda-forge/miniforge)) 
- [EIC Software](https://eic.github.io)
- [BIC/LowQ2 framework](https://github.com/aid2e/BICLowQ2-framework)

## Code organization

This repository is structured like so:

  | File/Directory | Description |
  |----------------|-------------|
  | `lowq2-mobo.yml` | conda/mamba environment file |
  | `environment.py` | script to create/remove lowq2-mobo conda/mamba environment |
  | `run-lowq2-mobo.py` | wrapper script and point-of-entry to the problem |
  | `configurations` | collects various configuration files that define the problem |
  | `objectives` | collects analysis scripts to calculate objectives for optimize for |
  | `steering` | collects steering/macro files for running simulations |
  | `examples` | collects of example config files, scripts, etc. for illustrating some of the extended functionality |
  | `scripts` | collects various scripts useful for running, testing, etc. |
  | `tests` | collects test scripts for unit tests |

There are four configuration files which define the parameters of the problem.

  | File | Description |
  |------|-------------|
  | `run.config` | defines paths to EIC software, components, executables to be used, etc. |
  | `problem.config` | defines metadata and parameters for optimization algorithms |
  | `parameters.config` | defines design parameters to optimize with |
  | `objectives.config` | defines objectives to optimize for |

## Installation

Before beginning, please make sure conda and/or mamba is installed. Once
ready, the environment for the problem can be set up via:

```bash
./environment.py --create
```

And activated via `conda`
```bash
conda activate lowq2-mobo
```

At any point, this environment can be deleted with
```bash
./environment.py --remove
```

Lastly, you'll need to make sure the `eic-shell` is available on your
machine.  You can find instructions to do so [here](https://eic.github.io/tutorial-setting-up-environment/).

## Running the framework

Before running, make sure you source one of the generated scripts
in `./bin` to set appropriate environment variables:
```bash
source .bin/this-mobo.sh
```

Subsitute the appropriate script for your shell.  Note that these
can be modified to point to other config files as needed.  For
example, if you wanted to run with a different parameter file
you could modify the scripts such that:
```bash
export PAR_CFG=$THIS_MOBO/configuration/different_parameters.config
```

(Modify as needed for the other scripts) These can also be changed
at runtime using the options described [here](https://github.com/aid2e/BICLowQ2-framework/blob/main/src/BICLowQ2/AID2ETools/OptionParser.py#L84).

Then, create a local installation of [the ePIC geometry description](https://github.com/eic/epic):
```bash
cd <where-the-geo-goes>
git clone git@github.com:eic/epic.git
```

Then, modify `configurations/run.config` accordingly so that the paths point to your
installations and relevent scripts, e.g.
```json
    "_comment"      : "Configures runtime options, and paths to EIC software components",
    "conda"         : "<path-to-your-script>/conda.sh", # <<< for example /home/<username>/.miniforge3/etc/profile.d
    "environment"   : "lowq2-mobo",
    "out_path"      : "$THIS_MOBO/out",
    "run_path"      : "$THIS_MOBO/run",
    "log_path"      : "$THIS_MOBO/log",
    "eic_shell"     : "<path-to-your-script>/eic-shell", # <<< wherever you installed your eic-shell
    "overlap_check" : "checkOverlaps",
    "epic_setup"    : "$THIS_MOBO/epic/install/bin/thisepic.sh", # <<< might need to adjust
    "det_path"      : "$THIS_MOBO/epic/install/share/epic", # <<< might need to adjust
    "cmake_path"    : "$THIS_MOBO/epic", # <<< might need to adjust
    "det_path"      : "$THIS_MOBO/epic/install/share/epic", # <<< might need to adjust
    "det_config"    : "epic_ip6_extended",
    "sim_exec"      : "npsim",
    "sim_input"     : {
        "single_electron" : {
            "location" : "$THIS_MOBO/steering/electron",
            "type"     : "gps"
        },
        "pythia6" : {
            "_comment" : "currently unused",
            "location" : "$THIS_MOBO/steering/pythia",
            "type"     : "hepmc"
        }
    },
    "rec_exec"    : "eicrecon",
    "rec_collect" : [
        "MCParticles",
        "GeneratedParticles",
        "BackwardBeamlineHits",
        "TaggerTrackerM1LocalTracks",
        "TaggerTrackerM2LocalTracks",
        "TaggerTrackerReconstructedParticles"
    ],
    "sched_n_jobs"        : 1,
    "monitoring_interval" : 30

```

Notice the `$THIS_MOBO` variable: this points to the directory holding the
`bin/this-mobo.*` scripts.  It can be used to specify paths relative to
the directory the wrapper script is in.

Once appropriately configured, the optimization can be run in 3 modes:
1. Locally with Joblib
2. Remotely with a single Slurm monitoring job
3. Remotely in waves with a sequence of Slurm monitoring jobs.

**(1) Local Running:**
```bash
python run-lowq2-mobo.py
```

**(2) Single Monitoring Job Running:**
```bash
python run-lowq2-mobo.py -l
```

**(3) Multi-Monitoring Job Running:**
```bash
python run-lowq2-mobo.py -w
```
