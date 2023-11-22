# Bioinformatics 

This repo has my code, notes and visualizations from the courses in the [Coursera Bioinformatics specialization](https://www.coursera.org/specializations/bioinformatics).

[x] [Bioinformatics I](https://www.coursera.org/learn/dna-analysis/home) - completed  

[x] [Bioinformatics II](https://www.coursera.org/learn/genome-sequencing/home) - in progress

Some of these problems are also on [Rosalind](https://rosalind.info/problems/locations/). 

**Setup**
```bash
$ virtualenv ./venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

**Run**

Use the `Justfile` to run if you have `just` installed:
```bash
just part1_week1 #run code & tests for each week/part
just web #run vis webserver
```

or use bash:
```bash
$ source venv/bin/activate
$ cd src
$ python3 wsgi.py #run vis webserver
$ python3 -m part1.week1.py #run code & tests for each week/part
$ python3 lib.py #run tests
```

**Todos**

- fix tests to not hardcode file path but not run tests from imported files.