
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'sarayuchalla/student-feedback'
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        KUBECONFIG_CREDENTIALS_ID = 'kubeconfig-file'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate files') {
            steps {
                bat 'if not exist app.py exit /b 1'
                bat 'if not exist requirements.txt exit /b 1'
                bat 'if not exist Dockerfile exit /b 1'
                echo 'All required files are present.'
            }
        }

        stage('Build image') {
            steps {
                bat 'docker build -t %DOCKER_IMAGE%:%BUILD_NUMBER% -t %DOCKER_IMAGE%:latest .'
            }
        }

        stage('Push image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS_ID}",
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat 'powershell -NoProfile -Command "$env:DOCKERHUB_TOKEN | docker login -u $env:DOCKERHUB_USER --password-stdin"'
                    bat 'docker push %DOCKER_IMAGE%:%BUILD_NUMBER%'
                    bat 'docker push %DOCKER_IMAGE%:latest'
                    bat 'docker logout'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([
                    file(
                        credentialsId: "${KUBECONFIG_CREDENTIALS_ID}",
                        variable: 'KUBECONFIG_FILE'
                    )
                ]) {
                    bat '''
                        set "KUBECONFIG=%KUBECONFIG_FILE%"
                        powershell -NoProfile -ExecutionPolicy Bypass -Command "(Get-Content deployment.yaml -Raw) -replace 'sarayuchalla/student-feedback:latest', 'sarayuchalla/student-feedback:%BUILD_NUMBER%' | Set-Content deployment-ci.yaml"
                        if errorlevel 1 exit /b 1

                        kubectl apply -f deployment-ci.yaml
                        if errorlevel 1 exit /b 1

                        kubectl apply -f service.yaml
                        if errorlevel 1 exit /b 1

                        kubectl rollout status deployment/student-feedback --timeout=120s
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Student Feedback System deployed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the Console Output.'
        }
    }
}
