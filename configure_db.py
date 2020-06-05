import requests
import json
from db import *

def configure():
    url = "https://api.ciu.nstu.ru/v1.0/test/for_bot"


    r = requests.get(url)
    res = json.loads(r.content.decode("utf-8"))
    print("111")

    for direction in res:
        try:
            dir = Direction.insert( {"name": direction["DIRECTION"].lower().strip(),
                                    "faculty": direction["FACULT"],
                                    "keys_plus": direction["KEYS_PLUS"],
                                    "ball_k": direction["BALL_K"],
                                    "ball_b": direction["BALL_B"],
                                    "url": direction["URL"],
                                    "description": direction["DESCR"],
                                    "profile_name": direction["PROFILE_NAME"],
                                    "idNSTU": direction["ID"],
                                    "RN": direction["RN"]}).execute()
        except:
            continue
        spheres = direction["data"]
        if spheres[0]["SPHERE"] != None:
            for sphere in spheres:
                try:
                    s = Sphere.insert({"name": sphere["SPHERE"].lower().strip()}).execute()
                except:
                    s = Sphere.select().where(Sphere.name == sphere["SPHERE"].lower().strip())
                DirectionSphere.insert({"direction": dir, "sphere": s}).execute()
        subjects = [direction["DISC1"], direction["DISC2"], direction["DISC3"]]
        for subject in subjects:
            if subject.lower() == "иностр. яз.":
                subject = "иностранный язык"
            try:
                s = Subject.insert({"name": subject.lower().strip()}).execute()
            except:
                s = Subject.select().where(Subject.name == subject.lower().strip())
            DirectionSubject.insert({"direction": dir, "subject": s}).execute()

def create_faculty_table():
    with open("./faculties.txt", "r", encoding="utf8") as f:
        for line in f.readlines():
            print(line)
            name, url = line.split(" ")
            Faculty.insert({"name": name, "url": url}).execute()





if __name__ == "__main__":
    configure()
    # create_faculty_table()