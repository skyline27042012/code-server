/* import shared library */
@Library('jenkins-shared-library')_

pipeline {
    agent any
    environment {
        //be sure to replace "sampriyadarshi" with your own Docker Hub username
        DOCKER_IMAGE_NAME = "skyline27042012/code-server"
        CANARY_REPLICAS = 0
    }
    stages {
        stage('Build') {
            steps {
                echo 'Running build automation'
                //sh './gradlew build --no-daemon'
                //archiveArtifacts artifacts: 'dist/trainSchedule.zip'
            }
/*
	    post {
       	    	always {
           		jiraSendBuildInfo site: 'http://192.168.1.201:6080/browse/BD-1'
			//Testing
       	    	 }
	    }
*/

        }
        stage('Build Docker Image') {
            when {
                branch 'master'
            }
            steps {
                script {
                    app = docker.build(DOCKER_IMAGE_NAME)
                    //app.inside {
                    //    sh 'echo Hello, World!'
                    //}
                }
            }
        }
        stage('Push Docker Image') {

            when {
                branch 'master'
            }

            steps {
                script {
                    docker.withRegistry("https://registry.hub.docker.com", "docker_hub_token") {
                        app.push("${env.BUILD_NUMBER}")
                        app.push("latest")
                    }
                }
            }
        }
        
        stage('DeployToProduction') {
            when {
                branch 'master'
            }
            steps {
                milestone(1)
                kubernetesDeploy(
                    kubeconfigId: 'kubenetes_token',
                    configs: 'code-server.yml',
                    enableConfigSubstitution: true
                )
            }
        }
    }
    /*post {
	always {
            kubernetesDeploy (
                kubeconfigId: 'kubeconfig',
                configs: 'train-schedule-kube-canary.yml',
                enableConfigSubstitution: true
            )
        }
	*/    
        //cleanup {
	    
	    /* Use slackNotifier.groovy from shared library and provide current build result as parameter */   
        //    slackNotifier(currentBuild.currentResult)
            // cleanWs()
        //}
   // }
}
