from flask import Flask, request, jsonify
from flask_cors import CORS
from config import db, SECRET_KEY
from os import path, getcwd, environ
from dotenv import load_dotenv
from models.user import User
from models.projects import Projects
from models.experiences import Experiences
from models.educations import Educations
from models.skills import Skills
from models.certificates import Certificates
from models.personalDetails import PersonalDetails

load_dotenv(path.join(getcwd(), '.env'))


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.secret_key = SECRET_KEY

    db.init_app(app)
    print("DB initialized successfully")

    with app.app_context():
        @app.route("/signup", methods=['POST'])
        def signup():
            data = request.form.to_dict(flat=True)
            print(data)
            new_user = User(
                username=data['username']
            )

            db.session.add(new_user)
            db.session.commit()
            return jsonify(msg="User added successfully")

        @app.route("/add_personal_details", methods=['POST'])
        def add_personal_details():
            recv_username = request.args.get('username')
            user = User.query.filter_by(username=recv_username).first()

            data = request.get_json()

            new_personal_details = PersonalDetails(
                name=data['name'],
                phone=data['phone'],
                email=data['email'],
                address=data['address'],
                Linkdin_url=data['linkedin_url'],
                user_id=user.id
            )

            db.session.add(new_personal_details)
            db.session.commit()

            return jsonify(msg="Personal details added successfully")

        @app.route("/add_projects", methods=['POST'])
        def add_projects():
            recv_username = request.args.get('username')
            user = User.query.filter_by(username=recv_username).first()

            project_data = request.get_json()
            for data in project_data["data"]:
                user_proj = Projects(
                    name=data["name"],
                    desc=data["desc"],
                    start_date=data["start_date"],
                    end_date=data["end_date"],
                    user_id=user.id
                )
            db.session.add(user_proj)
            db.session.commit()

            return jsonify(msg="Projects added successfully")

        @app.route("/add_experiences", methods=['POST'])
        def add_experiences():
            recv_username = request.args.get('username')
            user = User.query.filter_by(username=recv_username).first()
            exp_data = request.get_json()
            for data in exp_data["data"]:
                user_exp = Experiences(
                    company_name=data["company_name"],
                    role=data["role"],
                    role_desc=data["role_desc"],
                    start_date=data["start_date"],
                    end_date=data["end_date"],
                    user_id=user.id
                )
            db.session.add(user_exp)
            db.session.commit()

            return jsonify(msg="Experiences added successfully")

        @app.route("/add_educations", methods=['POST'])
        def add_educations():
            recv_username = request.args.get('username')
            user = User.query.filter_by(username=recv_username).first()
            edu_data = request.get_json()
            for data in edu_data["data"]:
                user_edu = Educations(
                    school_name=data["school_name"],
                    degree_name=data["degree_name"],
                    start_date=data["start_date"],
                    end_date=data["end_date"],
                    user_id=user.id
                )
            db.session.add(user_edu)
            db.session.commit()

            return jsonify(msg="Education details added successfully")
        
        
        @app.route("/add_certificates", methods=['POST'])
        def add_certificates():
            recv_username = request.args.get('username')
            user = User.query.filter_by(username=recv_username).first()
            cert_data = request.get_json()
            for data in cert_data["data"]:
                user_cert = Certificates(
                    title=data["title"],
                    start_date=data["start_date"],
                    end_date=data["end_date"],
                    user_id=user.id
                )
            db.session.add(user_cert)
            db.session.commit()

            return jsonify(msg="Certificates added successfully")
        

        @app.route("/add_skills", methods=['POST'])
        def add_skills():
            recv_username = request.args.get('username')
            user = User.query.filter_by(username=recv_username).first()
            skills_data = request.get_json()
            for data in skills_data["data"]:
                user_skills = Skills(
                    title=data["title"],
                    confidence_score=data["confidence_score"],
                    user_id=user.id
                )
            db.session.add(user_skills)
            db.session.commit()

            return jsonify(msg="Skills added successfully")

            

        @app.route("/get_resume_json", methods=["GET"])
        def get_resume_json():
            recv_username = request.args.get('username')
            user = User.query.filter_by(username=recv_username).first()

            personal_details = PersonalDetails.query.filter_by(user_id=user.id).first()
            experiences = Experiences.query.filter_by(user_id=user.id).all()
            projects = Projects.query.filter_by(user_id=user.id).all()
            educations = Educations.query.filter_by(user_id=user.id).all()
            certificates = Certificates.query.filter_by(user_id=user.id).all()
            skills = Skills.query.filter_by(user_id=user.id).all()

            resume_data = {
                "name": personal_details.name,
                "phone": personal_details.phone,
                "email": personal_details.email,
                "address": personal_details.address,
                "linkedin_url": personal_details.Linkdin_url
            }

            experiences_data = []
            projects_data = []
            education_data = []
            certificates_data = []
            skills_data = []

            # Experience
            for exp in experiences:
                experiences_data.append({
                    "company_name": exp.company_name,
                    "role": exp.role,
                    "role_desc": exp.role_desc,
                    "start_date": exp.start_date,
                    "end_date": exp.end_date
                })

            resume_data["experiences"] = experiences_data

            # Project
            for proj in projects:
                projects_data.append({
                    "name": proj.name,
                    "desc": proj.desc,
                    "start_date": exp.start_date,
                    "end_date": exp.end_date
                })

            resume_data["projects"] = projects_data

            # Education
            for edu in educations:
                education_data.append({
                    "school_name": edu.school_name,
                    "degree_name": edu.degree_name,
                    "start_date": edu.start_date,
                    "end_date": edu.end_date
                })

            resume_data["educations"] = education_data
            
            # Certificates
            for cer in certificates:
                certificates_data.append({
                    "title": cer.title,
                    "start_date": cer.start_date,
                    "end_date": cer.end_date
                })

            resume_data["certificates"] = certificates_data
            
            
            # Skills
            for skills in skills_data:
                skills_data.append({
                    "title": skills.title,
                    "confidence_score": skills.confidence_score
                })

            return resume_data
        # db.drop_all()
        db.create_all()
        db.session.commit()

        return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
