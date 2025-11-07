import os
import json
import re
from datetime import datetime
from uuid import uuid4
import mimetypes
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from services.interfaces import TextExtractor, TextGenerator
from services.impl import DefaultTextExtractor, GeminiTextGenerator

app = Flask(__name__)



# Basic configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///edubot.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-change-me')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16 MB

ALLOWED_EXTENSIONS = {'.pdf', '.txt'}

_text_extractor: TextExtractor = DefaultTextExtractor()
_text_generator: TextGenerator = GeminiTextGenerator()

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_public_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
        }


class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    original_name = db.Column(db.String(255), nullable=False)
    stored_name = db.Column(db.String(255), nullable=False)
    relative_path = db.Column(db.String(1024), nullable=False)
    mime_type = db.Column(db.String(100))
    size_bytes = db.Column(db.Integer)
    extracted_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref=db.backref('documents', lazy=True))

# Ensure database tables exist on startup
with app.app_context():
    db.create_all()


@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from EduBot!', 'status': 'success'})


@app.route('/api/auth/register', methods=['POST'])
def register():
    payload = request.get_json(silent=True) or {}
    email = (payload.get('email') or '').strip().lower()
    password = payload.get('password') or ''

    if not email or not password:
        return jsonify({'error': 'email and password are required'}), 400

    if len(password) < 8:
        return jsonify({'error': 'password must be at least 8 characters'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'email already registered'}), 409

    password_hash = generate_password_hash(password)
    user = User(email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'registration successful'}), 201



@app.route('/api/auth/login', methods=['POST'])
def login():
    payload = request.get_json(silent=True) or {}
    email = (payload.get('email') or '').strip().lower()
    password = payload.get('password') or ''

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'invalid credentials'}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={'email': user.email}
    )
    return jsonify({'access_token': access_token, 'token_type': 'Bearer'})



@app.route('/api/me', methods=['GET'])
@jwt_required()
def me():
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'error': 'invalid token identity'}), 401
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404
    return jsonify({'user': user.to_public_dict()})


def _allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename)
    return ext.lower() in ALLOWED_EXTENSIONS



