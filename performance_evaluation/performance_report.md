The result I got when running the performance_evalutation.py is:

{'local': [0.052641647999999985, 0.06868050100000003, 0.12462108700000002], 
'push': [0.035110132000000016, 0.064172589, 0.12108545100000001, 0.3668141829999999], 
'pull': [0.051844507999999956, 0.06669162399999995, 0.12620875499999995, 0.27096458]}

As we can see the push and pull performed rather similar. The pull with many workers we can see that it runs faster than push. I think this is because getting many dealer sockets set up for the workers for push takes a long time.

We can see with running locally is just as fast as push and pull.

I believe that all the different types of workers are the same since even when distributing the work to workers on different nodes (i.e. pull or push) we are still waiting for the response to be returned to task_dispatcher. If instead the workers pushed the results to redis itself I believe that the speedup we would see would be significant. 