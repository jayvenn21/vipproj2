#!/bin/bash
#SBATCH -N1 -n1                         
#SBATCH --mem-per-cpu=16G               
#SBATCH -t15                             
#SBATCH -oReport-%j.out   

TASK=$1
INPUT_FILE=$2
OUTPUT_FILE=$3

echo "Running $TASK..."
case $TASK in
  ("Summarize")
    srun python ~/vipproj2/summarize.py --input "$INPUT_FILE" --output "$OUTPUT_FILE"
    ;;
  ("Translate")
    srun python ~/vipproj2/translate.py --input "$INPUT_FILE" --output "$OUTPUT_FILE"
    ;;
  ("Answer Question")
    srun python ~/vipproj2/qa.py --input "$INPUT_FILE" --output "$OUTPUT_FILE"
    ;;
  ("Classify")
    srun python ~/vipproj2/classify.py --input "$INPUT_FILE" --output "$OUTPUT_FILE"
    ;;
  (*)
    echo "Unknown task: $TASK"
    exit 1
    ;;
esac