CREATE TABLE payroll (
	date DATE NOT NULL, employee_id MEDIUMINT UNSIGNED NOT NULL, 
	hours TINYINT UNSIGNED NOT NULL,
	job_group CHAR(1) NOT NULL,
	INDEX(date),
	INDEX(employee_id),
	INDEX(job_group)
);
CREATE TABLE reports (report_id TINYINT UNSIGNED NOT NULL PRIMARY KEY);