#!/usr/bin/env python
from fetch import get_basketball_courts_summary
from clear import clear

if __name__ == "__main__":
  clear()
  summary = get_basketball_courts_summary()
  print(summary)

