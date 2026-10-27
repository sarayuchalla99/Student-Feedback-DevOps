pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'YOUR_DOCKERHUB_USERNAME/student-feedback'
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        KUBECONFIG_CREDENTIALS_ID = 'kubeconfig-file'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Validate files') {
            steps {
                sh 'test -f app.py && test -f requirements.txt && test -f Dockerfile'
            }
        }
        stage('Build image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$BUILD_NUMBER -t $DOCKER_IMAGE:latest .'
            }
        }
        stage('Push image') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh 'echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin'
                    sh 'docker push "$DOCKER_IMAGE:$BUILD_NUMBER"'
                    sh 'docker push "$DOCKER_IMAGE:latest"'
                    sh 'docker logout'
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS_ID}", variable: 'KUBECONFIG_FILE')]) {
                    sh 'sed "s|YOUR_DOCKERHUB_USERNAME/student-feedback:latest|$DOCKER_IMAGE:$BUILD_NUMBER|g" deployment.yaml > deployment-ci.yaml'
                    sh 'KUBECONFIG="$KUBECONFIG_FILE" kubectl apply -f deployment-ci.yaml'
                    sh 'KUBECONFIG="$KUBECONFIG_FILE" kubectl apply -f service.yaml'
                    sh 'KUBECONFIG="$KUBECONFIG_FILE" kubectl rollout status deployment/student-feedback --timeout=120s'
                }
            }
        }
    }
    post {
        success { echo 'Student Feedback System deployed successfully.' }
        failure { echo 'Pipeline failed. Check the console log for the error.' }
    }
}
