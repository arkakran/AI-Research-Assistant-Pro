from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import threading
import time
import traceback
import re
from markupsafe import Markup

load_dotenv()

from utils.config import Config
from utils.agents import ModernResearchAgents
from utils.search import TavilyRetrievalSystem
from utils.report_generator import EnhancedReportGenerator

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Global variable to store research progress
research_progress = {}

def process_report_content(content):
    """Process report content to properly format HTML with clean structure"""
    if not content:
        return ""
    
    # First, let's clean up the content and convert everything to a consistent format
    html = content
    
    # Remove any existing HTML tags and convert to plain text first
    html = re.sub(r'<[^>]+>', '', html)  # Strip all HTML tags
    
    # Now process line by line for better structure
    lines = html.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Process headings
        if line.startswith('### '):
            processed_lines.append(f'<h3 class="mt-4 mb-3 text-dark">{line[4:]}</h3>')
        elif line.startswith('## '):
            processed_lines.append(f'<h2 class="mt-4 mb-3 text-primary border-bottom pb-2">{line[3:]}</h2>')
        elif line.startswith('# '):
            processed_lines.append(f'<h1 class="mt-5 mb-4 text-primary border-bottom pb-2">{line[2:]}</h1>')
        
        # Process bullet points
        elif line.startswith('- ') or line.startswith('* '):
            bullet_text = line[2:].strip()
            # Process bold and italic within bullet points
            bullet_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', bullet_text)
            bullet_text = re.sub(r'(?<!\*)\*(.*?)\*(?!\*)', r'<em>\1</em>', bullet_text)
            processed_lines.append(f'<li class="mb-2">{bullet_text}</li>')
        
        # Process regular paragraphs
        else:
            # Process bold and italic
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'(?<!\*)\*(.*?)\*(?!\*)', r'<em>\1</em>', line)
            
            # Process URLs
            line = re.sub(r'(https?://[^\s<>"{}|\\^`[\]]+)', 
                         r'<a href="\1" target="_blank" rel="noopener noreferrer" class="text-decoration-underline">\1</a>', 
                         line)
            
            processed_lines.append(f'<p class="mb-3 lh-lg">{line}</p>')
    
    # Join all lines
    html = '\n'.join(processed_lines)
    
    # Wrap consecutive <li> elements in <ul>
    html = re.sub(r'(<li[^>]*>.*?</li>(?:\s*<li[^>]*>.*?</li>)*)', 
                  r'<ul class="mb-4 ps-4">\1</ul>', html, flags=re.DOTALL)
    
    return Markup(html)

