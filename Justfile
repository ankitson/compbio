set shell := ["bash","-c"]
web:
  #!/bin/bash
  source venv/bin/activate
  cd src && python3 wsgi.py
part1_week1:
  source venv/bin/activate
  cd src && python3 -m part1.week1
part1_week2:
  source venv/bin/activate
  cd src && python3 -m part1.week2
part1_week3:
  source venv/bin/activate
  cd src && python3 -m part1.week3
part1_week4:
  source venv/bin/activate
  cd src && python3 -m part1.week4
part2_week1:
  source venv/bin/activate
  cd src && python3 -m part2.week1