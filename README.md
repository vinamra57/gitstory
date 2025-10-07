# GitStory

GitStory is a command-line tool that helps developers quickly understand the history and structure of a software project by turning Git data into a readable “story.” Instead of manually digging through hundreds of commits or complex branches, users can run a single command to generate concise, human-readable summaries of a repository’s evolution.

GitStory is especially useful for:
- New developers onboarding onto large or unfamiliar codebases  
- Engineering managers or professors reviewing team progress  
- Open-source contributors exploring new projects  

Our long-term vision is to make project history as easy to understand as reading a short narrative — one that highlights when, how, and why major changes occurred.

---

## Project Goals

- Summarize major commits and branch changes from a repository’s Git history  
- Help developers identify when and why key features or refactors occurred  
- Reduce onboarding time for new team members and contributors  
- Provide readable, AI-generated summaries that capture a project’s evolution  
- Maintain data privacy by running locally and only sharing minimal metadata with external APIs  

---

## Planned Features

- Repository Parsing Engine – Extracts commit messages, authors, and timestamps from local Git repositories using GitPython  
- Commit Grouping – Automatically clusters related commits into “chapters” (feature additions, bug fixes, refactors)  
- AI Summarization Module – Sends grouped commit data to an external or local AI model for text summarization  
- Command-Line Interface – Simple, human-readable commands for summarizing repositories, branches, or time ranges  
- Error Handling & Logging – Graceful handling of invalid repos, API errors, or empty histories  

Stretch Goals
- Interactive web-based visualization dashboard  
- Enhanced contextual summaries across branches and contributors  
- **Time-bound summarization mode 
- Repository comparison and analytics  

---

## Team

| Name | Role |
|------|------|
| Vinamra Agarwal | AI Developer |
| Adwita Garg | Backend Developer |
| Vishal Sathambakkam | AI Developer |
| Ian Limasi | Backend Developer |
| ShengYao Liu | Product Manager |
| Derick Chiem | Backend Developer |

---

## Living Document

You can view our detailed proposal, use cases, requirements, and process plan here: [GitStory Living Document (Google Doc)](https://docs.google.com/document/d/1lqRVpxWHBmymRPX7l9FnYYCD0okzg7u-qnDOIQPh01U/edit?usp=sharing)

---

## Repository Layout

This repository will include:
```

/src/          →  Core CLI implementation (Git parser, summarizer, etc.)
/docs/         →  Milestone write-ups and final report PDFs
/tests/        →  Unit and integration tests
README.md      →  Project overview and setup instructions

```

---

## 📄 License

This project is developed as part of the **University of Washington CSE 403 (Software Engineering)** course.  
All rights reserved to the GitStory project team. Educational and non-commercial use only.
