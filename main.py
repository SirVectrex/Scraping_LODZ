import multiprocessing
import time
import requests as requests
requests.packages.urllib3.disable_warnings()
import os
# ignore all warnings and errors


# This project will check a number of links and if they are valid and show a pdf as content, it will download the pdf and save it to a folder.

link = "https://bc.wimbp.lodz.pl/Content/"
start_scraping = 30400
end_scraping = 30900
max_jobs = 80
searchable_article = "Freie Presse"

def job_scheduler(link, target_name):
    try:

        # create a list of links to check
        amount_of_successful_downloads = 0
        jobs = []
        to_dos = end_scraping - start_scraping
        jobs_created = 0
        # run processes

        # check if there are more than 80 jobs running, if so, wait for 20 to finish, else start a new job
        # this is to prevent the program from crashing due to too many processes running at the same time
        while jobs_created < to_dos:

                # print(len(jobs))
                if len(jobs) > max_jobs:
                    for job in jobs:
                        job.join()
                        jobs.remove(job)
                        print("\r RUNNING: Active jobs: " + str(len(jobs)) + "  -  JOBS LEFT: " + str(
                            to_dos - jobs_created), end="")
                        # print("Job finished - active jobs: " + str(len(jobs)))
                        time.sleep(1)

                p = multiprocessing.Process(target=check_link, args=(link + str(start_scraping + jobs_created) + "/",target_name))
                jobs.append(p)
                print("\r RUNNING: Active jobs: " + str(len(jobs)) + "  -  JOBS LEFT: " + str(to_dos - jobs_created), end="")
                p.start()
                jobs_created = jobs_created + 1
    finally:
        pass

def check_link(link, target_name):
    try:
        r = requests.get(link, verify=False, timeout=None)

        filename = r.headers['Content-Disposition'].split('filename=')[1].replace('"', '')
        # add "downloads" to the filename as a folder
        savefile = "downloads/" + filename
        # if filename starts with the same 6 characters as the target name, it is the correct pdf
        if filename[:6] == target_name[:6]:
            with open(savefile, "wb") as f:
                f.write(r.content)
                # add info to log file
                with open("downloads/log.txt", "a") as log:
                    log.write("Downloaded " + filename + " from " + link + " at " + str(time.asctime(time.localtime(time.time()))) + "\n")
        else:
            # add info to misses.txt
            with open("downloads/misses.txt", "a") as misses:
                misses.write("Not downloading " + filename + " from " + link + " at " + str(time.asctime(time.localtime(time.time()))) + "\n")
    except:
        pass

    finally:
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create directory for downloads
    # delete all " " from the searchable article

    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    if not os.path.exists("logs"):
        os.makedirs("logs")
    # create misses.txt and log.txt
    with open("logs/misses.txt", "w") as misses:
        misses.write("Misses:\n")
    with open("logs/log.txt", "w") as log:
        log.write("Log:\n")


    print("Starting job scheduler for looking for " + link)
    print("Searching for " + searchable_article + " from " + str(start_scraping) + " to " + str(end_scraping) + " with a maximum of " + str(max_jobs) + " threads at the same time")
    job_scheduler(link, searchable_article)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
