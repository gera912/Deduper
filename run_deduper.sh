#!/bin/bash

#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --job-name=Deduper
#SBATCH --output=slurm-%j-%x.out

#SBATCH --time=0-24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=7

conda deactivate
conda deactivate
conda deactivate
conda deactivate
conda activate bgmp_py3

file1="/projects/bgmp/shared/deduper/Dataset1.sam"
file2="/projects/bgmp/shared/deduper/Dataset2.sam"
file3="/projects/bgmp/shared/deduper/Dataset3.sam"


/usr/bin/time -v python  perez_deduper.py -f $file1
/usr/bin/time -v python  perez_deduper.py -f $file2
/usr/bin/time -v python  perez_deduper.py -f $file3
