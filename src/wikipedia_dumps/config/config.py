from pathlib import Path
from os.path import splitext

ROOT_DIR = Path(__file__).resolve().parents[3]

source_file_name = 'skwiki-20201101-pages-articles.xml'
source_file_path = ROOT_DIR.joinpath(f'data/{source_file_name}')
out_dir = ROOT_DIR.joinpath(f'data/{splitext(source_file_name)[0]}')

# create the out_dir if does not exist
Path(out_dir).mkdir(parents=True, exist_ok=True)
