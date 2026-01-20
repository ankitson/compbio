# Bioinformatics 

This repo has my code, notes and visualizations from the courses in the [Coursera Bioinformatics specialization](https://www.coursera.org/specializations/bioinformatics).

[x] [Bioinformatics I](https://www.coursera.org/learn/dna-analysis/home) - completed  

[x] [Bioinformatics II](https://www.coursera.org/learn/genome-sequencing/home) - in progress

Some of these problems are also on [Rosalind](https://rosalind.info/problems/locations/). 

**Setup**
```bash
$ uv sync
```

**Run**

Use the `Justfile` to run if you have `just` installed:
```bash
just part1_week1 #run code & tests for each week/part
just web #run vis webserver
```

or use bash:
```bash
$ cd src
$ uv run python wsgi.py #run vis webserver
$ uv run python -m part1.week1 #run code & tests for each week/part
$ uv run python lib.py #run tests
```

**Todos**

- Use text dumps or something to version SQLITE DB instead of committing the binary
https://news.ycombinator.com/item?id=38110286
https://garrit.xyz/posts/2023-11-01-tracking-sqlite-database-changes-in-git
https://datasette.io/tools/sqlite-diffable
