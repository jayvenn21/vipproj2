under construction

dependencies: 
pip install transformers torch sentencepiece scikit-learn accelerate

how to run:
python main_gui.py

for each feature:
- Summarize (t5-base): place some text as input
- Translate (Helsinki-NLP/opus-mt-{source}-{target}): place some text as input and choose source language and target language
- Answer Question (t5-base): Line 1: context (text that contains the answer), Line 2: the question
- Classify (sentiment analysis): place some sentence or paragraph as input

REMOTE HPC INSTRUCTIONS:
Differences: The program connects remotely to a HPC and runs the AI on there instead of on your local machine. 
It will display the result on your local machine.
As this program is not published yet and is still in testing, some setup needs to be done:

SETUP INSTRUCTIONS
1. Generate an id_rsa public/private pair using the following command on your local machine:
ssh-keygen -t rsa -b 4096 -C "username@host"
Replace "username@host" with what you use to log on to your HPC cluster
2. If it's not there, put the public id_rsa in the .ssh folder of your hpc cluster: cd .ssh and use scp
Seeing as only students of Georgia Tech should be reading this nonfinal version of the README, and it was there already for me, you should probably be fine already
3. Make a secret.py file.
Include the following 5 variables:
HPC_USER = your username, whatever is before the @ in what you use to login
HPC_HOST = the host of the HPC, whatever is after the @ in what you use to login
REMOTE_INPUT_FILE = The absolute path to your desired prompt.txt location in your HPC
REMOTE_OUTPUT_FILE = The absolute path to your desired prompt.txt location in your HPC
HPC_JOB_SCRIPT = The path to your desired jobscript.sh location. Does not have to be the absolute path
To get the absolute filepath you can use pwd or realpath
NOTE: Put secret.py in the .gitignore
4. Clone the repository in the HPC
5. scp your secrets file into the HPC
6. run "python main_hpc.py" from the local directory

DEBUGGING:
If you want error logs, add the following line to the start of your jobscript.sh on the HPC:
#SBATCH -oReport-%j.out
More of a note to self, but if you want to remove all your report logs, use "rm Report*" in the directory of your report logs

KNOWN ISSUES:
"Answer Question" response not displaying properly when using the HPC version of the program
