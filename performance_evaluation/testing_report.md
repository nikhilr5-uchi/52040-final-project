To test the solutions first fire up the sever using

`uvicorn main:app --reload`

Then fire up redis using

`redis-server`

Now final run to get the output of runtimes.

`python performance_evaluation/performance_evalutation.py`

This python file tests for push and pull workers where the problem size and number of tasks increase (1 worker == 5 tasks, 2 workers == 10 tasks, 4 workers == 20 tasks, 8 workers == 40 tasks).

The output is the amount of time it took to complete all the tasks.

It tests it on running the double function defined in the file on a given set of inputs. 