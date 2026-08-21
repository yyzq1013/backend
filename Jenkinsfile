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
    image: python:3.11-slim
    command:
    - sleep
    args:
    - 99d
    tty: true

  - name: kubectl
    image: bitnami/kubectl:1.33
    command:
    - sleep
    args:
    - 99d
    tty: true

  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
    - sleep
    args:
    - 99d
    tty: true
    volumeMounts:
    - name: docker-config
      mountPath: /kaniko/.docker

  volumes:
  - name: docker-config
    secret:
      secretName: dockerhub-secret
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
                        /kaniko/executor                           --context $WORKSPACE                           --dockerfile Dockerfile                           --destination $REGISTRY/$IMAGE:$IMAGE_TAG                           --destination $REGISTRY/$IMAGE:latest                           --insecure                           --skip-tls-verify
                    '''
                }
            }
        }

        stage('Deploy to k3s') {
            steps {
                container('kubectl') {
                    sh '''
                        kubectl set image deployment/$DEPLOYMENT                           $CONTAINER=$REGISTRY/$IMAGE:$IMAGE_TAG                           -n $NAMESPACE
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