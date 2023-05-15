# 52040-final-project
Final project for distributed systems.

# Overview
The performance evaluation info is contained in the performance_evlaution directory such as information on how to run performance informance.

## Notes

The individual components of this system all seemed to work properly, but some of the communication (i.e. between the workers and task_dispatcher) I was confused on exactly what to do, so I read online different approaches and picked the best one,

Some of the error handling I missed.

I note this in the performance_report.md, but the speedup depending on the workers was not as great since the task_dispatcher waits until it recieves results from the workers to then push to redis. This is what I understood the project was suppose to do, but I do not believe is the most efficient approach since I could have had the workers just push to redis themselves thus freeing up the task dispatcher. I note this in the report file, but I might have misunderstood.

### To run the tests that were supplied I ran each component (task_dispatcher, worker, main app) seperately.

## References

https://zguide.zeromq.org/docs/chapter3/#The-DEALER-to-ROUTER-Combination
https://blog.devgenius.io/how-to-use-redis-pub-sub-in-your-python-application-b6d5e11fc8de
https://www.ibm.com/topics/faas
https://medium.com/code-chasm/go-concurrency-pattern-worker-pool-a437117025b1
