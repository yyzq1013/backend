pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
metadata:
  namespace: jenkins
spec:
  containers:
  - name: python
    image: python:3.11-slim
    command:
    - sleep
    args:
    - 99d
'''
        }
    }

    stages {
        stage('Python Version') {
            steps {
                container('python') {
                    sh 'python3 --version'
                }
            }
        }
    }
}