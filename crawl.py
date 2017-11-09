import socket

from Portals.Indeed import IndeedCrawler


def _check_internet_connection():
	host = "8.8.8.8"
	port = 53
	timeout = 3

	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except Exception as ex:
		print("No internet connection available!")
		return False

if __name__ == "__main__":
    if _check_internet_connection():
        new_jobs = []

        ae = IndeedCrawler()
        new_jobs.extend(ae.start_crawling())

        print(new_jobs)

