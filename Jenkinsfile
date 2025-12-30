// Jenkinsfile - Declarative Pipeline for E2E Tests
// Runs Playwright tests in Docker and archives artifacts

pipeline {
    agent any

    environment {
        // Docker image name
        DOCKER_IMAGE = 'parking-e2e-tests'
        DOCKER_TAG = "${BUILD_NUMBER}"
        
        // Test configuration - loaded from Jenkins credentials
        BASE_URL = credentials('PARKING_BASE_URL')
        TEST_USERNAME = credentials('PARKING_TEST_USERNAME')
        TEST_PASSWORD = credentials('PARKING_TEST_PASSWORD')
        PLATE_NO = credentials('PARKING_PLATE_NO')
    }

    options {
        // Keep builds for 30 days
        buildDiscarder(logRotator(daysToKeepStr: '30', numToKeepStr: '50'))
        // Timeout after 30 minutes
        timeout(time: 30, unit: 'MINUTES')
        // Add timestamps to console output
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Run E2E Tests') {
            steps {
                echo 'Running E2E tests...'
                script {
                    // Run tests in Docker container
                    // Mount artifacts directory to persist test results
                    sh """
                        docker run --rm \
                            -e BASE_URL="${BASE_URL}" \
                            -e TEST_USERNAME="${TEST_USERNAME}" \
                            -e TEST_PASSWORD="${TEST_PASSWORD}" \
                            -e PLATE_NO="${PLATE_NO}" \
                            -e HEADLESS=true \
                            -v \${PWD}/artifacts:/app/artifacts \
                            ${DOCKER_IMAGE}:${DOCKER_TAG} \
                            pytest \
                            --junitxml=/app/artifacts/junit.xml \
                            --html=/app/artifacts/report.html \
                            --self-contained-html \
                            -v \
                            || true
                    """
                    // Note: '|| true' ensures we don't fail immediately on test failures
                    // This allows us to archive artifacts before marking build as failed
                }
            }
        }

        stage('Collect Results') {
            steps {
                echo 'Collecting test results...'
                script {
                    // Check if tests passed by examining the junit.xml
                    def testResults = junit(
                        testResults: 'artifacts/junit.xml',
                        allowEmptyResults: true
                    )
                    
                    // Archive all artifacts
                    archiveArtifacts(
                        artifacts: 'artifacts/**',
                        allowEmptyArchive: true,
                        fingerprint: true
                    )
                    
                    // Publish HTML report
                    publishHTML(target: [
                        allowMissing: true,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'artifacts',
                        reportFiles: 'report.html',
                        reportName: 'Playwright Test Report'
                    ])
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            // Clean up Docker image to save space
            sh """
                docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true
            """
            
            // Always archive artifacts even on failure
            archiveArtifacts(
                artifacts: 'artifacts/**',
                allowEmptyArchive: true
            )
        }
        
        success {
            echo 'Tests passed successfully!'
        }
        
        failure {
            echo 'Tests failed. Check artifacts for details.'
            // Optional: Send notification
            // emailext(
            //     subject: "E2E Tests Failed - Build #${BUILD_NUMBER}",
            //     body: "Check ${BUILD_URL} for details",
            //     recipientProviders: [developers()]
            // )
        }
        
        unstable {
            echo 'Tests are unstable. Some tests may have failed.'
        }
    }
}
