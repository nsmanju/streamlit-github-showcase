import streamlit as st
import requests
import base64

st.set_page_config(page_title="GitHub Repo Showcase", layout="wide")

st.title("📘 GitHub Repository Showcase")

# Step 1: GitHub Username
username = st.text_input("GitHub Username", value="nsmanju")

if username:
    # Step 2: Fetch public repos
    repos_url = f"https://api.github.com/users/{username}/repos"
    repos_response = requests.get(repos_url)

    if repos_response.status_code == 200:
        repos = repos_response.json()
        repo_names = sorted([repo["name"] for repo in repos])

        # Step 3: Select a repo
        selected_repo = st.selectbox("Select a repository", repo_names)

        if selected_repo:
            # Step 4: Fetch selected repo metadata
            repo_url = f"https://api.github.com/repos/{username}/{selected_repo}"
            readme_url = f"https://api.github.com/repos/{username}/{selected_repo}/readme"

            repo_res = requests.get(repo_url)
            readme_res = requests.get(readme_url)

            if repo_res.status_code == 200:
                repo_data = repo_res.json()

                st.header(f"📂 {repo_data['full_name']}")
                st.markdown(f"[🔗 GitHub Link]({repo_data['html_url']})")
                st.markdown(f"**Description:** {repo_data.get('description', 'No description')}")
                st.markdown(f"⭐ Stars: {repo_data['stargazers_count']} | 🍴 Forks: {repo_data['forks_count']} | 🐛 Open Issues: {repo_data['open_issues_count']}")

                if readme_res.status_code == 200:
                    content = readme_res.json().get('content', '')
                    try:
                        decoded = base64.b64decode(content).decode("utf-8")
                        st.subheader("📖 README")
                        st.markdown(decoded)
                    except Exception:
                        st.warning("Could not decode README.")
                else:
                    st.warning("README not found.")
            else:
                st.error("Failed to fetch repository metadata.")
    else:
        st.error("Failed to load repositories. Check GitHub username or rate limit.")
