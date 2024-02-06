# ERD
ERD is an RDMA QP communication mechanism used for AI HPC cluster network protocol design.

### System Requirements
Ubuntu 14.04 Server/Desktop

### Deployment process
#### 1. Install related environment and dependent libraries
sudo apt-get install gcc g++ python  <br>
sudo apt-get install gcc g++ python python-dev  <br>
sudo apt-get install mercurial  <br>
sudo apt-get install bzr  <br>
sudo apt-get install gdb valgrind  <br>
sudo apt-get install gsl-bin libgsl0-dev libgsl0ldbl  <br>
sudo apt-get install flex bison libfl-dev  <br>
sudo apt-get install g++-3.4 gcc-3.4  <br>
sudo apt-get install tcpdump  <br>
sudo apt-get install sqlite sqlite3 libsqlite3-dev  <br>
sudo apt-get install libxml2 libxml2-dev  <br>
sudo apt-get install libgtk2.0-0 libgtk2.0-dev  <br>
sudo apt-get install vtun lxc  <br>
sudo apt-get install uncrustify  <br>
sudo apt-get install doxygen graphviz imagemagick  <br>
sudo apt-get install texlive texlive-extra-utils texlive-latex-extra  <br>
sudo apt-get install python-sphinx dia  <br>
sudo apt-get install python-pygraphviz python-kiwi python-pygoocanvas libgoocanvas-dev  <br>
sudo apt-get install libboost-signals-dev libboost-filesystem-dev  <br>

#### 2. Deploy project
* Download the project and place it in a custom directory (such as /home/ERD/)  <br>
cd /home/ERD/  <br>
  <br>
* Configure waf  <br>
./waf configure  <br>
./waf  <br>
  <br>
* Run the test:  <br>
Execute Python ./sim_run.py  <br>
  <br>
* Result output  <br>
After executing the test, the results will be output to the /home/ERD/sim/ directory, and the specific corresponding results are determined by sim-main.conf  <br>

#### 3. Test instructions
1) You can open the /home/ERD/sim-main-sample.conf file, which contains the test configurations of four scenarios as a reference.  <br>
2) After executing the test, the results will be automatically generated to /home/ERD/sim/{scenario name}/out_res_xx.txt.  <br>
3) The configuration and results of this real test scenario are stored in the /home/ERD/output directory.  <br>

#### 4. Configuration instructions
Explain the functions of the main fields in sim-main.conf.  <br>
  <br>
**conf_name**: Specify the names of the input reference files and output result files, which should correspond to the file names in the /ERD/ directory and generally do not need to be modified.  <br>
**active**: Whether to enable this scenario test, set to false, and ignore this scenario during testing.  <br>
**conf_path**: The directory where the test result file is output, relative to the /ERD/ directory, generally does not need to be modified.  <br>
**unit**: The format of the output value can be all, s, ms, us, or ns, corresponding to the original value, seconds, milliseconds, microseconds, and nanoseconds respectively.  <br>
**decimals**: Specifies the number of decimal points retained by the output value.  <br>
**struct**: Array structure, which contains multiple test objects. The difference between each object is that a different number of nodes can be specified.  <br>
**nodeCount**: Specify the number of nodes for this test object during this test.  <br>
**compareSet**: Array structure, specifying different comparison scenarios. For example, all under 8 nodes, there are three test scenarios: RC, XRC and ERD.  <br>
**isBase**: Whether it is a reference object for comparison. For example, if XRC and ERD need to be compared with RC, then RC is set to true. This parameter is valid in goodput and throughput scenarios.  <br>
**lossRate**: Packet loss rate. If the packet loss rate is set to a large value, data loss may easily occur and the results cannot be counted. This parameter is valid in the goodput scenario.  <br>
**bandWidth**: Set the bandwidth value for the test, in Gbps.  <br>
**linkDelay**: Set the transmission delay of each link, in ms.  <br>
**payloadSize**: Set the size of data to be transmitted each time, in byte.  <br>
------------     <br> 
descript: The output description name corresponding to a single test item in compareSet, which is output to out_res_xx.txt together with the test results.  <br>
​
