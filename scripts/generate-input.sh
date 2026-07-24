#!/bin/bash
# ===============================================
# @file    generate-input.sh
# @authors Derek Anderson
# @date    12.11.2025
# -----------------------------------------------
# Runs npsim and eicrecon to generate
# inputs for testing objective scripts.
#
# Usage:
#   ./generate-input.sh \
#       test.edm4hep.root \
#       test.edm4eic.root
# ===============================================

out_sim=$1
out_rec=$2

npsim --compactFile $DETECTOR_PATH/epic_ip6_extended.xml --enableG4GPS --steeringFile ../steering/electron/backward.e18ele.py --macroFile ../steering/electron/backward.e18ele.mac --outputFile $out_sim

eicrecon -Ppodio:output_file=$out_rec $out_sim

# end ===========================================