# Make the function available in templates
app.jinja_env.globals.update(process_report_content=process_report_content)

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/start_research', methods=['POST'])
def start_research():
    """Start the research process"""
    print("=== POST request received to /start_research ===")  # Debug log
    try:
        # Check if request has JSON data
        if not request.is_json:
            print("ERROR: Request is not JSON")
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        print(f"Request data: {data}")  # Debug log
        
        if not data:
            print("ERROR: No JSON data received")
            return jsonify({'error': 'No data received'}), 400
        
        query = data.get('query', '').strip()
        print(f"Query extracted: '{query}'")  # Debug log
        
        if not query:
            print("ERROR: Empty query")
            return jsonify({'error': 'Please enter a research query'}), 400
        
        # Check API keys
        groq_key = os.getenv("GROQ_API_KEY")
        tavily_key = os.getenv("TAVILY_API_KEY")
        
        print(f"API Keys check - Groq: {'✓' if groq_key else '✗'}, Tavily: {'✓' if tavily_key else '✗'}")
        
        if not groq_key or not tavily_key:
            print("ERROR: API keys missing")
            return jsonify({'error': 'API keys not found. Please check your .env file'}), 500
        
        # Generate unique research ID
        research_id = f"research_{int(time.time())}"
        print(f"Generated research ID: {research_id}")  # Debug log
        
        # Initialize progress tracking
        research_progress[research_id] = {
            'status': 'initializing',
            'progress': 0,
            'message': 'Initializing AI Research Agents...',
            'query': query,
            'result': None,
            'error': None
        }
        
        # Start research in background thread
        thread = threading.Thread(target=run_research, args=(research_id, query))
        thread.daemon = True
        thread.start()
        print(f"Background thread started for {research_id}")  # Debug log
        
        response_data = {'research_id': research_id, 'status': 'started'}
        print(f"Sending response: {response_data}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"ERROR in start_research: {str(e)}")  # Debug log
        print(f"Traceback: {traceback.format_exc()}")  # Full traceback
        return jsonify({'error': str(e)}), 500

def run_research(research_id, query):
    """Run research in background thread"""
    print(f"=== Starting research thread for {research_id} ===")
    try:
        # Initialize agents
        print("Phase 1: Initializing agents...")
        research_progress[research_id].update({
            'status': 'initializing',
            'progress': 10,
            'message': 'Setting up AI agents...'
        })
        
        agents = ModernResearchAgents()
        retrieval = TavilyRetrievalSystem(agents.tavily_api_key)
        
        research_agent = agents.setup_research_agent()
        summarizer_agent = agents.setup_summarizer_agent()
        critic_agent = agents.setup_critic_agent()
        writer_agent = agents.setup_writer_agent()
        
        print("Agents initialized successfully")
        
        # Phase 1: Search
        print("Phase 2: Starting search...")
        research_progress[research_id].update({
            'status': 'searching',
            'progress': 25,
            'message': 'Conducting advanced web search...'
        })
        
        search_results = retrieval.advanced_search(query)
        print(f"Search completed, results length: {len(search_results)}")
        
        research_data = research_agent.invoke({
            "query": query, 
            "search_results": search_results
        })
        print("Research agent completed")
        
        # Phase 2: Summarize
        print("Phase 3: Summarizing...")
        research_progress[research_id].update({
            'status': 'summarizing',
            'progress': 50,
            'message': 'Processing and summarizing information...'
        })
        
        summary = summarizer_agent.invoke({"research_content": research_data})
        print("Summarizer agent completed")
        
        # Phase 3: Critique
        print("Phase 4: Critiquing...")
        research_progress[research_id].update({
            'status': 'critiquing',
            'progress': 75,
            'message': 'Fact-checking and verification...'
        })
        
        critique = critic_agent.invoke({"summary_content": summary})
        print("Critic agent completed")
        
        # Phase 4: Write Report
        print("Phase 5: Writing report...")
        research_progress[research_id].update({
            'status': 'writing',
            'progress': 90,
            'message': 'Generating final report...'
        })
        
        final_report = writer_agent.invoke({
            "research_data": research_data,
            "summary": summary,
            "critique": critique
        })
        print("Writer agent completed")
        
        # Complete
        research_progress[research_id].update({
            'status': 'completed',
            'progress': 100,
            'message': 'Research completed successfully!',
            'result': final_report
        })
        
        print(f"=== Research {research_id} completed successfully ===")
        
    except Exception as e:
        error_msg = f'Research failed: {str(e)}'
        print(f"ERROR in run_research: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        
        research_progress[research_id].update({
            'status': 'error',
            'progress': 0,
            'message': error_msg,
            'error': str(e)
        })

@app.route('/research_progress/<research_id>')
def get_research_progress(research_id):
    """Get research progress"""
    print(f"Progress check for: {research_id}")  # Debug log
    
    if research_id not in research_progress:
        print(f"Research ID {research_id} not found")
        return jsonify({'error': 'Research ID not found'}), 404
    
    progress_data = research_progress[research_id]
    print(f"Progress data: {progress_data}")  # Debug log
    
    return jsonify(progress_data)

@app.route('/research_result/<research_id>')
def research_result(research_id):
    """Display research results"""
    print(f"Displaying results for: {research_id}")  # Debug log
    
    if research_id not in research_progress:
        print(f"Research ID {research_id} not found")
        return render_template('index.html', error='Research not found')
    
    progress_data = research_progress[research_id]
    
    if progress_data['status'] != 'completed':
        print(f"Research {research_id} not completed yet, status: {progress_data['status']}")
        return render_template('index.html', error='Research not completed yet')
    
    print(f"Rendering research results for {research_id}")
    return render_template('research.html', 
                         query=progress_data['query'],
                         report=progress_data['result'],
                         research_id=research_id)

@app.route('/download/<format>/<research_id>')
def download_report(format, research_id):
    """Download report in specified format"""
    print(f"Download request: {format} for {research_id}")  # Debug log
    
    if research_id not in research_progress:
        print(f"Research ID {research_id} not found for download")
        return "Research not found", 404
    
    progress_data = research_progress[research_id]
    
    if progress_data['status'] != 'completed':
        print(f"Research {research_id} not completed for download")
        return "Research not completed", 400
    
    query = progress_data['query']
    report_content = progress_data['result']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    try:
        if format == 'markdown':
            content = EnhancedReportGenerator.generate_markdown(report_content, query)
            filename = f"research_report_{timestamp}.md"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Generated markdown file: {filename}")
            return send_file(filename, as_attachment=True, download_name=filename)
            
        elif format == 'pdf':
            pdf_buffer = EnhancedReportGenerator.generate_pdf(report_content, query)
            filename = f"research_report_{timestamp}.pdf"
            
            with open(filename, 'wb') as f:
                f.write(pdf_buffer.getvalue())
            
            print(f"Generated PDF file: {filename}")
            return send_file(filename, as_attachment=True, download_name=filename)
        
        elif format == 'json':
            report_data = {
                "query": query,
                "report": report_content,
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "ai_model": "llama-3.3-70b-versatile",
                    "search_engine": "tavily_advanced"
                }
            }
            filename = f"research_data_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2)
            
            print(f"Generated JSON file: {filename}")
            return send_file(filename, as_attachment=True, download_name=filename)
        
        else:
            print(f"Invalid format requested: {format}")
            return "Invalid format", 400
            
    except Exception as e:
        print(f"ERROR generating {format} file: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return f"Error generating {format} file: {str(e)}", 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    groq_configured = bool(os.getenv("GROQ_API_KEY"))
    tavily_configured = bool(os.getenv("TAVILY_API_KEY"))
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'api_keys_configured': groq_configured and tavily_configured,
        'groq_configured': groq_configured,
        'tavily_configured': tavily_configured,
        'debug_mode': app.debug
    })

@app.route('/test', methods=['POST'])
def test_post():
    """Test POST endpoint"""
    print("=== Test POST endpoint hit ===")
    try:
        data = request.get_json()
        print(f"Test data received: {data}")
        return jsonify({
            'message': 'POST request working!',
            'data_received': data,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Test POST error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    print(f"Internal server error: {str(error)}")
    return render_template('index.html', error='Internal server error'), 500

# Before request logging
@app.before_request
def log_request_info():
    print(f"=== {request.method} {request.path} ===")
    if request.method == 'POST':
        print(f"Content-Type: {request.content_type}")
        print(f"Is JSON: {request.is_json}")

if __name__ == '__main__':
    print("=== Starting Flask App ===")
    print(f"GROQ_API_KEY configured: {'✓' if os.getenv('GROQ_API_KEY') else '✗'}")
    print(f"TAVILY_API_KEY configured: {'✓' if os.getenv('TAVILY_API_KEY') else '✗'}")
    print(f"SECRET_KEY configured: {'✓' if os.getenv('SECRET_KEY') else '✗'}")
    print("==========================")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
