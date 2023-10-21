## Code and notes from [Coursera Bioinformatics I](https://www.coursera.org/learn/dna-analysis/home) course

These problems are also on [Rosalind](https://rosalind.info/problems/locations/). Also includes some visualizations.

**Setup**
```bash
$ virtualenv ./venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

**Running**

Then either launch the visualizations server:
```bash
$ ./server.sh # To launch dash/plotly server
```

or run the files with code & tests for each week:

```bash
$ source venv/bin/activate
$ python3 week1.py #to run week1/2/3...
$ python3 lib.py #run tests
```

**Todos**

- fix tests to not hardcode file path but not run tests from imported files.