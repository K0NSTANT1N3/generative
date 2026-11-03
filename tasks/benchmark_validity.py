"""Time public-source structure parsing locally; this is not a GPU benchmark."""
import csv
import importlib.metadata
import json
import platform
import random
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

from glyles import convert
from rdkit import Chem, RDLogger

RDLogger.DisableLog('rdApp.*')
SOURCE = Path('/tmp/glycan_np_audit')
rng = random.Random(20261023)

def summary(values):
    values = sorted(values)
    return {'n': len(values), 'median_ms': statistics.median(values),
            'mean_ms': statistics.mean(values),
            'p95_ms': values[int(0.95 * (len(values) - 1))]}

with (SOURCE / 'molgen_np_test.csv').open() as handle:
    nps = [r['smiles'] for r in csv.DictReader(handle)]
nps = rng.sample(list(dict.fromkeys(nps)), 200)
with (SOURCE / 'sweettalk_data.csv').open() as handle:
    glycans = [r['target'] for r in csv.DictReader(handle)]
glycans = sorted({g for g in glycans if '?' not in g and 15 <= len(g) <= 220})
glycans = rng.sample(glycans, 200)

def validate_np(smiles):
    molecule = Chem.MolFromSmiles(smiles)
    return None if molecule is None else Chem.MolToSmiles(molecule, isomericSmiles=True)

def validate_glycan(iupac):
    result = convert(iupac)
    return validate_np(result[0][1]) if result and result[0][1] else None

validate_np(nps[0])
validate_glycan('Gal(b1-4)GlcNAc')
np_times, np_ok, heavy_atoms = [], 0, []
for _ in range(10):
    for molecule in nps:
        start = time.perf_counter()
        result = validate_np(molecule)
        np_times.append(1000 * (time.perf_counter() - start))
        np_ok += result is not None
for molecule in nps:
    mol = Chem.MolFromSmiles(molecule)
    if mol is not None:
        heavy_atoms.append(mol.GetNumHeavyAtoms())

glycan_times, glycan_success_times, glycan_ok = [], [], 0
for molecule in glycans:
    start = time.perf_counter()
    try:
        result = validate_glycan(molecule)
    except Exception:
        result = None
    duration = 1000 * (time.perf_counter() - start)
    glycan_times.append(duration)
    if result is not None:
        glycan_ok += 1
        glycan_success_times.append(duration)

cpu = next((line.split(':', 1)[1].strip()
            for line in Path('/proc/cpuinfo').read_text().splitlines()
            if line.startswith('model name')), platform.processor())
report = {
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'cpu': cpu, 'python': platform.python_version(),
    'packages': {p: importlib.metadata.version(p) for p in ['rdkit', 'glyles', 'numpy']},
    'rdkit_parse_sanitize_canonicalize': {
        **summary(np_times), 'unique_reference_molecules': 200,
        'repeats': 10, 'successful_calls': np_ok,
        'heavy_atoms_min': min(heavy_atoms), 'heavy_atoms_max': max(heavy_atoms)},
    'glyles_convert_then_rdkit': {
        **summary(glycan_times), 'successful': glycan_ok,
        'successful_only': summary(glycan_success_times)},
    'limits': 'Local CPU timings on reference inputs, not Colab, generated-invalid inputs, biosynthesis, or activity validation.',
}
target = Path(__file__).resolve().parent / 'validity_benchmark.json'
target.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
