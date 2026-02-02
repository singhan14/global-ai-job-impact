# 🚀 GitHub Deployment Guide

This guide will help you deploy your AI Impact Job Analyzer to GitHub and Streamlit Cloud.

## 📋 Prerequisites

- Git installed on your computer
- A GitHub account
- A Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

## 🔧 Step 1: Initialize Git Repository

Open terminal in your project directory and run:

```bash
cd "/Users/singhanyadav/Desktop/Datathon Sample"
git init
git add .
git commit -m "Initial commit: AI Impact Job Analyzer"
```

## 📤 Step 2: Create GitHub Repository

### Option A: Using GitHub Website

1. Go to [github.com](https://github.com) and sign in
2. Click the "+" icon in top right → "New repository"
3. Repository name: `ai-job-impact-analyzer` (or your preferred name)
4. Description: "AI-powered job analyzer predicting automation risk and AI impact"
5. Choose "Public" (required for free Streamlit deployment)
6. **Do NOT** initialize with README (we already have one)
7. Click "Create repository"

### Option B: Using GitHub CLI (if installed)

```bash
gh repo create ai-job-impact-analyzer --public --source=. --remote=origin
```

## 🔗 Step 3: Connect Local Repository to GitHub

Copy the commands from GitHub (after creating the repo) or run:

```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/ai-job-impact-analyzer.git
git branch -M main
git push -u origin main
```

## ☁️ Step 4: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Fill in the details:
   - **Repository**: Select your `ai-job-impact-analyzer` repo
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click "Advanced settings" (optional):
   - **Python version**: 3.11
6. Click "Deploy!"

The deployment will take 2-5 minutes. Streamlit will:
- Install dependencies from `requirements.txt`
- Load the model files (`.pkl`)
- Start the application

## 🎉 Step 5: Share Your App

Once deployed, you'll get a URL like:
```
https://ai-job-impact-analyzer.streamlit.app
```

Update your README.md with this URL:
```bash
# Edit README.md and add your URL to the "Live Demo" section
git add README.md
git commit -m "Add Streamlit Cloud URL"
git push
```

## 📊 Important Files for Deployment

Make sure these files are included in your repository:

### ✅ Required Files
- `app.py` - Main application (338 KB)
- `requirements.txt` - Dependencies
- `model_adoption.pkl` - AI adoption model (1.6 MB)
- `model_automation.pkl` - Automation risk model (1.7 MB)
- `model_displacement.pkl` - Displacement risk model (2.0 MB)
- `feature_columns.pkl` - Feature names (128 B)

### 📝 Documentation
- `README.md` - Project documentation
- `.gitignore` - Ignored files

### 🔄 Optional (for retraining)
- `train_models.py` - Model training script
- `ai_impact_jobs_2010_2025(2).csv` - Training data (415 KB)
- `Modelling.ipynb` - Original notebook

## 🔍 Troubleshooting

### Issue: "Module not found" error

**Solution**: Make sure `requirements.txt` has all dependencies with correct versions.

### Issue: App crashes on startup

**Solution**: Check that all `.pkl` files are committed to the repo:
```bash
git lfs track "*.pkl"  # If files are too large
git add .gitattributes
git add *.pkl
git commit -m "Add model files"
git push
```

### Issue: Models too large for GitHub

**Solution**: Use Git LFS (Large File Storage):
```bash
# Install Git LFS
brew install git-lfs  # macOS
# or visit: https://git-lfs.github.com/

# Initialize Git LFS
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git add *.pkl
git commit -m "Track model files with Git LFS"
git push
```

## 🔄 Updating Your App

After making changes:

```bash
git add .
git commit -m "Describe your changes"
git push
```

Streamlit Cloud will automatically redeploy your app!

## 🌟 Make Your Repo Stand Out

### Add badges to README.md:

```markdown
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CatBoost](https://img.shields.io/badge/CatBoost-FFD700?style=for-the-badge&logo=catboost&logoColor=black)
```

### Add topics to your repository:
- streamlit
- machine-learning
- catboost
- ai
- job-automation
- data-science
- python

## 📱 Next Steps

1. ✅ Share app URL on LinkedIn/Twitter
2. ✅ Add screenshot to README
3. ✅ Star your own repo (to test notifications)
4. ✅ Create a demo video
5. ✅ Add to your portfolio

---

## 📞 Need Help?

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **GitHub Docs**: [docs.github.com](https://docs.github.com)
- **Git LFS**: [git-lfs.github.com](https://git-lfs.github.com)

**Good luck with your deployment! 🚀**
