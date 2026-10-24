import application.salary as sal
import application.db.people as peeps
import datetime

if __name__ == "__main__":
    print(datetime.datetime.now().date())
    print(sal.calculate_salary())
    print(peeps.get_emploees())