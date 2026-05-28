# TODO - Phase 2 Steps (When API Key is Available)

## Prerequisites
- Python 3.9+ installed
- API key from teaching assistant

## Steps

### 1. Install dependencies
```bash
cd /Users/luca/dev/software-design
pip install -r requirements.txt
```

### 2. Set API key
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Run the program
```bash
cd /Users/luca/dev/software-design
python src/main.py
```

### 4. Check outputs
- `output/conversation_log.md` - Deliverable 2 (conversation log)
- `output/report.md` - Deliverable 3 (report draft)
- `output/views/` - All Mermaid diagram files

### 5. Fill in names
Edit `output/report.md`:
- Replace `[YOUR_NAME_1]` with actual name
- Replace `[YOUR_NAME_2]` with actual name
- Replace `[YOUR_NAME_3]` with actual name

### 6. Final cleanup
After everything is verified, delete this file:
```bash
rm TODO.md
```

## Troubleshooting

### API key error
If you see "GEMINI_API_KEY environment variable is not set":
```bash
export GEMINI_API_KEY="your-key"
```

### Model not found
If the model name `gemini-3.1-pro-preview` is not available, update `src/config.py`:
```python
MODEL_NAME = "actual-model-name"
```

### Token limit exceeded
If responses are cut off, reduce `max_output_tokens` in `src/config.py` or split prompts.
