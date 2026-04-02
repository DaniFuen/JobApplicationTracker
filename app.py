from flask import Flask, render_template, request, redirect
from database import get_db
import json

app = Flask(__name__)

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS n FROM companies")
    companies_count = cursor.fetchone()['n']

    cursor.execute("SELECT COUNT(*) AS n FROM jobs")
    jobs_count = cursor.fetchone()['n']

    cursor.execute("SELECT COUNT(*) AS n FROM applications")
    apps_count = cursor.fetchone()['n']

    cursor.execute("SELECT COUNT(*) AS n FROM contacts")
    contacts_count = cursor.fetchone()['n']

    cursor.execute("SELECT status, COUNT(*) AS cnt FROM applications GROUP BY status")
    status_counts = {r['status']: r['cnt'] for r in cursor.fetchall()}

    cursor.execute("""
        SELECT a.application_date, a.status, j.job_title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC
        LIMIT 5
    """)
    recent = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html",
                           companies_count=companies_count,
                           jobs_count=jobs_count,
                           apps_count=apps_count,
                           contacts_count=contacts_count,
                           status_counts=status_counts,
                           recent=recent)


@app.route('/companies')
def companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    data = cursor.fetchall()
    conn.close()
    return render_template("companies.html", data=data)


@app.route('/add_company', methods=['POST'])
def add_company():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO companies (company_name, industry, website, city, state, notes) VALUES (%s,%s,%s,%s,%s,%s)",
        (request.form['company_name'], request.form.get('industry'), request.form.get('website'),
         request.form.get('city'), request.form.get('state'), request.form.get('notes'))
    )
    conn.commit()
    conn.close()
    return redirect('/companies')


@app.route('/edit_company/<int:id>', methods=['GET', 'POST'])
def edit_company(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        cursor.execute(
            "UPDATE companies SET company_name=%s, industry=%s, website=%s, city=%s, state=%s, notes=%s WHERE company_id=%s",
            (request.form['company_name'], request.form.get('industry'), request.form.get('website'),
             request.form.get('city'), request.form.get('state'), request.form.get('notes'), id)
        )
        conn.commit()
        conn.close()
        return redirect('/companies')
    cursor.execute("SELECT * FROM companies WHERE company_id=%s", (id,))
    company = cursor.fetchone()
    conn.close()
    return render_template("edit_company.html", company=company)


@app.route('/delete_company/<int:id>')
def delete_company(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM companies WHERE company_id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/companies')

@app.route('/jobs')
def jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT j.*, c.company_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY j.date_posted DESC
    """)
    data = cursor.fetchall()
    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies_list = cursor.fetchall()
    conn.close()
    return render_template("jobs.html", data=data, companies=companies_list)


@app.route('/add_job', methods=['POST'])
def add_job():
    reqs = request.form.get('requirements', '')
    req_json = json.dumps([r.strip() for r in reqs.split(',') if r.strip()])
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
        (request.form['company_id'], request.form['job_title'], request.form.get('job_type', 'Full-time'),
         request.form.get('salary_min') or None, request.form.get('salary_max') or None,
         request.form.get('job_url'), request.form.get('date_posted') or None, req_json)
    )
    conn.commit()
    conn.close()
    return redirect('/jobs')


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        reqs = request.form.get('requirements', '')
        req_json = json.dumps([r.strip() for r in reqs.split(',') if r.strip()])
        cursor.execute(
            "UPDATE jobs SET company_id=%s, job_title=%s, job_type=%s, salary_min=%s, salary_max=%s, job_url=%s, date_posted=%s, requirements=%s WHERE job_id=%s",
            (request.form['company_id'], request.form['job_title'], request.form.get('job_type', 'Full-time'),
             request.form.get('salary_min') or None, request.form.get('salary_max') or None,
             request.form.get('job_url'), request.form.get('date_posted') or None, req_json, id)
        )
        conn.commit()
        conn.close()
        return redirect('/jobs')
    cursor.execute("SELECT * FROM jobs WHERE job_id=%s", (id,))
    job = cursor.fetchone()
    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    companies_list = cursor.fetchall()
    conn.close()
    if job and job.get('requirements'):
        reqs = job['requirements']
        if isinstance(reqs, str):
            reqs = json.loads(reqs)
        job['requirements_str'] = ', '.join(reqs)
    return render_template("edit_job.html", job=job, companies=companies_list)


@app.route('/delete_job/<int:id>')
def delete_job(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE job_id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/jobs')

@app.route('/applications')
def applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, j.job_title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC
    """)
    data = cursor.fetchall()
    cursor.execute("""
        SELECT j.job_id, j.job_title, c.company_name FROM jobs j
        JOIN companies c ON j.company_id = c.company_id ORDER BY c.company_name
    """)
    jobs_list = cursor.fetchall()
    conn.close()
    return render_template("applications.html", data=data, jobs=jobs_list)


@app.route('/add_application', methods=['POST'])
def add_application():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, notes) VALUES (%s,%s,%s,%s,%s,%s)",
        (request.form['job_id'], request.form['application_date'], request.form.get('status', 'Applied'),
         request.form.get('resume_version'), 1 if request.form.get('cover_letter_sent') else 0,
         request.form.get('notes'))
    )
    conn.commit()
    conn.close()
    return redirect('/applications')


