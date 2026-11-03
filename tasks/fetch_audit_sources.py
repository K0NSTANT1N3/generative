"""Download public research source/config metadata into /tmp for this audit."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path('/tmp/glycan_np_audit')
ROOT.mkdir(exist_ok=True)
URLS = {
    'spacegfn_paper.pdf': 'https://arxiv.org/pdf/2603.00614',
    'sweettalk_tree.json': 'https://api.github.com/repos/midas-wyss/sweettalk/git/trees/master?recursive=1',
    'molgen_tree.json': 'https://api.github.com/repos/zjunlp/MolGen/git/trees/main?recursive=1',
    'molgen_README.md': 'https://raw.githubusercontent.com/zjunlp/MolGen/main/README.md',
    'molgen_LICENSE': 'https://raw.githubusercontent.com/zjunlp/MolGen/main/LICENSE',
    'chefnmr_tree.json': 'https://api.github.com/repos/ml-struct-bio/chefnmr/git/trees/main?recursive=1',
    'chefnmr_README.md': 'https://raw.githubusercontent.com/ml-struct-bio/chefnmr/main/README.md',
    'chefnmr_LICENSE': 'https://raw.githubusercontent.com/ml-struct-bio/chefnmr/main/LICENSE',
    'glycoforge_tree.json': 'https://api.github.com/repos/BojarLab/GlycoForge/git/trees/main?recursive=1',
    'glycan_np_download_page.html': 'https://glycosmos.org/download',
    'molgen_config.py': 'https://raw.githubusercontent.com/zjunlp/MolGen/main/MolGen/config.py',
    'molgen_config.json': 'https://raw.githubusercontent.com/zjunlp/MolGen/main/MolGen/config.json',
    'molgen_train_ds.py': 'https://raw.githubusercontent.com/zjunlp/MolGen/main/MolGen/train_ds.py',
    'molgen_train_prefix.py': 'https://raw.githubusercontent.com/zjunlp/MolGen/main/MolGen/train_prefix.py',
    'molgen_paper.pdf': 'https://arxiv.org/pdf/2301.11259',
    'chefnmr_LICENSE.txt': 'https://raw.githubusercontent.com/ml-struct-bio/chefnmr/main/LICENSE.txt',
    'chefnmr_config.yaml': 'https://raw.githubusercontent.com/ml-struct-bio/chefnmr/main/configs/config.yaml',
    'chefnmr_large.yaml': 'https://raw.githubusercontent.com/ml-struct-bio/chefnmr/main/configs/model/dit-l.yaml',
    'chefnmr_small.yaml': 'https://raw.githubusercontent.com/ml-struct-bio/chefnmr/main/configs/model/dit-s.yaml',
    'chefnmr_train.slurm': 'https://raw.githubusercontent.com/ml-struct-bio/chefnmr/main/script/00-training/02-spectranp/NP-H10kC10k-L64-cfg15-gpu8-seed42.slurm',
    'chefnmr_paper.html': 'https://arxiv.org/html/2512.03127v1',
    'sweettalk_data.csv': 'https://raw.githubusercontent.com/midas-wyss/sweettalk/master/datasets/combined_database_long.csv',
    'sweettalk_LICENSE': 'https://raw.githubusercontent.com/midas-wyss/sweettalk/master/LICENSE',
    'sweettalk_paper.pdf': 'https://static1.squarespace.com/static/5c264953620b850c9fb03732/t/600082bf431d6965cc7504a2/1610646220537/cellhostmicrobe_bojar.pdf',
    'glycobart_zenodo.json': 'https://zenodo.org/api/records/15741423',
    'sweetfold_zenodo.json': 'https://zenodo.org/api/records/21105358',
    'chefnmr_zenodo.json': 'https://zenodo.org/api/records/17766755',
    's4_zenodo.json': 'https://zenodo.org/api/records/12666371',
    'glycangt_zenodo.json': 'https://zenodo.org/api/records/18636040',
    'molgen_hf_config.json': 'https://huggingface.co/zjunlp/MolGen-large/resolve/main/config.json',
    'molgen_np_test.csv': 'https://raw.githubusercontent.com/zjunlp/MolGen/main/moldata/finetune/np_test.csv',
}

def fetch(item):
    name, url = item
    try:
        if (ROOT / name).exists():
            body = (ROOT / name).read_bytes()
            return {'file': name, 'url': url, 'status': 'cached', 'bytes': len(body),
                    'sha256': hashlib.sha256(body).hexdigest()}
        with urlopen(Request(url, headers={'User-Agent': 'Research-audit/1.0'}), timeout=40) as response:
            body = response.read(64_000_001)
            if len(body) > 64_000_000:
                raise ValueError('Source exceeds the 64 MB audit limit; not saved')
            (ROOT / name).write_bytes(body)
            return {'file': name, 'url': url, 'status': response.status,
                    'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}
    except Exception as exc:
        return {'file': name, 'url': url, 'error': str(exc)}

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(fetch, URLS.items()))
(ROOT / 'fetch_manifest.json').write_text(json.dumps(results, indent=2))
for result in results:
    print(json.dumps(result))
