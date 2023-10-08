import os
GENOMES = {
    'e_coli': os.path.abspath('inputs/E_coli_genome.txt'),
    'salmonella': os.path.abspath('inputs/Salmonella_enterica.txt'),
    'cholera': os.path.abspath('inputs/Vibrio_Cholera_Genome.txt')    
}
GENOMES_KEYS = list(GENOMES.keys())