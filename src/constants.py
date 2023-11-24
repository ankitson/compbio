from enum import Enum
import os

TEMP_PATH = os.path.abspath('../outputs/temp.txt')

# These are imported from the weekX.py files, which are run at path src/, but also from the server 
DATASETS = {
    'e_coli': os.path.abspath('../inputs/E_coli_genome.txt'),
    'salmonella': os.path.abspath('/home/ankit/code/compbio/inputs/Salmonella_enterica.txt'),
    'cholera': os.path.abspath('../inputs/Vibrio_Cholera_Genome.txt'),
    'tb_dosr': os.path.abspath('../inputs/DosR.txt'),
}
DATASET_KEYS = list(DATASETS.keys())

BASES = ['A','C','G','T']
BASES_COMPLEMENTS = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

class Plots(Enum):
    COUNTS_RAW = 'Counts'
    COUNTS_PCT = 'Counts (%)'
    COUNTS_PCT_BASE = 'Counts Centered (%)'
    COUNTS_PCT_DIFF = 'Counts Diff(%)'
    SKEW = 'Skew'
    TEST = 'Test'
    NETWORK = 'Network'

ENABLED_PLOTS = [Plots.COUNTS_PCT_BASE, Plots.COUNTS_PCT_DIFF, Plots.SKEW, Plots.NETWORK]

def dataset(key):
  if key not in DATASET_KEYS:
    raise Exception(f"invalid key {key}")
  if key == 'tb_dosr':
     with open(DATASETS[key]) as f: return [l.strip() for l in f.readlines()]
  with open(DATASETS[key]) as f: return f.read().strip().replace('\n','')