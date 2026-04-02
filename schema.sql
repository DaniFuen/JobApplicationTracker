DROP DATABASE IF EXISTS job_tracker;
CREATE DATABASE job_tracker;
USE job_tracker;


CREATE TABLE companies (
    company_id   INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    industry     VARCHAR(50),
    website      VARCHAR(200),
    city         VARCHAR(50),
    state        VARCHAR(50),
    notes        TEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE jobs (
    job_id          INT AUTO_INCREMENT PRIMARY KEY,
    company_id      INT NOT NULL,
    job_title       VARCHAR(100) NOT NULL,
    job_type        ENUM('Full-time','Part-time','Contract','Internship') DEFAULT 'Full-time',
    salary_min      INT,
    salary_max      INT,
    job_url         VARCHAR(300),
    date_posted     DATE,
    requirements    JSON,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);


CREATE TABLE applications (
    application_id    INT AUTO_INCREMENT PRIMARY KEY,
    job_id            INT NOT NULL,
    application_date  DATE NOT NULL,
    status            ENUM('Applied','Screening','Interview','Offer','Rejected','Withdrawn') DEFAULT 'Applied',
    resume_version    VARCHAR(50),
    cover_letter_sent BOOLEAN DEFAULT FALSE,
    interview_data    JSON,
    notes             TEXT,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);


CREATE TABLE contacts (
    contact_id   INT AUTO_INCREMENT PRIMARY KEY,
    company_id   INT NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    title        VARCHAR(100),
    email        VARCHAR(100),
    phone        VARCHAR(20),
    linkedin_url VARCHAR(200),
    notes        TEXT,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);


SHOW TABLES;


INSERT INTO companies (company_name, industry, website, city, state) VALUES
('Tech Solutions Inc',  'Technology',      'www.techsolutions.com',     'Miami',         'Florida'),
('Data Analytics Corp', 'Data Science',    'www.dataanalytics.com',     'Austin',        'Texas'),
('Cloud Systems LLC',   'Cloud Computing', 'www.cloudsystems.com',      'Seattle',       'Washington'),
('Digital Innovations', 'Software',        'www.digitalinnovations.com','San Francisco', 'California'),
('Smart Tech Group',    'AI/ML',           'www.smarttech.com',         'Boston',        'Massachusetts');


SELECT * FROM companies;


INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, date_posted, requirements) VALUES
(1, 'Software Developer',     'Full-time', 70000,  90000,  '2025-01-15', '["Python", "SQL", "Flask"]'),
(1, 'Database Administrator', 'Full-time', 75000,  95000,  '2025-01-10', '["MySQL", "SQL", "Linux"]'),
(2, 'Data Analyst',           'Full-time', 65000,  85000,  '2025-01-12', '["SQL", "Python", "Tableau"]'),
(3, 'Cloud Engineer',         'Full-time', 80000,  100000, '2025-01-08', '["AWS", "Docker", "Kubernetes"]'),
(4, 'Junior Developer',       'Full-time', 55000,  70000,  '2025-01-14', '["Python", "JavaScript", "HTML"]'),
(4, 'Senior Developer',       'Full-time', 95000,  120000, '2025-01-14', '["Python", "React", "SQL", "AWS"]'),
(5, 'ML Engineer',            'Full-time', 90000,  115000, '2025-01-11', '["Python", "TensorFlow", "SQL"]');


SELECT * FROM jobs;


INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent) VALUES
(1, '2025-01-16', 'Applied',    'v2.1', TRUE),
(3, '2025-01-13', 'Interview',  'v2.1', TRUE),
(4, '2025-01-09', 'Rejected',   'v2.0', FALSE),
(5, '2025-01-15', 'Applied',    'v2.1', TRUE),
(7, '2025-01-12', 'Screening',  'v2.1', TRUE);


SELECT * FROM applications;


INSERT INTO contacts (company_id, contact_name, title, email, phone) VALUES
(1, 'Sarah Johnson',  'HR Manager',          'sjohnson@techsolutions.com', '305-555-0101'),
(2, 'Michael Chen',   'Technical Recruiter', 'mchen@dataanalytics.com',    '512-555-0102'),
(3, 'Emily Williams', 'Hiring Manager',      'ewilliams@cloudsystems.com', '206-555-0103'),
(4, 'David Brown',    'Senior Developer',     NULL,                         '415-555-0104'),
(5, 'Lisa Garcia',    'Talent Acquisition',  'lgarcia@smarttech.com',      '617-555-0105');


SELECT * FROM contacts;

SELECT * FROM jobs WHERE salary_min >= 70000;


SELECT * FROM contacts WHERE email IS NULL;


UPDATE applications
SET status = 'Interview'
WHERE application_id = 3;


SELECT jobs.job_title, jobs.salary_min, jobs.salary_max, companies.company_name
FROM jobs
INNER JOIN companies ON jobs.company_id = companies.company_id;


SELECT companies.company_name, jobs.job_title
FROM companies
LEFT JOIN jobs ON companies.company_id = jobs.company_id;


SELECT c.company_name, j.job_title, a.application_date, a.status
FROM applications a
INNER JOIN jobs j ON a.job_id = j.job_id
INNER JOIN companies c ON j.company_id = c.company_id;


SELECT company_name FROM companies
WHERE company_id IN (SELECT DISTINCT company_id FROM jobs);


SELECT job_title, salary_min FROM jobs
WHERE salary_min > (SELECT AVG(salary_min) FROM jobs);
