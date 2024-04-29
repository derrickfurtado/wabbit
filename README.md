MVP:

1. Create Account
2. Log in securly to Account with bcrypt
3. Record Job Opportunities and details associated with it.
4. Link Job object to Company objects
5. Link Job object to staff and recruiter objects
6. Create tasks for email, call, or general for each job
7. Have time dependency associated with all tasks
8. Trigger notifications based on time frame: (following is a general timeline)
    - Create job as favorite, but have not applied yet ==> 24 hours - automate email to user (E2U) to demand call-2-action (CTA) apply for this job
    - Job applied
        - immediately ==> find recruiter and create recruiter object
        - immediately ==> find 2 staffers that could be on team and create staff object
        - immediately ==> E2U -- CTA connect on LinkedIn to staffers and send intro
        - 24 hours ==> CTA send email/InMail to recruiter (if found)
        - 1 week ==> E2U -- "Have you heard back?"
        - 1 week ==> CTA -- DM one of 2 staffers for referral
    - Recruiter Interview
        - E2U 2 days before scheduled interview to demand research and preparation
        - 30 mins after interview -- E2U to CTA -- send thank you and excited email to recruiter
    - Multiple interviews
        - similar to recruiter steps



Rubric:

1. Front End
    - 3 CSS-styled pages.
2. Server
    - 3 endpoints
    - 3 view functions
3. DB
    - Active DB
    - Full CRUD functionality
4. Login
    - need login process functioning
5. Features
    - 3 user features complete and function