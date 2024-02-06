### System Requirements
Ubuntu 14.04 Server/Desktop

### Deployment process
#### 1. Install related environment and dependent libraries
sudo apt-get install gcc g++ python  <br>
sudo apt-get install gcc g++ python python-dev
sudo apt-get install mercurial
sudo apt-get install bzr
sudo apt-get install gdb valgrind
sudo apt-get install gsl-bin libgsl0-dev libgsl0ldbl
sudo apt-get install flex bison libfl-dev
sudo apt-get install g++-3.4 gcc-3.4
sudo apt-get install tcpdump
sudo apt-get install sqlite sqlite3 libsqlite3-dev
sudo apt-get install libxml2 libxml2-dev
sudo apt-get install libgtk2.0-0 libgtk2.0-dev
sudo apt-get install vtun lxc
sudo apt-get install uncrustify
sudo apt-get install doxygen graphviz imagemagick
sudo apt-get install texlive texlive-extra-utils texlive-latex-extra
sudo apt-get install python-sphinx dia
sudo apt-get install python-pygraphviz python-kiwi python-pygoocanvas libgoocanvas-dev
sudo apt-get install libboost-signals-dev libboost-filesystem-dev

#### 2. Deploy project
Download the project and place it in a custom directory (such as /home/ERD/)
cd /home/ERD/

Configure waf
./waf configure
./waf

Run the test:
Execute Python ./sim_run.py

Result output
After executing the test, the results will be output to the /home/ERD/sim/ directory, and the specific corresponding results are determined by sim-main.conf

#### 3. Test instructions
1) You can open the /home/ERD/sim-main-sample.conf file, which contains the test configurations of four scenarios as a reference.
2) After executing the test, the results will be automatically generated to /home/ERD/sim/{scenario name}/out_res_xx.txt.
3) The configuration and results of this real test scenario are stored in the /home/ERD/output directory.

#### 4. Configuration instructions
Explain the functions of the main fields in sim-main.conf.
**conf_name**: Specify the names of the input reference files and output result files, which should correspond to the file names in the /ERD/ directory and generally do not need to be modified.
**active**: Whether to enable this scenario test, set to false, and ignore this scenario during testing.
**conf_path**: The directory where the test result file is output, relative to the /ERD/ directory, generally does not need to be modified.
**unit**: The format of the output value can be all, s, ms, us, or ns, corresponding to the original value, seconds, milliseconds, microseconds, and nanoseconds respectively.
**decimals**: Specifies the number of decimal points retained by the output value.
**struct**: Array structure, which contains multiple test objects. The difference between each object is that a different number of nodes can be specified.
**nodeCount**: Specify the number of nodes for this test object during this test.
**compareSet**: Array structure, specifying different comparison scenarios. For example, all under 8 nodes, there are three test scenarios: RC, XRC and ERD.
**isBase**: Whether it is a reference object for comparison. For example, if XRC and ERD need to be compared with RC, then RC is set to true. This parameter is valid in goodput and throughput scenarios.
**lossRate**: Packet loss rate. If the packet loss rate is set to a large value, data loss may easily occur and the results cannot be counted. This parameter is valid in the goodput scenario.
**bandWidth**: Set the bandwidth value for the test, in Gbps.
**linkDelay**: Set the transmission delay of each link, in ms.
**payloadSize**: Set the size of data to be transmitted each time, in byte.
descript: The output description name corresponding to a single test item in compareSet, which is output to out_res_xx.txt together with the test results.
​
