pipeline {
    agent {
        dockerfile {
            args "-v /var/lib/jenkins/tools/ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation/allure:/var/lib/jenkins/tools/ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation/allure -e ENV=$stand --add-host=ispro-test.mos.ru:10.15.141.129"
        }
    }

    environment {
        HOME = "${WORKSPACE}"
        STAGE_URL = 'type_url'
    }

    stages {

        stage("Prepare Environment") {
            steps {
                sh("chmod 777 utils/report/reporter.py")
                sh("mkdir ./temp")
                script {
                        def stand = params.stand
                        def url
                        switch (stand) {
                            case 'stage': url = env.STAGE_URL; break;
                        }
                        sh("""curl -s -k ${url}/oog/buildinfo | jq .data | jq -r 'to_entries|map("\\(.key)=\\(.value|tostring)")|.[]' > ./temp/environment.properties""")
                }
                sh("echo -e 'stand=$stand\ntestpath=$testpath' >> ./temp/environment.properties")
            }
        }

        stage("Run Tests") {
            steps {
                catchError { // start serial tests
                        sh("python3 -m pytest -n 1 -v -l -m 'serial' --remote --alluredir=allure-results --clean-alluredir $testpath")
                }
                catchError { // start parallel tests
                        sh("python3 -m pytest -n $threads -v -l -m 'not serial' --env=$stand --remote --alluredir=allure-results $testpath")
                }
            }
        }

        stage("Generate Report") {
            steps {
                  sh("mv ./temp/environment.properties ./allure-results/")
                  allure([
                        results: [[path: "allure-results"]]
                    ])
            }
        }
/*
       stage("Send Notification") {
            steps {
                dir("utils/report") {
                            sh("./reporter.py                        \
                            --chat_dest ${chatDest}                      \
                            --allure-report ${WORKSPACE}/allure-report/  \
                            --build-url ${BUILD_URL}                     \
                            --job_name=${JOB_NAME}")
                }
            }
        }
*/
        stage("Send Notification to telegram") {
            steps {
                dir("utils/report") {
                    sh("chmod +x tgm_reporter.py")
                    withCredentials([
                        string(credentialsId: 'cd399d14-6200-4105-8d37-f0c33985b1a3', variable: 'botToken'),
                        ]) {
                            sh("./tgm_reporter.py                            \
                            --botid ${BotID}                             \
                            --token ${botToken}                          \
                            --chatid ${ChatID}                           \
                            --allure-report ${WORKSPACE}/allure-report/  \
                            --build-url ${BUILD_URL}                     \
                            --job_name=${JOB_NAME}                       \
                            --stand_name=${stand}")
                    }
                }
            }
        }
    }
}

