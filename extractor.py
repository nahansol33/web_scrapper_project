from file import save_to_file
from indeed import indeed_search
from wwr import extract_jobs

def job_extractor(searchWord):
    wwr_job_results = extract_jobs(searchWord)
    indeed_job_results = indeed_search(searchWord)
    all_jobs = wwr_job_results + indeed_job_results
    return all_jobs
