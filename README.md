# ERD
ERD is an RDMA QP communication mechanism used for AI HPC cluster network protocol design, simulation based on NS-3 platform.

### System Requirements
Ubuntu 14.04 Server/Desktop

### Deployment process
#### 1. Install related environment and dependent libraries
```
sudo apt-get install gcc g++ python
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
```

#### 2. Deploy project
* Download the project and place it in a custom directory (such as /home/ERD/)  <br>
```
cd /home/ERD/
```

* Configure waf  <br>
```
./waf configure 
./waf 
```

* Run the test:  <br>
Execute Python `./sim_run.py`  <br>

* Result output  <br>
After executing the test, the results will be output to the `/home/ERD/sim/` directory, and the specific corresponding results are determined by sim-main.conf  <br>

#### 3. Test instructions
1) You can open the `/home/ERD/sim-main-sample.conf` file, which contains the test configurations of four scenarios as a reference.  <br>
2) After executing the test, the results will be automatically generated to `/home/ERD/sim/{scenario name}/out_res_xx.txt`.  <br>
3) The configuration and results of this real test scenario are stored in the `/home/ERD/output` directory.  <br>


------------     <br> 
Descript: The output description name corresponding to a single test item in compareSet, which is output to out_res_xx.txt together with the test results.  <br>
​
