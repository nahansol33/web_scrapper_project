def save_to_file(file_name, jobs):
    file = open(f"{file_name}.csv", "w")
    file.write("title, company, location, URL\n")
    for job in jobs:
        file.write(f"{job['title']},{job['company']},{job['location']},{job['link']}\n")
    file.close()
    print("Finished Writing to File")