@app.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_file():
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'error': 'invalid token identity'}), 401

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'user not found'}), 404

    if 'file' not in request.files:
        return jsonify({'error': 'no file part in the request'}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({'error': 'no selected file'}), 400

    if not _allowed_file(uploaded_file.filename):
        return jsonify({'error': 'only PDF and TXT files are allowed'}), 400

    original_name = secure_filename(uploaded_file.filename)
    _, ext = os.path.splitext(original_name)
    unique_name = f"{uuid4().hex}{ext.lower()}"

    user_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    save_path = os.path.join(user_dir, unique_name)
    uploaded_file.save(save_path)

    # Determine metadata
    guessed_mime, _ = mimetypes.guess_type(save_path)
    try:
        size_bytes = os.path.getsize(save_path)
    except OSError:
        size_bytes = None

    # Extract text content (SRP: delegated to extractor; DIP: via interface)
    try:
        extracted_text = _text_extractor(save_path)
    except Exception as exc:
        # Cleanup the saved file if extraction fails
        try:
            os.remove(save_path)
        except Exception:
            pass
        return jsonify({'error': 'failed to extract text from file', 'details': str(exc)}), 400

    # Persist document record
    document = Document(
        user_id=user_id,
        original_name=original_name,
        stored_name=unique_name,
        relative_path=f"{user_dir}/{unique_name}",
        mime_type=guessed_mime,
        size_bytes=size_bytes,
        extracted_text=extracted_text,
    )
    db.session.add(document)
    db.session.commit()

    preview = (extracted_text or '')[:200]
    return jsonify({
        'message': 'file uploaded and text extracted successfully',
        'file': {
            'id': document.id,
            'original_name': original_name,
            'stored_name': unique_name,
            'user_id': user_id,
            'relative_path': f"{user_dir}/{unique_name}",
            'mime_type': guessed_mime,
            'size_bytes': size_bytes,
        },
        'extracted_text_chars': len(extracted_text or ''),
        'extracted_text_preview': preview,
    }), 201


@app.route('/api/ai/generate', methods=['POST'])
@jwt_required()
def ai_generate():
    identity = get_jwt_identity()
    try:
        int(identity)
    except (TypeError, ValueError):
        return jsonify({'error': 'invalid token identity'}), 401

    payload = request.get_json(silent=True) or {}
    prompt = (payload.get('prompt') or '').strip()
    model = (payload.get('model') or '').strip() or None
    if not prompt:
        return jsonify({'error': 'prompt is required'}), 400


    try:
        text = _text_generator(prompt, model_name=model)
    except Exception as exc:
        return jsonify({'error': 'generation failed', 'details': str(exc)}), 400

    return jsonify({'output': text})


@app.route('/api/ai/summarize', methods=['POST'])
@jwt_required()
def ai_summarize():
    """Generate a summary of the provided text using Gemini AI."""
    identity = get_jwt_identity()
    try:
        int(identity)
    except (TypeError, ValueError):
        return jsonify({'error': 'invalid token identity'}), 401

    payload = request.get_json(silent=True) or {}
    text = (payload.get('text') or '').strip()
    if not text:
        return jsonify({'error': 'text is required'}), 400

    # Create a prompt for summarization
    summarize_prompt = f"""Please provide a concise summary of the following text. 
Format the summary as a bulleted list with key points. Each point should be on a new line starting with a bullet (•).

Text to summarize:
{text}

Summary:"""

    try:
        summary = _text_generator(summarize_prompt)
        return jsonify({'summary': summary})
    except Exception as exc:
        return jsonify({'error': 'summarization failed', 'details': str(exc)}), 400


@app.route('/api/ai/flashcards', methods=['POST'])
@jwt_required()
def ai_flashcards():
    """Generate flashcards (question-answer pairs) from the provided text using Gemini AI."""
    identity = get_jwt_identity()
    try:
        int(identity)
    except (TypeError, ValueError):
        return jsonify({'error': 'invalid token identity'}), 401

    payload = request.get_json(silent=True) or {}
    text = (payload.get('text') or '').strip()
    if not text:
        return jsonify({'error': 'text is required'}), 400

    # Create a prompt for flashcard generation
    flashcard_prompt = f"""Based on the following text, generate 5-6 educational flashcards in JSON format.
Each flashcard should have a "question" and "answer" field. The questions should test understanding of key concepts.
Return ONLY a valid JSON array, no other text.

Text:
{text}

Format:
[
  {{"question": "Question 1", "answer": "Answer 1"}},
  {{"question": "Question 2", "answer": "Answer 2"}}
]

JSON:"""

    try:
        response = _text_generator(flashcard_prompt)
        # Try to extract JSON from the response (Gemini might add extra text)
        
        # Try to find JSON array in the response
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            flashcards_data = json.loads(json_match.group(0))
        else:
            # Fallback: try parsing the whole response
            flashcards_data = json.loads(response.strip())
        
        # Validate structure
        if not isinstance(flashcards_data, list):
            raise ValueError("Response is not a list")
        
        # Ensure each item has question and answer
        flashcards = []
        for item in flashcards_data:
            if isinstance(item, dict) and 'question' in item and 'answer' in item:
                flashcards.append({
                    'question': str(item['question']),
                    'answer': str(item['answer'])
                })
        
        if not flashcards:
            raise ValueError("No valid flashcards generated")
        
        return jsonify({'cards': flashcards})
    except json.JSONDecodeError as exc:
        return jsonify({'error': 'failed to parse flashcard response', 'details': str(exc), 'raw_response': response[:200]}), 400
    except Exception as exc:
        return jsonify({'error': 'flashcard generation failed', 'details': str(exc)}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)


