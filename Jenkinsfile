pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t devops_project .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker rm -f devops_container || exit 0'
                bat 'docker run -d -p 5000:5000 --name devops_container devops_project'
            }
        }
    }

    post {
        success {
            echo 'Build and deployment successful!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}