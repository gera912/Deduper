#!/bin/bash



#SBATCH --account=bgmp
#SBATCH --partition=bgmp
#SBATCH --job-name=Sam_sort
#SBATCH --output=slurm-%j-%x.out

#SBATCH --time=0-01:00:00
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

/usr/bin/time -v samtools view -bh $file1 > Dataset1.out.bam
/usr/bin/time -v  samtools sort Dataset1.out.bam -o Dataset1.sort.bam
/usr/bin/time -v samtools sort  Dataset1.out.bam -o Dataset1.sort.sam

/usr/bin/time -v samtools view -bh $file2 > Dataset2.out.bam
/usr/bin/time -v  samtools sort Dataset2.out.bam -o Dataset2.sort.bam
/usr/bin/time -v samtools sort  Dataset2.out.bam -o Dataset2.sort.sam


/usr/bin/time -v samtools view -bh $file3 > Dataset3.out.bam
/usr/bin/time -v  samtools sort Dataset3.out.bam -o Dataset3.sort.bam
/usr/bin/time -v samtools sort  Dataset3.out.bam -o Dataset3.sort.sam
