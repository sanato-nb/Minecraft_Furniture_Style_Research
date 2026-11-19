#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 8 ]]; then
    echo 'Usage (from repository root): replay_exit.sh AF_GIT HC_GIT JAR_DIR AF_FABRIC_402 AF_NEOFORGE_403 NEW_ATLAS_TSV SCRATCH_DIRECTORY REPORT_DIRECTORY' >&2
    exit 2
fi
af=$1
hc=$2
jars=$3
fabric=$4
neoforge=$5
atlas=$6
work=$7
out=$8
phase=research/furniture_mods/phase_1-4
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$work"/{A,B,C,D,E,C_followup,E_followup}
faces="$work/MODEL_FACES.csv.xz"
source_flags=(--af "$af" --hc "$hc" --jars "$jars")

python "$phase/A/audit_handoff_scope.py" > "$work/A/1-4_A_SCOPE_AUDIT.json"
python "$phase/entry01/measure.py" --repo . "${source_flags[@]}" --out "$work/B" > "$work/B.log"
python "$phase/entry02/measure_uv.py" "${source_flags[@]}" --out "$work/C" --faces "$faces" > "$work/C.log"
python "$phase/entry02/audit_uv.py" "$faces" > "$work/C/INDEPENDENT_AUDIT.json"
python "$phase/entry03/compare_materials.py" "${source_flags[@]}" --faces "$faces" --out "$work/D" > "$work/D.log"
python "$phase/entry03/audit_comparison.py" > "$work/D/INDEPENDENT_AUDIT.json"
python "$phase/entry04/build_handoff.py" --af "$af" --faces "$faces" --out "$work/E" > "$work/E.log"
python "$phase/entry04/audit_handoff.py" > "$work/E/INDEPENDENT_AUDIT.json"
python "$phase/C_followup/measure_exceptions.py" "${source_flags[@]}" --faces "$faces" \
    --fabric-402 "$fabric" --neoforge-403 "$neoforge" --out "$work/C_followup" > "$work/C_followup.log"
python "$phase/C_followup/audit_support.py" > "$work/C_followup/INDEPENDENT_AUDIT.json"
cp "$atlas" "$work/ATLAS_REPLAY.tsv"
python "$phase/E_followup/audit_references.py" --atlas "$work/ATLAS_REPLAY.tsv" --fabric "$fabric" \
    --out "$work/E_followup" > "$work/E_followup.log"
python "$phase/F/audit_exit.py" --replay "$work" --out "$out"
