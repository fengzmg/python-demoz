To run the example, you need to install pywebsocket.

## Install pywebsocket

Download mod_pywebsocket-x.x.x.tar.gz from pywebsocket which aims to provide a Web Socket extension for Apache HTTP Server ans install it following these steps.

Unzip and untar the downloaded file.

Go inside pywebsocket-x.x.x/src/ directory.

    python setup.py build

    sudo python setup.py install

Then read document by:

    pydoc mod_pywebsocket
    
This will install it into your python environment.

## Start the Server

Go to the pywebsocket-x.x.x/src/mod_pywebsocket folder and run the following command:

    sudo python standalone.py -p 9998 -w ../example/

This will start the server listening at port 9998 and use the handlers directory specified by the -w option where our echo_wsh.py resides.

Now using Chrome browser open the html file your created in the beginning. If your browser supports WebSocket(), then you would get alert indicating that your browser supports WebSoc
