
## Overview

In this project, We will build a Github repository from scratch and create a scaffolding in performing both Continuous Integration and Continuous Delivery.

- Using Github Actions along with a Makefile, requirements.txt and application code to perform an initial lint, test, and install cycle.
- Integrating this project with Azure Pipelines to enable Continuous Delivery to Azure App Service.
- Using Azure Cloud shell in this project.

## Project Plan

- [Trello Board](https://trello.com/b/umdJDZJw/udacity-project-2)
- [Original Project Plan](documents/OriginalProjectPlan.xlsx)
- [Final Project Plan](documents/FinalProjectPlan.xlsx)

## Architecture Diagram

![Architectural Diagram](screenshots/architecture.png)

## Instructions

### Configuring Github

- Log in Azure Portal and access Azure Cloud Shell

- Create a ssh key by using this command:

    ```bash
    ssh-keygen -t rsa -b 2048 -C "phuongnv1996@outlook.com"
    ```

    ![SSH Key Create](screenshots/az-ssh.png)

- Copy the public key to Github Account -> Settings -> SSH and GPG keys (<https://github.com/settings/keys>)

    ![Setting SSH Key in Github](screenshots/github-setting-ssh.png)

### Project Locally

- After setting SSH key in Github, we can clone source code to Azure Cloud Shell by using command below:

    ```bash
    git clone git@github.com:phuongnv196/udacity-project-2.git
    ```

    ![Clone git source code](screenshots/github-clone-success.png)

- Create a Python Virtual Environment to run your application

    ```bash
    python3 -m venv ~/.udacity-project-2
    source ~/.udacity-project-2/bin/activate
  ```

    ![Install dependencies](screenshots/az-create-inv.png)

- Install all dependencies by using **make**

    ```bash
    make all
    ```

    ![Install dependencies](screenshots/az-install-dependencies.png)

- Run application using **flask**

    ```bash
    export FLASK_APP=app.py
    flask run
    ```

  ![Local run](screenshots/az-flask-run.png)

- After run application we had to open new tab and lauch a new Azure Cloud Shell session to test the application by running the *make_prediction.sh* script

    ```bash
    chmod +x make_prediction.sh
    ```

    ```bash
    ./make_prediction.sh
    ```

    We can see the result of script:

    ```bash
    Port: 5000
    {"prediction":[20.353731771344123]}
    ```

    ![Make prediction result](screenshots/az-make-prediction-result.png)  

### Azure App Service

Azure App Service is a cloud platform service (PaaS) offered by Azure that allows you to easily and quickly deploy web applications, mobile back-ends and RESTful APIs without worrying about the infrastructure. Some of the benefits of using Azure App Service are:

- It supports multiple programming languages (Java, Python, C#) and frameworks (.NET, Spring boot, Flask), giving you the flexibility to choose the best tools for your project.
- It provides high availability and scalability, ensuring that your applications can handle high traffic and demand without downtime or performance issues.
- It supports both Windows and Linux operating systems, enabling you to run your applications on the platform of your choice.
- It integrates very well with Azure pipelines for continuous delivery, allowing you to automate the deployment process and deliver updates faster and more reliably.
For more information and tutorials on how to use Azure App Service, please visit this [link](https://docs.microsoft.com/en-us/azure/app-service/).

#### ML Azure App Service

Azure App Service provides various options to create a new application. In this section, you will learn how to use the Azure CLI to deploy your app. In another section, you will see how to use Azure Pipelines to automate the deployment process.
**Set up Azure CLI:**

- Create a new Resource Group for our app

   ```bash
    az group create --location westeurope --resource-group phuongnv_rg_02 --tags project=udacity_p_2 environment=dev
    ```

**Deploy Application:**

- Clone the project, we can clone source code to Azure Cloud Shell by using command below:

    ```bash
    git clone git@github.com:phuongnv196/udacity-project-2.git
    ```

- Create a Python Virtual Environment to run your application

    ```bash
    python3 -m venv ~/.udacity-project-2
    source ~/.udacity-project-2/bin/activate
  ```

    ![Install dependencies](screenshots/az-create-inv.png)

- Install all dependencies by using **make**

    ```bash
    make all
    ```

    ![Install dependencies](screenshots/az-install-dependencies.png)

- Deploy application into the our resource group

    ```bash
    az webapp up -n flask-app-phuongnv --resource-group phuongnv_rg_02 --sku FREE
    ```

- Application will be deployed to azure service
  **(https://${app-name}.azurewebsites.net)** default port is 443

  ![Azure Service Deployed available](screenshots/az-service-deploy-flask-app.png)
  
- We can find app service in Azure Portal
  ![App Service in Azure Portal](screenshots/az-flask-app-service.png)
  
- Application was deployed successfully using azure pipelines from Deployment Center
  ![Azure app service from the Deployment Center](screenshots/az-deployment-center.png)

**Test ML Application:**

- Modify the *'make_predict_azure_app.sh'* script by updating the host name to align with the prediction application that has been deployed.
![Azure Service Edit Host Name](screenshots/az-mak-predict-azure-edit-app-name.png)

- Run the script *'make_predict_azure_app.sh'* to test the app

    ```bash
    chmod +x make_predict_azure_app.sh

    ./make_predict_azure_app.sh
    ```

- We will get the result:

    ```
    Port: 443
    {"prediction":[20.353731771344123]}
    ```

    ![Azure Prediction Result](screenshots/az-make-azure-prediction-result.png)

- Run locust from project folder in Windows by using Windows Power Shell

    ```bash
    locust
    ```

  ![Run locust test](screenshots/az-lotust-start.png)

- We can access to <http://localhost:8089> to test application with *locust*

  ![Locust Test Result](screenshots/az-lolust-result.png)

**Logs of Azure Webapp:**

Azure App Service offers the capability to access and view application logs. You can access these logs using Azure CLI commands:
    ```
    az webapp log tail --name flask-app-phuongnv --resource-group phuongnv_rg_02
    ```

![Screenshot of Logs](screenshots/az-flask-app-service-log.png)

### Github Actions

GitHub Actions is a powerful feature provided by GitHub, enabling the creation of comprehensive CI/CD workflows. Within the context of this project, we harness GitHub Actions to execute our Continuous Integration (CI) processes. These processes encompass building, linting, and testing our code, all of which are performed seamlessly through GitHub Actions.

To set up GitHub Actions for your repository, follow these steps:

- Navigate to the "Actions" tab within your GitHub repository.

- Select "New Workflow," and opt for the "Python Application Workflow." GitHub has the ability to analyze your code and suggest relevant workflows tailored to your codebase.

    ![GitHub Actions Setup](screenshots/github-action-python.png)

- Proceed with the workflow setup process. GitHub Actions will configure a workflow that suits the requirements of your code.

- Customization of the actions to align with our specific needs is essential. The default action steps are designed to run Python commands. However, given that we employ the *Make* utility for building, testing, and linting our code, we will need to adjust the GitHub Actions configuration accordingly.

By following these steps, you can harness the full potential of GitHub Actions and tailor them to your project's requirements.

![GitHub Actions Python configue](screenshots/github-action-python-configue.png)

- Edit the file *.github/workflows/python-app.yml*

    ```yml
    name: Python application test with Github Actions

    on: [push]

    jobs:
    build:

        runs-on: ubuntu-latest

        steps:
        - uses: actions/checkout@v2
        - name: Set up Python 3.8
        uses: actions/setup-python@v1
        with:
            python-version: 3.8
        - name: Install dependencies
        run: |
            make install
        - name: Lint with pylint
        run: |
            make lint
        - name: Test with pytest
        run: |
            make test

    ```

- Manually trigger the GitHub Action. Upon a successful launch, the results will be displayed below.
![Github Actions Result](screenshots/github-action-python-success.png)

- Once the workflow is configured, our application will undergo continuous building with each push or pull request made to our main branch.

### Azure DevOps

Azure DevOps offers a comprehensive set of developer services, enabling teams to efficiently plan work, collaborate on code development, and build and deploy applications. This platform fosters a collaborative environment and establishes a cohesive set of processes that unite developers, project managers, and contributors in software development endeavors. With Azure DevOps, organizations can accelerate product development compared to traditional software development approaches.

Here are key components of Azure DevOps:

- **Azure Repos**: It provides Git repositories and Team Foundation Version Control (TFVC) for effective source control of your code.

- **Azure Pipelines**: This service facilitates continuous integration and delivery (CI/CD) by offering build and release capabilities for your applications.

- **Azure Boards**: Equipped with a suite of Agile tools, it supports work planning and tracking, code defect management, and issue tracking using both Kanban and Scrum methodologies.

- **Azure Test Plans**: It furnishes various testing tools, including manual and exploratory testing, as well as continuous testing, to ensure the quality of your applications.

- **Azure Artifacts**: This feature enables teams to share packages from various sources, including Maven, npm, NuGet, and more, whether they are public or private, and to seamlessly integrate package sharing into your development pipelines.

With these offerings, Azure DevOps streamlines the software development lifecycle and empowers teams to enhance collaboration and accelerate the delivery of high-quality applications.

#### Set Up Azure Pipelines for Continuous Delivery

In this project, we leverage Azure Pipelines for the continuous delivery of the Flask ML App. Follow the steps below to set up your environment:

### Setting up Azure DevOps

- If you don't already have an Azure DevOps account, go to [dev.azure.com](https://dev.azure.com) to sign up for a free account.

- Create an Azure DevOps project:
  - Create a new project and establish a connection to Azure. The screenshots below illustrate the process:

     ![Create Azure Project](screenshots/devops-create-project.png)

- After creating the project, navigate to **Project settings** from the left navigation. On the Project Settings page, select **Pipelines > Service connections**, and then click on **New service connection**:

     ![Azure Project Settings](screenshots/devops-create-service-connection.png)

- In the **New Service Connections** dialog, select **Azure Resource Manager** from the dropdown:

     ![New Azure Resource Manager](screenshots/devops-create-service-connection-2.png)

- In the **Service Connection** dialogue box:
  - Select the scope level as **Subscription**.
  - You might need to log in.
  - Choose the **Resource Group** of the **Azure Web App** deployed.
  - Input a valid **Service Connection Name**.
  - Check the box for **Grant Access Permissions to all pipelines**.
  - Click **Save**.

     ![New Azure Resource Manager 2](screenshots/devops-create-service-connection-3.png)

### Setting up Azure Pipeline

- First, we need to create an Agent Pool to run jobs for Pipelines, and here we are using Linux to configure the Agent Pool. In **Project Setting** > **Agent Pools** > **Add pool**
    ![Create Agent Pool](screenshots/devops-piplines-create-agent-pool.png)

- On the **Add agent pool** popup, select the **Pool type** as **Self-hosted**, give the pool a name, and check the "**Grant access permission to all pipelines**" checkbox. Then, click the "**Create**" button.
    ![Create Agent Pool](screenshots/devops-piplines-create-agent-pool-2.png)

- On the Agent pool management screen that you've just created, click the **New agent** button and follow the instructions to set up the agent.
    ![Create Agent Pool](screenshots/devops-piplines-create-agent-pool-3.png)
    ![Create Agent Pool](screenshots/devops-piplines-create-agent-pool-4.png)
    ![Create Agent Pool](screenshots/devops-config-agent-pool.png)

- From your project page's left navigation, navigate to **Pipelines** and select **New Pipelines**.

- In the New Pipeline Interface:
  - Select GitHub as the repository source.
    ![Select GitHub Repo](screenshots/devops-create-pipelines.png)

  - Select your project.
     ![Select GitHub Repo 2](screenshots/devops-create-pipelines-1.png)

- In the Configure section, choose **Python to Linux Azure Webapp**:
  - Select the deployed app.
    ![Configure Pipeline](screenshots/devops-create-pipelines-2.png)
    ![Configure Pipeline](screenshots/devops-create-pipelines-3.png)
    ![Configure Pipeline](screenshots/devops-create-pipelines-4.png)

  - Validate and Review the configuration.
    ![Select Web App Name](screenshots/devops-create-pipelines-5.png)

- In the Review section, change pool to Agent Pool you created before. Validate the Pipeline YAML and click the **Save and Run** button. You might be prompted to save the code into GitHub.

    ![Review Pipeline](screenshots/devops-piplines-edit-yaml.png)
    ![Review Pipeline 2](screenshots/devops-piplines-edit-yaml-2.png)

- Once the pipeline is configured, you can continuously deliver your ML Flask App by running the pipeline.

     ![Pipeline Build](screenshots/devops-pipelines-finish-build-job.png)
     ![Pipeline Deploy](screenshots/devops-pipelines-finish-deploy-job.png)
     ![Pipeline Stage](screenshots/devops-piplines-lists.png)

## Resource Cleanup

To prevent incurring Azure resource charges related to this project, it is advisable to remove the resource group housing the App Service and the App Service Plan.

## Recommendations

- Develop efficient microservices.
- Establish useful and actionable alert mechanisms.

## Demonstration

[CI/CD Demo](https://youtu.be/4rQqlsnzKic)
