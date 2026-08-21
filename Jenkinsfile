pipeline {

    agent {
        kubernetes {

            yaml """
apiVersion: v1
kind: Pod

spec:
  serviceAccountName: jenkins

  containers:

  - name: python
    image: 192.168.0.48:5000/python
    imagePullPolicy: Always
    command:
    - sleep
    args:
    - 99d
    tty: true

  - name: kubectl
    image: 192.168.0.48:5000/kubectl:latest
    imagePullPolicy: Always
    command:
    - sleep
    args:
    - 99d
    tty: true

  - name: kaniko
    image: 192.168.0.48:5000/kaniko-shell:latest
    imagePullPolicy: Always
    command:
    - /bin/sh
    - -c
    args:
    - |
      while true; do
        sleep 3600
      done
    tty: true
"""
        }
    }

    environment {

        REGISTRY = "192.168.0.48:5000"
        IMAGE = "backend"
        IMAGE_TAG = "${BUILD_NUMBER}"

        DEPLOYMENT = "backend"
        CONTAINER = "backend"

        NAMESPACE = "default"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment') {
            steps {
                container('python') {
                    sh '''
                        echo "===== Workspace ====="
                        pwd
                        ls -al

                        echo "===== Python ====="
                        python3 --version
                        pip3 --version
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                container('python') {
                    sh '''
                        pip install --no-cache-dir -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Test') {
            steps {
                container('python') {
                    sh '''
                        pytest -v
                    '''
                }
            }
        }

        stage('Build & Push Image') {
            steps {
                container('kaniko') {
                    sh '''
                    /kaniko/executor \
                        --context $WORKSPACE \
                        --dockerfile Dockerfile \
                        --destination 192.168.0.48:5000/backend:${BUILD_NUMBER} \
                        --destination 192.168.0.48:5000/backend:latest \
                        --insecure \
                        --skip-tls-verify
                    '''
                }
            }
        }

        stage('Deploy to k3s') {
            steps {
                container('kubectl') {
                    sh '''
                        set -eux

                        echo "HELLO FROM KUBECTL"

                        kubectl version --client

                        kubectl get pods -n default

                        echo "DEPLOY TEST FINISHED"
                    '''
                }
            }
        }

        stage('Verify Rollout') {
            steps {
                container('kubectl') {
                    sh '''
                        kubectl rollout status deployment/$DEPLOYMENT                           -n $NAMESPACE                           --timeout=180s

                        kubectl get pods -n $NAMESPACE -o wide
                    '''
                }
            }
        }
    }

    post {

        success {
            echo "=============================="
            echo "Build SUCCESS!"
            echo "Image: $REGISTRY/$IMAGE:$IMAGE_TAG"
            echo "Deployment Updated Successfully."
            echo "=============================="
        }

        failure {
            echo "=============================="
            echo "Build FAILED!"
            echo "=============================="
        }

        always {
            cleanWs()
        }
    }
}