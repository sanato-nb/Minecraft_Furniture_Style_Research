#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 6 ]]; then
    echo 'Usage (from repository root): replay_static.sh WORK AF_GIT HC_GIT MACAW_JAR MC_1.21.1_JAR MC_1.21.11_JAR' >&2
    exit 2
fi

work=$1
phase=research/furniture_mods/phase_1-5
mkdir -p "$work"/{A,B,C,D,E}

python "$phase/A/verify_scope.py" --jar "$6" --out "$work/A"
python "$phase/B/measure_comparison.py" --jar "$6" --out "$work/B"
python "$phase/C/compare_categories.py" --out "$work/C"
python "$phase/D/review_exceptions.py" --af "$2" --hc "$3" --macaw "$4" \
    --mc1211 "$5" --mc12111 "$6" --out "$work/D"
python "$phase/E/build_comparison_db.py" --out "$work/E"
