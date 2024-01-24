# GEI-Dashboard

This was a group project, for Makers Academy Data Engineering Bootcamp.

### Goal

Creating data pipelines to analyze the PISA 2018 dataset and develop a functioning dashboard that an organisation called GEI can use to easily visualise and interpret the data.

### Data Pipeline

For this project, there was 20 relational databases that hold real-time data for 20 different countries and we had a three level challenge to extract the data, do transformation to get specific results and load into 5 different charts on a dashboard.

We were tasked with a three level challenge, first to develop the charts displaying correct summary data that is no more than an hour old, then data should be no more than a minute old, and last the data should be up to the second which we managed to show the charts being updated up to the second.

This is the diagram of designing our pipeline, although for the execution we decided to set up Airflow and the Dags on localhost.

<img width="1363" alt="Screenshot 2024-01-11 at 17 35 18" src="https://github.com/shirinooo/GEI-Dashboard/assets/141428650/7ca7c61f-f5da-4023-b3d4-783ff6b09f30">

### REST API

For the final part to provide transformed data in the specified JSON format, we made a Flask app to create the endpoints for each chart and deployed it to EC2.

<img width="766" alt="Screenshot 2024-01-24 at 11 18 44" src="https://github.com/shirinooo/GEI-Dashboard/assets/141428650/516b645a-7604-4b1d-8ccc-aad6a0bf5d14">

This is the dashboard with two charts updated with the data.

<img width="1437" alt="Screenshot 2024-01-10 at 18 24 53" src="https://github.com/shirinooo/GEI-Dashboard/assets/141428650/e71daffe-c4fe-4218-a685-f0b912e448aa">



And this is a recording of the Dashboard with all the charts being updated every few seconds.

https://github.com/shirinooo/GEI-Dashboard/assets/141428650/9f0addd8-404b-44fa-a929-3a27519e92c9

