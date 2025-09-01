pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID = '923714621804'
        AWS_REGION     = 'us-east-1'
        CLUSTER_NAME   = 'cloudautomation_cluster'
        SERVICE_NAME   = 'cloudtrack-task-service-v6tmpjqz'
        TASK_FAMILY    = 'cloudtrack-task'
        REPO_URL       = 'https://github.com/poojiroy/CloudAutomation.git'
        ECR_REPO       = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/cloudautomation"
        IMAGE_TAG      = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: "${env.REPO_URL}"
            }
        }

        stage('Login to ECR') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                                  credentialsId: 'aws-creds']]) {
                    sh '''
                    aws ecr get-login-password --region $AWS_REGION \
                      | docker login --username AWS --password-stdin $ECR_REPO
                    '''
                }
            }
        }

        stage('Build & Push with docker-compose') {
            steps {
                sh '''
                ECR_REPO=$ECR_REPO IMAGE_TAG=$IMAGE_TAG docker-compose build
                ECR_REPO=$ECR_REPO IMAGE_TAG=$IMAGE_TAG docker-compose push
                '''
            }
        }

        stage('Register New Task Definition Revision') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                                  credentialsId: 'aws-creds']]) {
                    sh '''
                    aws ecs describe-task-definition --task-definition $TASK_FAMILY \
                      --region $AWS_REGION \
                      --query taskDefinition > taskdef.json

                    cat taskdef.json | \
                      jq --arg IMAGE "$ECR_REPO:$IMAGE_TAG" \
                      '.containerDefinitions[0].image=$IMAGE
                       | del(.taskDefinitionArn, .revision, .status, .requiresAttributes, .compatibilities, .registeredAt, .registeredBy)' \
                      > new-taskdef.json

                    aws ecs register-task-definition \
                      --region $AWS_REGION \
                      --cli-input-json file://new-taskdef.json
                    '''
                }
            }
        }

        stage('Update ECS Service') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                                  credentialsId: 'aws-creds']]) {
                    sh '''
                    aws ecs update-service \
                      --cluster $CLUSTER_NAME \
                      --service $SERVICE_NAME \
                      --force-new-deployment \
                      --region $AWS_REGION
                    '''
                }
            }
        }
    }
}
