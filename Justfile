set shell := ["bash","-c"]
web:
  #!/bin/bash
  cd src && uv run python wsgi.py
part1_week1:
  cd src && uv run python -m part1.week1
part1_week2:
  cd src && uv run python -m part1.week2
part1_week3:
  cd src && uv run python -m part1.week3
part1_week4:
  cd src && uv run python -m part1.week4
part2_week1:
  cd src && uv run python -m part2.week1
part2_week2:
  cd src && uv run python -m part2.week2
rr:
  cargo run --release

alias w    := web
alias p1w1 := part1_week1
alias p1w2 := part1_week2
alias p1w3 := part1_week3
alias p1w4 := part1_week4
alias p2w1 := part2_week1
alias p2w2 := part2_week2
