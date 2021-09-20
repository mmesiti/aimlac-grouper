# Usage

Note: in the following, `X` is going to be 0 or 1. 

- Fill the `Software dev Expertise` column
  in `cohort.202X.csv` 
  with integer values between 0 and 2 
- run
  ```
  ./make_groups.py 4 cohort.202X.csv
  ```
  to make 4 groups.
  Change 4->N if you want N groups.
  Note: with less than 4 groups,
  we get institution/theme repetitions.
- A plot with diagnostics 
  of the simulated annealing
  is going to be shown, 
  and the teams.

# Parameters & Inner workings
- All the parameters 
  can be tweaked inside `make_groups.py`.
- the cost function can be tweaked 
  in the `cost.py` file. 
  There is a contribution 
  due to pair interactions
  (which can be split between 
  categorical
  and numerical dimensions)
  and contributions 
  due to "global" imbalances. 
  
# Note on privacy
  All data in `cohort.202X.csv` 
  comes from http://cdt-aimlac.org/cdt-cohorts.html
  and is thus publicly available,
  except from the `Software dev Expertise` column
  which is random data.
