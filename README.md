# RangRajasthan Market

Rajasthan-focused social commerce marketplace for local artists. It mixes an Instagram-style artist feed with Amazon-style product shopping, cart, checkout, highlighted top projects, and an AI seller studio for captions, listing copy, SEO tags, photo ideas, and engagement suggestions.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501`.

## Optional Live AI

The AI seller studio works without an API token using a local fallback generator. For live HuggingFace model output, copy `.env.example` to `.env` and set:

```bash
HUGGINGFACEHUB_API_TOKEN=hf_your_token_here
```

## Files

- `app.py` - Streamlit marketplace, feed, cart, checkout, and AI seller studio
- `ai_workflow.py` - prompt construction, HuggingFace call, local fallback generation
- `validation.py` - input validation and sanitization
- `assets/artisan-market-banner.png` - generated project banner
