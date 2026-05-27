import pandas as pd

# ── 1. LOAD ──────────────────────────────────────────────
df = pd.read_csv("postings.csv")
print(f"Total rows loaded: {len(df)}")

# ── 2. CLEAN ─────────────────────────────────────────────

# Keep only useful columns
cols = [
    'title', 'company_name', 'location', 'formatted_work_type',
    'formatted_experience_level', 'remote_allowed',
    'min_salary', 'max_salary', 'med_salary', 'normalized_salary',
    'currency', 'skills_desc', 'description'
]
df = df[cols]

# Drop rows where the job title is missing (essential column)
df = df.dropna(subset=['title'])

# Fill missing salary with 0 (we'll filter these out in charts)
df['normalized_salary'] = df['normalized_salary'].fillna(0)

# Clean up remote_allowed — treat missing as "Not specified"
df['remote_allowed'] = df['remote_allowed'].fillna(0).astype(int)
df['remote_allowed'] = df['remote_allowed'].map({1: 'Remote', 0: 'On-site'})

# Standardize text columns
df['title'] = df['title'].str.strip().str.title()
df['company_name'] = df['company_name'].str.strip().str.title()

print(f"Rows after cleaning: {len(df)}")

# ── 3. ANALYZE ────────────────────────────────────────────

# Top 15 most common job titles
print("\n📌 Top 15 Job Titles:")
print(df['title'].value_counts().head(15))

# Top 10 hiring companies
print("\n🏢 Top 10 Hiring Companies:")
print(df['company_name'].value_counts().head(10))

# Work type breakdown (full-time, part-time, contract etc.)
print("\n⏰ Work Type Breakdown:")
print(df['formatted_work_type'].value_counts())

# Experience level breakdown
print("\n🎓 Experience Level Breakdown:")
print(df['formatted_experience_level'].value_counts())

# Remote vs On-site
print("\n🌍 Remote vs On-site:")
print(df['remote_allowed'].value_counts())

# Salary insights (only where salary data exists)
salary_df = df[df['normalized_salary'] > 0]
print(f"\n💰 Salary Insights (from {len(salary_df)} postings with salary data):")
print(f"  Average salary: ${salary_df['normalized_salary'].mean():,.0f}")
print(f"  Median salary:  ${salary_df['normalized_salary'].median():,.0f}")
print(f"  Min salary:     ${salary_df['normalized_salary'].min():,.0f}")
print(f"  Max salary:     ${salary_df['normalized_salary'].max():,.0f}")

# ── 4. SAVE CLEANED DATA ─────────────────────────────────
df.to_csv("cleaned_jobs.csv", index=False)
print("\n✅ Cleaned data saved to cleaned_jobs.csv")