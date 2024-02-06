#### 4. Configuration instructions
Explain the functions of the main fields in sim-main.conf.  <br>

+ **conf_name**: Specify the names of the input reference files and output result files, which should correspond to the file names in the /ERD/ directory and generally do not need to be modified.  <br>
+ **active**: Whether to enable this scenario test, set to false, and ignore this scenario during testing.  <br>
+ **conf_path**: The directory where the test result file is output, relative to the /ERD/ directory, generally does not need to be modified.  <br>
+ **unit**: The format of the output value can be all, s, ms, us, or ns, corresponding to the original value, seconds, milliseconds, microseconds, and nanoseconds respectively.  <br>
+ **decimals**: Specifies the number of decimal points retained by the output value.  <br>
+ **struct**: Array structure, which contains multiple test objects. The difference between each object is that a different number of nodes can be specified.  <br>
+ **nodeCount**: Specify the number of nodes for this test object during this test.  <br>
+ **compareSet**: Array structure, specifying different comparison scenarios. For example, all under 8 nodes, there are three test scenarios: RC, XRC and ERD.  <br>
+ **isBase**: Whether it is a reference object for comparison. For example, if XRC and ERD need to be compared with RC, then RC is set to true. This parameter is valid in goodput and throughput scenarios.  <br>
+ **lossRate**: Packet loss rate. If the packet loss rate is set to a large value, data loss may easily occur and the results cannot be counted. This parameter is valid in the goodput scenario.  <br>
+ **bandWidth**: Set the bandwidth value for the test, in Gbps.  <br>
+ **linkDelay**: Set the transmission delay of each link, in ms.  <br>
+ **payloadSize**: Set the size of data to be transmitted each time, in byte.  <br>