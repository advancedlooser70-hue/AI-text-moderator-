# Deploying Chat Toxicity Moderator on Vercel

This guide explains how to deploy the Chat Toxicity Moderator application on Vercel with the proper setup.

## 🚀 Quick Deployment

### Prerequisites
- A free [Vercel account](https://vercel.com/signup)
- [Vercel CLI](https://vercel.com/cli) installed (optional)

### Steps

1. **Prepare your repository**
   - Make sure you have this repository ready with all files
   - The `vercel.json` configuration is already included
   - The `api/moderate.py` file contains the serverless function

2. **Deploy via Vercel Dashboard**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will automatically detect the configuration
   - Click "Deploy"

3. **Deploy via CLI** (Alternative)
   ```bash
   # Install Vercel CLI
   npm i -g vercel
   
   # Navigate to project directory
   cd Chat-Toxicity-Moderator
   
   # Deploy
   vercel
   ```

## ⚙️ Environment Variables (Optional)

For enhanced functionality, add these environment variables in your Vercel project settings:

- `GROQ_API_KEY`: Your GROQ API key for improved rephrasing quality

To add environment variables:
1. Go to your project in the Vercel dashboard
2. Go to Settings → Environment Variables
3. Add the variables listed above

## 📁 Project Structure for Vercel

```
├── api/
│   └── moderate.py         # Vercel serverless function
├── public/
│   ├── index.html          # Main interface
│   ├── sender.html         # Sender view
│   ├── receiver.html       # Receiver view
│   ├── moderator.html      # Moderation dashboard
│   └── demo.html           # Demo instructions
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel configuration
└── README.md              # Project documentation
```

## 🌐 Accessing Your Deployed Application

After deployment, your application will be available at:
- **Main Interface**: `https://your-project-name.vercel.app/`
- **Sender View**: `https://your-project-name.vercel.app/sender.html`
- **Receiver View**: `https://your-project-name.vercel.app/receiver.html`
- **Moderation Dashboard**: `https://your-project-name.vercel.app/moderator.html`

## 🔧 API Endpoints

- `POST /api/moderate` - Moderate a message
- `GET /api/moderate` - Health check

Example API call:
```javascript
const response = await fetch('/api/moderate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: "Your message here" })
});
const result = await response.json();
```

## 🛠️ How It Works

The Vercel deployment uses:
- **Static hosting** for HTML files in the `public` directory
- **Serverless functions** for the moderation API
- **Keyword-based toxicity detection** for Vercel compatibility
- **Optional GROQ API** for enhanced rephrasing

## ⚠️ Important Notes

1. **Model Limitations**: The full ML model functionality (Detoxify and T5) is not deployed to Vercel due to size and timeout constraints. Instead, a simpler keyword-based approach is used with optional external API support.

2. **Performance**: For production use with full ML functionality, consider platforms like Render, Railway, or AWS that support larger Python applications.

3. **API Keys**: When you provide a GROQ API key, the application will use the more sophisticated rephrasing functionality.

## 📞 Support

If you encounter issues:
1. Check the Vercel deployment logs in your dashboard
2. Verify environment variables are properly set
3. Review the application in the browser console for any frontend errors

## 🔄 Updating Your Deployment

After making changes:
1. Push updates to your GitHub repository
2. Vercel will automatically redeploy
3. Or manually trigger a deployment from your dashboard

# Vercel Deployment Instructions

## Memory Optimization for AI Text Moderator

This project has been optimized for Vercel deployment by using a lightweight toxicity detection system that avoids heavy AI dependencies during build time.

### Key Changes Made:

1. **Reduced Dependencies**: Heavy AI libraries (PyTorch, Transformers, Detoxify) have been removed from requirements.txt for Vercel deployment
2. **Keyword-based Detection**: Uses simple keyword-based toxicity detection instead of ML models during Vercel deployment
3. **Optimized Configuration**: vercel.json includes memory and timeout optimizations

### How It Works:

- The [api/moderate.py](file:///c/Users/Anadi Sharma/2k26 hackathons/Manit/AI-text-moderator/api/moderate.py) file contains both a simple keyword-based toxicity detector and a more advanced API-based rephrasing system
- For Vercel deployment, it uses the lightweight keyword-based system to avoid memory issues
- The rephrasing still works using the Groq API when available

### Environment Variables Required:

- `GROQ_API_KEY` (optional) - For enhanced rephrasing capabilities

### Deployment:

1. Push your changes to your GitHub repository
2. Import the project in Vercel
3. The build should complete without memory errors

### Local Development:

For full functionality with ML models, use:
```bash
pip install -r requirements-full.txt  # Contains all dependencies
```

The application will work with reduced functionality on Vercel but with full functionality when run locally.
