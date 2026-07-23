# =============================================================================
## @file   test-objectives.py
#  @author Derek Anderson
#  @date   08.29.2025
# -----------------------------------------------------------------------------
## @Driver script to test run objective
#    methods
#
#  TODO convert to use pytest
# =============================================================================

import json
import subprocess
import sys
sys.path.append('../')

import objectives.LowQ2GlobalResolution as lqg
import objectives.LowQ2LocalResolution as lql

# test 0: generate inputs -----------------------------------------------------

# input file names for convenience
ifSim = "backward.e18ele.edm4hep.root"
ifRec = "backward.e18ele.edm4eic.root"

subprocess.run(["../scripts/generate-input.sh", ifSim, ifRec])

# test 0: run objectives ------------------------------------------------------

# output file names for convenience
ofGloRes  = "test_globa_reso.root"
ofLocRes1 = "test_local1_reso.root"
ofLocRes2 = "test_local2_reso.root"

# test global resolution
glo_reso = lqg.CalculateMomReso(ifRec, ofGloRes)

# test local resolutions
lo1_reso = lql.CalculateMomReso(ifSim, ifRec, ofLocRes1, 1)
lo2_reso = lql.CalculateMomReso(ifSim, ifRec, ofLocRes2, 2)

print(f"[1] Ran objectives:")
print(f"  -- global p resolution   = {glo_reso}")
print(f"  -- m1 local p resolution = {lo1_reso}")
print(f"  -- m2 local p resolution = {lo2_reso}")

# test 1: extract objectives --------------------------------------------------

# extract global resolution
glo_reso_json = None
with open(ofGloRes.replace(".root", ".json")) as oglo:
    glo_reso_data = json.load(oglo)
    glo_reso_json = glo_reso_data["global_resolution"]

# extract local resolutions
lo1_reso_json = None
with open(ofLocRes1.replace(".root", ".json")) as olo1:
    lo1_reso_data = json.load(olo1)
    lo1_reso_json = lo1_reso_data["local_resolution_1"]

lo2_reso_json = None
with open(ofLocRes2.replace(".root", ".json")) as olo2:
    lo2_reso_data = json.load(olo2)
    lo2_reso_json = lo2_reso_data["local_resolution_2"]

print(f"[2] Extracted objectives:")
print(f"  -- global p resolution   = {glo_reso_json}, type = {type(glo_reso_json)}")
print(f"  -- m1 local p resolution = {lo1_reso_json}, type = {type(lo1_reso_json)}")
print(f"  -- m2 local p resolution = {lo2_reso_json}, type = {type(lo2_reso_json)}")

# end =========================================================================
