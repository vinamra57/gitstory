# GitStory

GitStory is a command-line tool that helps developers quickly understand the history and structure of a software project by turning Git data into a readable “story.” Instead of manually digging through hundreds of commits or reading through complex branches, users can run a single command to generate concise, human-readable summaries of a repository’s evolution.

GitStory is especially useful for:
- New developers onboarding onto large or unfamiliar codebases  
- Engineering managers, nontechnical PMs, or professors reviewing team progress  
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

## Features of GitStory

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

## Buildings, Testing, and Running

To build + run GitStory as a **user** (i.e. a user who would like to use GitStory for individual purpose), click here to get started (or check /docs/user): [User Documentation](docs/user)\
\
To build + run GitStory as a **developer** (i.e. someone who would like to contribute to GitStory or run the GitStory code), click here to get started (or check /docs/dev): [Developer Documentation](docs/dev)

---

## Repository Layout

This repository will include:
```

/src/gitstory  →  Core CLI implementation (Git parser, summarizer, etc.)
/reports/      →  Milestone write-ups and final report PDFs
/docs/         
-  /docs/dev/  →  Developer documentation
-  /docs/user/ →  User documentation
/tests/        →  Unit and integration tests
README.md      →  Project overview and setup instructions

```

---

## Living Document

You can view our detailed proposal, use cases, requirements, and process plan here: [GitStory Living Document (Google Doc)](https://docs.google.com/document/d/1lqRVpxWHBmymRPX7l9FnYYCD0okzg7u-qnDOIQPh01U/edit?usp=sharing)

---

## Team

| Name | Role | Email |
|------|------|-------|
| Vinamra Agarwal | AI Developer | vinamra1@cs.washington.edu
| Adwita Garg | Backend Developer | adgarg12@cs.washington.edu
| Vishal Sathambakkam | AI Developer | vishksat@cs.washington.edu
| Ian Limasi | Backend Developer | imlimasi@cs.washington.edu
| ShengYao Liu | Product Manager, UI Designer | sliu1229@cs.washington.edu
| Derick Chiem | Backend Developer | dchiem@cs.washington.edu

If there is a developer concern or an error in GitStory, **please create an Issue in the "Issues" tab for this Git Repo**, and our team will do the best to address the problem as soon as possible. To get in touch with the GitStory team for any other purposes however, please reach out to any of us through the email IDs listed above.

---

## 📄 License

This project is developed as part of the **University of Washington CSE 403 (Software Engineering)** course.  
All rights reserved to the GitStory project team. Educational and non-commercial use only.
