"""Read public dataset metadata/pages for the bee-project source audit."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path('/tmp/bee-dataset-audit')
ROOT.mkdir(exist_ok=True)
URLS = {
    'mendeley_chronic.json': 'https://data.mendeley.com/public-api/datasets/7y27kdw5h2/versions/1',
    'mendeley_development.json': 'https://data.mendeley.com/public-api/datasets/948kv7yhdp/versions/1',
    'mendeley_adjuvants.json': 'https://data.mendeley.com/public-api/datasets/hj9xk95h2t/versions/1',
    'mendeley_chronic.html': 'https://data.mendeley.com/datasets/7y27kdw5h2/1',
    'mendeley_adjuvants.html': 'https://data.mendeley.com/datasets/hj9xk95h2t/1',
    'dryad_neonic_field.json': 'https://datadryad.org/api/v2/datasets/doi:10.5061/dryad.245kq',
    'dryad_fungicide_heat.json': 'https://datadryad.org/api/v2/datasets/doi:10.5061/dryad.jh9w0vth8',
    'dryad_osmia_chronic.json': 'https://datadryad.org/api/v2/datasets/doi:10.5061/dryad.wh70rxwxk',
    'dryad_xenoglossa.json': 'https://datadryad.org/api/v2/datasets/doi:10.5061/dryad.b2rbnzsp6',
    'dryad_optomotor.json': 'https://datadryad.org/api/v2/datasets/doi:10.5061/dryad.ht76hdrh4',
    'dryad_fpf_pathogen.json': 'https://datadryad.org/api/v2/datasets/doi:10.5061/dryad.1g1jwsv54',
    'dryad_swimming.json': 'https://datadryad.org/api/v2/datasets/doi:10.5061/dryad.w9ghx3g2r',
    'dryad_search.json': 'https://datadryad.org/api/v2/search?q=bee%20pesticide&per_page=100',
    'dryad_search_toxicity.json': 'https://datadryad.org/api/v2/search?q=bee%20toxicity&per_page=100',
    'dryad_search_insecticide.json': 'https://datadryad.org/api/v2/search?q=bee%20insecticide&per_page=100',
    'dryad_search_fungicide.json': 'https://datadryad.org/api/v2/search?q=bee%20fungicide&per_page=100',
    'dryad_search_pollinator.json': 'https://datadryad.org/api/v2/search?q=pollinator%20pesticide&per_page=100',
    'dryad_search_neonic.json': 'https://datadryad.org/api/v2/search?q=bee%20neonicotinoid&per_page=100',
    'dryad_osmia_encoded.json': 'https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.wh70rxwxk',
    'mendeley_development.html': 'https://data.mendeley.com/datasets/948kv7yhdp/1',
    'zenodo_poshbee.json': 'https://zenodo.org/api/records/20341013',
    'zenodo_harmonized.json': 'https://zenodo.org/api/records/17288507',
    'figshare_beeecotox.json': 'https://api.figshare.com/v2/articles/32019582',
    'figshare_tosi.json': 'https://api.figshare.com/v2/articles/20208659',
    'figshare_epa_endpoints.json': 'https://api.figshare.com/v2/articles/19541630',
    'beesafe_tree.json': 'https://api.github.com/repos/sxxyyzk/Bee-Safe-2.0/git/trees/main?recursive=1',
    'zenodo_apple_risk.json': 'https://zenodo.org/api/records/10835333',
    'zenodo_bee_hotels.json': 'https://zenodo.org/api/records/20844744',
    'zenodo_heat_acetamiprid.json': 'https://zenodo.org/api/records/18800326',
    'zenodo_mustb.json': 'https://zenodo.org/api/records/4953761',
    'zenodo_betterb_restricted.json': 'https://zenodo.org/api/records/21352607',
    'zenodo_search.json': 'https://zenodo.org/api/records?q=resource_type.type%3Adataset%20AND%20%28bee%20OR%20honeybee%20OR%20bumblebee%20OR%20pollinator%29%20AND%20%28toxicity%20OR%20pesticide%20OR%20insecticide%20OR%20fungicide%29&size=100',
    'illinois_honey.html': 'https://databank.illinois.edu/datasets/IDB-6733018',
    'ucr.html': 'https://bees.ucr.edu/pesticide-toxicity',
    'minnesota.html': 'https://www.mda.state.mn.us/protecting/bmps/pollinators/beetoxicity',
}

def fetch(item):
    name, url = item
    target = ROOT / name
    try:
        if target.exists():
            body = target.read_bytes()
            status = 'cached'
        else:
            with urlopen(Request(url, headers={'User-Agent': 'Dataset-research-audit/1.0'}), timeout=25) as response:
                body = response.read(5_000_001)
                status = response.status
            if len(body) > 5_000_000:
                raise ValueError('metadata/page exceeds 5 MB limit')
            target.write_bytes(body)
        return {'file': name, 'url': url, 'status': status, 'bytes': len(body),
                'sha256': hashlib.sha256(body).hexdigest()}
    except Exception as exc:
        return {'file': name, 'url': url, 'error': str(exc)}

with ThreadPoolExecutor(max_workers=5) as pool:
    manifest = list(pool.map(fetch, URLS.items()))
(ROOT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
for entry in manifest:
    print(json.dumps(entry))
