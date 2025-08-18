pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = '923714621804.dkr.ecr.us-east-1.amazonaws.com/cloudtracking'
        IMAGE_TAG = "${BUILD_NUMBER}"
        LOCAL_IMAGE_NAME = "cloudtrack-app"  // from docker-compose.yaml
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image via Compose') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Login to AWS ECR') {
            steps {
                withAWS(credentials: 'aws-creds', region: "${AWS_REGION}") {
                    sh '''
                      aws ecr get-login-password --region ${AWS_REGION} \
                      | docker login --username AWS --password-stdin ${ECR_REPO}
                    '''
                }
            }
        }

        stage('Tag and Push to ECR') {
            steps {
                sh """
                  docker tag ${LOCAL_IMAGE_NAME}:latest ${ECR_REPO}:${IMAGE_TAG}
                  docker push ${ECR_REPO}:${IMAGE_TAG}
                """
            }
        }
    }
}
