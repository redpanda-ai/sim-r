==============================
sim-r (pronounded "simmer") Microservice
==============================


The sim-r microservice uses the `Connexion`_ Python library.

Connexion is a framework on top of Flask_ to automagically handle your REST API requests
based on `Swagger 2.0 Specification`_ files in YAML.


Features
========

This application shows various features supported by the Connexion library:

* mapping of REST operations to Python functions (using the ``operationId`` in ``swagger.yaml``)

  * maps path, query and body parameters to keyword arguments

* bundled Swagger UI (served on `/ui/`_ path)
* automatic JSON serialization for ``application/json`` content type
* schema validation for the HTTP request body and query parameters:

  * required object properties
  * primitive JSON types (string, integers, etc)
  * date/time values
  * string lengths
  * minimum/maximum values
  * regular expression patterns


Directory Structure, using `Linc Global's Standard Directory Layout`_
=====================================================================

* ``Dockerfile``: builds a runnable Docker image
* ``requirements.txt``: list of required Python libraries
* ``main/config/config.yaml``: configuration for the application
* ``main/data/train/*``: training data for our Machine Learning models
* ``main/src/server/swagger.yaml``: REST API Swagger definition
* ``main/src/app/*.py``: business logic modules
* ``main/src/db/*.py``: database connectivity modules
* ``main/src/server/service.py``: the primary web service module

Deploy Locally with Python 3
============================

You can run the Python application directly on your local operating system:

.. code-block:: bash

    # create your python3 virtual environment
    PROJECT=sim-r
    conda env create -f environment.yml
    # activate your virtual environment
    source activate ${PROJECT}
    # install required python libraries
    pip install -r requirements.txt
    # start the microservice
    python -m main.src.server.service 8080

Deploy with Kubernetes onto AWS
=========================================

.. code-block:: bash

    # 1. Build and tag your docker images
    PROJECT=sim-r
    docker build -t ${PROJECT}:v1 .

    # 2. Provide a target tag for your image for the remote repository
    # NOTE: Replace your_docker_repo with a repository you can write to
    DOCKER_REPO=your_docker_repo
    docker tag ${PROJECT}:v1 ${DOCKER_REPO}/${PROJECT}

    # 3. Push your docker image to the remote repository
    docker push ${DOCKER_REPO}/${PROJECT}

    # 4. Switch to the following context
    alias kubectl="kubectl --kubeconfig main/config/kube_config"
    kubectl config use-context myfirstcluster.letslinc.com

    # 5. Run your image on the named cluster
    kubectl run ${PROJECT} --image=${DOCKER_REPO}/${PROJECT}

    # 6. Expose your named deployment on port 80
    kubectl expose deployment ${PROJECT} --port=80 --type=LoadBalancer

    # 7. Obtain your DNS
    # NOTE: You'll have to wait about 60 seconds before the service starts
    kubectl get services -o wide | grep ${PROJECT} | awk ' { print $1 "\t" $3 "/ui/" } '

Optional Kubernetes/AWS commands
================================

.. code-block:: bash

    # To get your pod id
    PROJECT=sim-r
    kubectl get pods

    # To view your pod logs (use the [POD_ID] from the previous command)
    kubectl logs ${PROJECT}-[POD_ID]


Un-deploy from AWS
================================

.. code-block:: bash

    # First delete the deployment
    PROJECT=sim-r
    $ kubectl delete deployment ${PROJECT} && kubectl get deployments

    # Then delete the service
    $ kubectl delete service ${PROJECT} && kubectl get services


.. _Connexion: https://pypi.python.org/pypi/connexion
.. _Flask: http://flask.pocoo.org/
.. _Swagger 2.0 Specification: https://github.com/swagger-api/swagger-spec/blob/master/versions/2.0.md
.. _/ui/: http://localhost:8080/ui/
.. _using Flask with uWSGI: http://flask.pocoo.org/docs/latest/deploying/uwsgi/
.. _uWSGI documentation: https://uwsgi-docs.readthedocs.org/
.. _this guide: https://kubernetes.io/docs/getting-started-guides/ubuntu/
.. _Linc Global's Standard Directory Layout: https://letslinc.atlassian.net/wiki/spaces/EP/pages/69533697/Docker+Service+Structure

