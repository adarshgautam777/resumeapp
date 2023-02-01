# resumeapp

# Tables in Resume APP

User
    - id
    - username

PersonalDetails
    - id
    - name
    - phone
    - email
    - address
    - Linkdin_url
    - ForeignKey('user.id')

Projects
    - id
    - name
    - desc
    - start_date
    - end_date
    - ForeignKey('user.id')
    
Experiences
       - id
       - company_name
       - role
       - role desc
       - start_date
       - end_date
       - ForeignKey('user.id')

Education
    - id
    - school_name
    - degree_name
    - start_date
    - end_date
    - FOreignKey('user.id')

Certificates 
     - id
     - title
     - start_date
     - end_date
     - ForeignKey('user.id')

Skills
    - id
    - title
    - confidence_score
    - ForeignKey('user.id')

