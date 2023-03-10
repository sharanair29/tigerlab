pipeline {
    agent any 
    stages {
        stage('Build') { 
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Test') { 
            steps {
                sh 'python3 manage.py test'
            }
        }

        stage('Deploy to Staging') { 
            steps {
                sh 'ssh -o StrictHostKeyChecking=no deployment-user@stagingip "source venv/bin/activate; \
                cd tigerlab; \
                git pull origin master; \
                pip install -r requirements.txt --no-warn-script-location; \
                python manage.py migrate; \
                deactivate; \
                sudo sysmtemctl restart nginx; \
                sudo systemctl restart gunicorn "'
            }
        }

        stage('Deploy to Production') { 
            input {
                message "Shall we deploy to production?"
                ok "Yes please!"
            }
            steps {
                sh 'ssh -o StrictHostKeyChecking=no deployment-user@productionip "source venv/bin/activate; \
                cd polling; \
                git pull origin master; \
                pip install -r requirements.txt --no-warn-script-location; \
                python manage.py migrate; \
                deactivate; \
                sudo sysmtemctl restart nginx; \
                sudo systemctl restart gunicorn "'
            }
        }
    }
}