@app.route('/edit_application/<int:id>', methods=['GET', 'POST'])
def edit_application(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        cursor.execute(
            "UPDATE applications SET job_id=%s, application_date=%s, status=%s, resume_version=%s, cover_letter_sent=%s, notes=%s WHERE application_id=%s",
            (request.form['job_id'], request.form['application_date'], request.form.get('status', 'Applied'),
             request.form.get('resume_version'), 1 if request.form.get('cover_letter_sent') else 0,
             request.form.get('notes'), id)
        )
        conn.commit()
        conn.close()
        return redirect('/applications')
    cursor.execute("SELECT * FROM applications WHERE application_id=%s", (id,))
    application = cursor.fetchone()
    cursor.execute("""
        SELECT j.job_id, j.job_title, c.company_name FROM jobs j
        JOIN companies c ON j.company_id = c.company_id ORDER BY c.company_name
    """)
    jobs_list = cursor.fetchall()
    conn.close()
    return render_template("edit_application.html", application=application, jobs=jobs_list)


@app.route('/delete_application/<int:id>')
def delete_application(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE application_id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/applications')


@app.route('/contacts')
def contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ct.*, c.company_name
        FROM contacts ct
        JOIN companies c ON ct.company_id = c.company_id
        ORDER BY ct.contact_name
    """)
    data = cursor.fetchall()
    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies_list = cursor.fetchall()
    conn.close()
    return render_template("contacts.html", data=data, companies=companies_list)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes) VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (request.form['company_id'], request.form['contact_name'], request.form.get('title'),
         request.form.get('email') or None, request.form.get('phone'),
         request.form.get('linkedin_url'), request.form.get('notes'))
    )
    conn.commit()
    conn.close()
    return redirect('/contacts')


@app.route('/edit_contact/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        cursor.execute(
            "UPDATE contacts SET company_id=%s, contact_name=%s, title=%s, email=%s, phone=%s, linkedin_url=%s, notes=%s WHERE contact_id=%s",
            (request.form['company_id'], request.form['contact_name'], request.form.get('title'),
             request.form.get('email') or None, request.form.get('phone'),
             request.form.get('linkedin_url'), request.form.get('notes'), id)
        )
        conn.commit()
        conn.close()
        return redirect('/contacts')
    cursor.execute("SELECT * FROM contacts WHERE contact_id=%s", (id,))
    contact = cursor.fetchone()
    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    companies_list = cursor.fetchall()
    conn.close()
    return render_template("edit_contact.html", contact=contact, companies=companies_list)


@app.route('/delete_contact/<int:id>')
def delete_contact(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE contact_id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/contacts')


@app.route('/match', methods=['GET', 'POST'])
def match():
    results = []
    user_skills = ""
    if request.method == 'POST':
        user_skills = request.form.get('skills', '')
        skill_list = [s.strip().lower() for s in user_skills.split(',') if s.strip()]
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT j.job_id, j.job_title, j.salary_min, j.salary_max,
                   j.requirements, c.company_name
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
        """)
        jobs_all = cursor.fetchall()
        conn.close()
        for job in jobs_all:
            reqs_raw = job.get('requirements')
            if reqs_raw:
                if isinstance(reqs_raw, str):
                    reqs = json.loads(reqs_raw)
                else:
                    reqs = reqs_raw
                reqs_lower = [r.lower() for r in reqs]
                matched = [s for s in skill_list if s in reqs_lower]
                missing = [r for r in reqs if r.lower() not in skill_list]
                total = len(reqs_lower)
                pct = round(len(matched) / total * 100) if total else 0
                results.append({
                    'job_title':    job['job_title'],
                    'company_name': job['company_name'],
                    'salary_min':   job['salary_min'],
                    'salary_max':   job['salary_max'],
                    'matched':      matched,
                    'missing':      missing,
                    'total':        total,
                    'pct':          pct,
                })
        results.sort(key=lambda x: x['pct'], reverse=True)
    return render_template("match.html", results=results, user_skills=user_skills)


if __name__ == "__main__":
    app.run(debug=True)