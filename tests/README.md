# PRINT LEV GROUPS

This prints out groups of similar fields for a given input of files or stdin. The similarity is measured by the [Levenshtein edit distance](https://en.wikipedia.org/wiki/Levenshtein_distance).

You can put in the similarity factor as a number between 0 and 100, where 0 matches almost everything, and 100 looks for exact matches.

## Requirements

This project uses python3.5, python2.7 may work but is not guarenteed.

You require the following python packages to run

- fuzzywuzzy (0.15.0)
- networkx (1.11)
- python-Levenshtein (0.12.0)
- matplotlib (2.0.2)

Which you can install using pip

```bash
pip3 install fuzzywuzzy networkx python-Levenshtein matplotlib
```


## Usage

```bash
# Get the latest snapshot
git clone --depth=1 https://github.com/maabdelatif/print-lev-groups.git myproject

# Change directory
cd myproject

# Run the script against the sample first-names.txt files and 60 as the similarity percentage
python3 print_lev_groups.py --files small-file.txt --ratio 60
```

## Disclaimer

Please do not use this for any production code

### Credits

* StackOverflow

* The first-names.txt example file is from https://github.com/dominictarr/random-name/blob/master/first-names.txt

