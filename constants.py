from enum import Enum
import os

GENOMES = {
    'e_coli': os.path.abspath('inputs/E_coli_genome.txt'),
    'salmonella': os.path.abspath('inputs/Salmonella_enterica.txt'),
    'cholera': os.path.abspath('inputs/Vibrio_Cholera_Genome.txt')    
}
GENOMES_KEYS = list(GENOMES.keys())

BASES = ['A','C','G','T']
BASES_COMPLEMENTS = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

class Plots(Enum):
    COUNTS_RAW = 'Counts'
    COUNTS_PCT = 'Counts (%)'
    COUNTS_PCT_BASE = 'Counts Centered (%)'
    COUNTS_PCT_DIFF = 'Counts Diff(%)'
    SKEW = 'Skew'
    TEST = 'Test'

ENABLED_PLOTS = [Plots.COUNTS_PCT_BASE, Plots.COUNTS_PCT_DIFF, Plots.SKEW]

def genome(key):
  if key not in GENOMES_KEYS:
    raise Exception(f"invalid key {key}")
  with open(GENOMES[key]) as f: return f.read().strip().replace('\n','')