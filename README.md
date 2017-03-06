# RelNet
**RelNet** is a context-driven, multi-tasking, and recurrent deep learning model. RelNet uses context features (such as topic embeddings) to reinforce learning relevant NLP tasks. RelNet comes in two flavors: the CCRNN (Contextual Cascaded Recurrent Neural Network) and the MCRNN (Multi-tasking Contextual Recurrent Neural Network). 

RelNet has been trained on various tasks such as missing word prediction to hashtag recommendation using a diverse set of text corpuses including Twitter, Reuters, and IMDB.

A side project of RelNet resulted in the ***Infinite Data Pipeline*** which is built on Java, Apache Storm, Kafka, and the Twitter API. The Infinite Data Pipeline streams and preprocesses Twitter data online and directly injects the streamed data into a running Tensorflow topology. 

## Requirements:
1. CUDNN (tested on cuDNN 5105)
2. CUDA Drivers + NVIDIA Graphics Card with 5.0+ support (tested on GTX 1080)
3. Apache Zookeeper (tested on version 3.4.6)
4. Apache Storm (tested on version 0.9.5)
5. Twitter API + Developer Credentials (tested on version 4.0.4)
6. Theano (tested on version 0.8.2)
7. Keras (tested on latest version as of January 9, 2017)
8. Linux Based OS (tested on Ubuntu 16.04LTS)

## Install Guide:
1. [Install CUDA and cuDNN](http://www.pyimagesearch.com/2016/07/04/how-to-install-cuda-toolkit-and-cudnn-for-deep-learning/)
2. [Apache Storm and Twitter API Setup](https://www.tutorialspoint.com/apache_storm/apache_storm_installation.htm)
3. [Install keras and Theano](http://www.pyimagesearch.com/2016/07/18/installing-keras-for-deep-learning/)

## Data Miner Run Guide (MacOSX Local):
1. Run **systemStartMac.sh** to start your *Storm* instance. 
2. Run **runAPI.sh** to open the *Twitter* stream and start collection. (Requires you to edit **runAPI.sh** with correct *Twitter* API credentials).

## Data Miner Run Guide (Ubuntu 16.04 Local):
1. Run **systemStartMac.sh** to start your *Storm* instance. 
2. Run **runAPI.sh** to open the *Twitter* stream and start collection. (Requires you to edit **runAPI.sh** with correct *Twitter* API credentials).

## Tweetnet Run Guide:
1. Run **tweetnet.py**.

## Notes:

**Note**: The system start script opens four new terminals; *Apache Zookeeper*, the *Nimbus*, the *Supervisor*, and *StormUI*. Each new open terminal requires **sudo** access and will request for the user's password. To view *StormUI* you can navigate to *localhost:8080*. 

**Note**: In the CUDA setup, the section where you link cuda to cuda-7.5 is outdated. 

Intead of following this step:

    export CUDA_HOME=/usr/local/cuda-7.5

Make sure you using and linking *CUDA v8.0*:

    export CUDA_HOME=/usr/local/cuda-8.0

**Note**: You will need to register for Twitter Developer credentials to run the data miner.
