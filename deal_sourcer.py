# -*- coding: utf-8 -*-
import subprocess
import json
import ollama
import sys

# Reconfigure stdout for UTF-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

def fetch_deals(model_name="minicpm5:1b"):
    try:
        cmd = ["gh", "search", "repos", "created:>2026-05-01 stars:>500", "--json", "name,owner,description,stargazersCount"]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=True)
        repos = json.loads(res.stdout)[:5]
    except Exception as e:
        print(f"GitHub search failed: {e}. Loading cached or mock demo deals.")
        try:
            with open("output.json", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            with open("ideal_output.json", encoding="utf-8") as f:
                return json.load(f)

    results = []
    for r in repos:
        owner = r["owner"]["login"]
        repo_name = r["name"]
        stars = r["stargazersCount"]
        desc = r.get("description") or ""
        
        bio_text = f"Owner: {owner}"
        try:
            res_user = subprocess.run(["gh", "api", f"users/{owner}"], capture_output=True, text=True, encoding="utf-8", check=True)
            user_data = json.loads(res_user.stdout)
            bio_text = f"Name: {user_data.get('name')}, Bio: {user_data.get('bio')}, Company: {user_data.get('company')}"
        except Exception:
            pass

        prompt = f"Repo: {repo_name}\nStars: {stars}\nDesc: {desc}\nFounder: {bio_text}\n"
        try:
            resp = ollama.chat(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are a project scout. Evaluate if this looks like a solo, unfunded founder (High Potential) or enterprise project (Low Potential). Respond ONLY with a JSON object containing keys: 'founder', 'score' (int 0-100), 'verdict', 'reason'. Do not output any thoughts or extra text."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": 0.2},
                format="json"
            )
            eval_data = json.loads(resp["message"]["content"])
        except Exception as e:
            eval_data = {"founder": owner, "score": 50, "verdict": "Error", "reason": f"Evaluation failed: {e}"}

        eval_data.update({"repo": repo_name, "owner": owner, "description": desc, "stars": stars, "bio": bio_text})
        results.append(eval_data)

    # Save successful results to output.json for caching
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    return results

if __name__ == "__main__":
    deals = fetch_deals()
    print(json.dumps(deals, indent=2, ensure_ascii=False))
