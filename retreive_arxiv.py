import arxiv

# Define a search query
search = arxiv.Search(
    query="machine learning",  # Your search query
    max_results=5,             # Number of results to fetch
    sort_by=arxiv.SortCriterion.SubmittedDate
)

# Fetch and display results
for result in search.results():
    print(f"Title: {result.title}")
    print(f"Authors: {', '.join(author.name for author in result.authors)}")
    print(f"Published: {result.published}")
    print(f"Summary: {result.summary}")
    print(f"PDF: {result.pdf_url}")
    print("-" * 80)