import calc_run.py

def test_rd():
  assert calc_run.rd(3.0) == 3.0
  assert calc_run.rd(3.14) == 3.1
  assert calc_run.rd(3.15) == 3.2
  assert calc_run.rd(-1.15) == -1.2
 
