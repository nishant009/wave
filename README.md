# Wave Software Development Challenge

## Assumptions:
1. There are two job groups A and B. Job group A is paid $20/hr, and job group B is paid $30/hr.
1. Each employee is identified by a string called an "employee id" that is
globally unique in the system.
1. Hours are tracked per employee, per day in comma-separated value files (CSV).
1. Each individual CSV file is known as a "time report", and contains:
    1. A header, denoting the columns in the sheet (`date`, `hours worked`, `employee id`, `job group`)
    1. 0 or more data rows
    1. A footer row where the first cell contains the string `report id`, and the second cell contains a unique identifier for this report.
1. It is guaranteed that:
    1. Columns will always be in that order.
    1. There will always be data in each column.
    1. There will always be a well-formed header line.
    1. There will always be a well-formed footer line.
1. Number of hours worked will always be less than 255

## Available functionality:
1. The app accepts (via a form) a comma separated file with the schema
   described in the previous section.
1. The app parses the given file, and stores the timekeeping information  in a mysql database for archival reasons.
1. After upload, the application displays a _payroll report_. This
report is also accessible without having to upload a file first. This is assuming there is some data in the database.
1. If an attempt is made to upload two files with the same report id, the
second upload will fail with an error message indicating that this is not allowed.

## Payroll report structure:
1. There are 3 columns in the report: `Employee Id`, `Pay Period`,
   `Amount Paid`
1. A `Pay Period` is a date interval that is roughly biweekly. Each month has two pay periods; the _first half_ is from the 1st to the 15th inclusive, and the _second half_ is from the 16th to the end of the month inclusive.
1. Each employee has a single row in the report for each pay period that records hours worked in that period. 
1. The `Amount Paid` reports the sum of the hours worked in that pay period multiplied by the hourly rate for their job group.
1. If an employee was not paid in a specific pay period, no row exists for that employee + pay period combination in the report.
1. The report is sorted in descending order of pay periods. Additionally records with same pay period are sorted in ascending order of employee id.
1. The report is based on all _of the data_ across _all of the uploaded time reports_, for all time.

## Setup:
1. Make sure you have installed the latest version of docker on your machine.
1. Navigate to the project directory
1. To build the images, run the command: `docker-compose build`
1. To start the project, run the command: `docker-compose up -d`
1. Wait for the containers to start, you can check the status by running the command: `docker-compose ps`
1. Once all containers are reported as running, open your browser and navigate to `http://localhost:5000` to interact with the app
1. You can shutdown the app from the UI. Alternatively you can run the command `docker-compose down -v --rmi all --remove-orphans` to clean up everything.

## Description:
In this particular implementation of the challenge, I concentrated on the backend portion of the application since that is where my core strength lies. For the frontend portion I'm relying on server side rendering of HTML templates using FLASK's template rendering capabilities.

I have created two tables to respectively store the payroll information and the ids of the reports that I have already processed.

## Future Improvements:
- Testing infrastructure - unit tests and integration tests
- A proper user signup and authentication functionality - login
- Better validation of user input including checking data passed to backend for malicious code
- Better datetime math for calculating intervals
- Automated infrastructure creation for production with autoscaling
- Separation of concerns between frontend and backend
- Better secrets management
- Scalable persistance mechanisms
- Checking and guarding against common security threats/vulnerabilities
- Better handling of PII
- Alerting and monitoring
